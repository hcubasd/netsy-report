"""Complement the Dutch case with an explicitly qualified AHN terrain proxy.

Uses official AHN4 national download coverages, source node IDs for direction, and cached numeric
rasters. Unknown/structural links receive an explicit zero modelling fallback
with a status flag, never an assertion of measured flat road grade.
"""
import argparse
import concurrent.futures
import hashlib
import json
import time
import urllib.request
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import shapely
import requests
import threading



def terrain_grade(a, b, length_m, valid, minimum_length=50, maximum_grade=10):
    grade = np.divide(100 * (b-a), length_m, out=np.zeros(len(a)), where=length_m > 0)
    accepted = valid & (length_m >= minimum_length) & np.isfinite(grade) & (np.abs(grade) <= maximum_grade)
    return np.where(accepted, grade, 0), accepted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--base', type=Path, default=Path('/workdir/netherlands'))
    parser.add_argument('--nodes', type=Path, default=Path('/workdir/docs/reference/sweden/mass-gt/data/NL_main/data/nodes_v5.shp'))
    args = parser.parse_args(); out = args.output; out.mkdir(parents=True, exist_ok=True)
    import io, zipfile
    cache = out/'native-5m'; cache.mkdir(exist_ok=True)
    nodes = gpd.read_file(args.nodes).set_index('NODENR')
    assert np.allclose(nodes.geometry.x,nodes.X) and np.allclose(nodes.geometry.y,nodes.Y)
    nodes=nodes.set_crs(28992,allow_override=True)
    physical = nodes.TYPENO == 0
    # Historical internal channel labels; provider products and checked grids
    # are native 5 m, not the earlier 0.5 m WCS products.
    tasks=[]; assignments={}
    for coverage, product in [('dtm_05m','DTM5'),('dsm_05m','DSM5')]:
        index=out/f'AHN4_{product}.json'
        if not index.exists():
            index.write_bytes(urllib.request.urlopen(f'https://basisdata.nl/hwh-portal/20230609_tmp/links/nationaal/Nederland/AHN4_{product}.json',timeout=60).read())
        grid=gpd.read_file(index)
        joined=gpd.sjoin(nodes.loc[physical],grid[['geometry']],how='inner',predicate='intersects')
        joined=joined.loc[~joined.index.duplicated(keep='first')]
        assignments[coverage]=joined.index_right
        for tile in sorted(joined.index_right.unique()):
            tasks.append((coverage,int(tile),grid.loc[tile,'file'],grid.loc[tile,'sha256']))
    print(f'Downloading {len(tasks)} checksum-verified native 5 m tiles',flush=True)
    sessions=threading.local()
    def fetch(task):
        if not hasattr(sessions,"http"): sessions.http=requests.Session()
        coverage,tile,url,expected=task
        path=cache/f'{coverage}-{tile}.tif'; archive=path.with_suffix('.zip')
        for attempt in range(4):
            try:
                if archive.exists() and hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:
                    archive.unlink()
                    path.unlink(missing_ok=True)
                if not archive.exists():
                    response=sessions.http.get(url,timeout=(15,60));response.raise_for_status();data=response.content
                    if hashlib.sha256(data).hexdigest()!=expected: raise ValueError('Provider checksum mismatch')
                    temporary=archive.with_suffix('.download');temporary.write_bytes(data);temporary.replace(archive)
                if not path.exists():
                    data=archive.read_bytes()
                    if hashlib.sha256(data).hexdigest()!=expected: raise ValueError('Cached checksum mismatch')
                    z=zipfile.ZipFile(io.BytesIO(data)); member=next(n for n in z.namelist() if n.lower().endswith('.tif'))
                    path.write_bytes(z.read(member))
                with rasterio.open(path) as r:
                    if r.crs.to_epsg()!=28992 or not np.allclose(r.res,[5,5]): raise ValueError('Unexpected raster grid')
                return dict(coverage=coverage,tile=tile,url=url,provider_zip_sha256=expected,raster_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            except Exception:
                if attempt==3: raise
                time.sleep(2)
    manifest=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        for i,future in enumerate(concurrent.futures.as_completed([pool.submit(fetch,t) for t in tasks]),1):
            result=future.result()
            manifest.append(result)
            if i%100==0: print(f'Cached {i}/{len(tasks)} tiles',flush=True)
    (out/'retrieval.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for coverage in ['dtm_05m','dsm_05m']:
        nodes[coverage]=np.nan; nodes[coverage+'_valid']=0
        groups=assignments[coverage]
        for tile in sorted(groups.unique()):
            ids=groups.index[groups==tile]
            with rasterio.open(cache/f'{coverage}-{tile}.tif') as raster:
                z=raster.read(1); rows,cols=[np.asarray(v,dtype=int) for v in rasterio.transform.rowcol(raster.transform,nodes.loc[ids,'X'].to_numpy(),nodes.loc[ids,'Y'].to_numpy())]
                samples=[]
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        rr=rows+dr;cc=cols+dc;inside=(rr>=0)&(rr<z.shape[0])&(cc>=0)&(cc<z.shape[1])
                        value=np.full(len(ids),np.nan);value[inside]=z[rr[inside],cc[inside]]
                        value[(~np.isfinite(value))|(np.abs(value)>10000)]=np.nan;samples.append(value)
                samples=np.array(samples);count=np.isfinite(samples).sum(axis=0)
                median=np.ma.median(np.ma.masked_invalid(samples),axis=0).filled(np.nan)
                nodes.loc[ids,coverage]=np.where(count>=5,median,np.nan)
                nodes.loc[ids,coverage+'_valid']=count
    nodes['terrain_usable'] = physical & nodes.dtm_05m.notna() & nodes.dsm_05m.notna() & ((nodes.dsm_05m-nodes.dtm_05m).abs() <= 3)
    nodes.drop(columns='geometry').to_csv(out/'node-elevation.csv',index=True)

    network = gpd.read_file(args.base/'network.gpkg')
    a=network.from_node.map(nodes.dtm_05m).to_numpy();b=network.to_node.map(nodes.dtm_05m).to_numpy()
    usable=network.from_node.map(nodes.terrain_usable).fillna(False).to_numpy() & network.to_node.map(nodes.terrain_usable).fillna(False).to_numpy()
    horizontal=network.geometry.length.to_numpy()
    # Grade uses node identity, not geometry order (reverse arcs share geometry).
    nonroad=network.road_type.isin(['voedingslink','Veerverbinding']).to_numpy()
    named_structure=network['name'].fillna('').str.contains(r'tunnel|viaduct|brug',case=False,regex=True).to_numpy()
    grade, accepted=terrain_grade(a,b,horizontal,usable & ~nonroad & ~named_structure)
    status=np.full(len(network),'terrain_proxy',dtype=object)
    status[~usable]='unresolved_elevation_or_surface'
    status[(horizontal<50)&~nonroad]='short_link_fallback'
    raw=np.divide(100*(b-a),horizontal,out=np.zeros(len(a)),where=horizontal>0)
    status[usable & (np.abs(raw)>10)]='steep_proxy_rejected'
    status[named_structure]='named_structure_fallback';status[nonroad]='nonroad_fallback'
    assert np.all((status=='terrain_proxy') == accepted)
    network['grade']=grade;network['grade_status']=status
    network['terrain_from_m']=a;network['terrain_to_m']=b
    selected=network.loc[accepted]
    ends=[shapely.get_point(selected.geometry.to_numpy(),i) for i in [0,-1]]
    ends=[np.c_[shapely.get_x(v),shapely.get_y(v)] for v in ends]
    fa=nodes.reindex(selected.from_node)[['X','Y']].to_numpy();ta=nodes.reindex(selected.to_node)[['X','Y']].to_numpy()
    same=np.maximum(np.linalg.norm(fa-ends[0],axis=1),np.linalg.norm(ta-ends[1],axis=1))
    reverse=np.maximum(np.linalg.norm(fa-ends[1],axis=1),np.linalg.norm(ta-ends[0],axis=1))
    endpoint=np.minimum(same,reverse);ratio=selected.geometry.length/(1000*selected['length'])
    qa=dict(accepted_links=len(selected),node_geometry_endpoint_max_m=float(endpoint.max()),
            node_geometry_endpoint_quantiles_m={str(q):float(np.quantile(endpoint,q)) for q in [0,.5,.99,1]},
            endpoint_mismatches_above_5m=int((endpoint>5).sum()),
            geometry_to_case_length_quantiles={str(k):v for k,v in ratio.quantile([0,.01,.5,.99,1]).to_dict().items()},
            geometry_to_case_length_mismatches_above_5percent=int(((ratio<.95)|(ratio>1.05)).sum()),
            note='Grades use projected geometry length; model kilometres retain the source case length. Length discrepancies are retained as input-quality diagnostics, not silently corrected.')
    (out/'network-geometry-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    network.to_file(out/'network.gpkg',driver='GPKG')
    # Reverse arcs must receive opposite grades if both were accepted.
    by_pair=network.loc[accepted].groupby(['from_node','to_node']).grade.first()
    for (x,y),g in by_pair.items():
        if (y,x) in by_pair.index and not np.isclose(g,-by_pair.loc[(y,x)],atol=1e-5):
            raise ValueError(f'Reverse grade mismatch {x}->{y}')
    summary=dict(source='AHN4 official national download portal; acquisition 2020–2022',
                 download_portal='https://basisdata.nl/hwh-portal/download/index.html',native_resolution_m=5,sampling_resolution_m=5,
                 node_height='median of 3x3 numeric raster samples; at least five valid',
                 surface_screen='DTM/DSM median difference <=3 m; incomplete structure screening',
                 minimum_link_m=50,maximum_abs_grade_percent=10,crs='EPSG:28992',vertical_datum='NAP',
                 direction='source from_node/to_node coordinates; shared reverse geometry not used for sign',
                 status_counts=network.grade_status.value_counts().to_dict(),
                 accepted_length_km=float(network.loc[accepted,'length'].sum()),
                 road_length_km=float(network.loc[~nonroad,'length'].sum()),
                 grade_quantiles=network.loc[accepted,'grade'].quantile([0,.01,.1,.5,.9,.99,1]).to_dict(),
                 limitation='terrain-informed proxy, not validated road-deck slope; structures and external/short links have explicit zero modelling fallback')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__': main()
