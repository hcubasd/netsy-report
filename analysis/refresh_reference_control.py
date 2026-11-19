"""Refresh fixed-source-trip correspondence without rerunning MASS-GT."""
import argparse,hashlib,json,os,sys
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from run_paper_experiments import link_inputs,stage,MODEL,HERE

p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();root=a.root.resolve()
case=root/'fixed-reference-trips';link_inputs(root/'inputs',case)
source=Path('/workdir/docs/validation/reference-trips')
manifest=[]
for name in ['tours.gpkg','delivery_tours.gpkg','trip_matrices.omx']:
    src=source/name;dst=case/name
    if dst.is_symlink():dst.unlink()
    if not dst.exists():dst.symlink_to(src.resolve())
    manifest.append(dict(name=name,source=str(src.resolve()),sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
(case/'import-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
env=dict(os.environ,PYTHONPATH=str(MODEL/'src'),NETSY_WORKERS='1',PAPER_PATH_CACHE=str(root/'path-cache'))
for name,output in [('network-loads','network_loads.parquet'),('network-emissions','network_emissions.parquet')]:
    stage(case,name,[sys.executable,str(HERE/'experiment_stage.py'),'synth',name,'--force'],output,env)
refpath=Path('/workdir/docs/reference/sweden/mass-gt/runs/NL_REF/links_loaded_REF_intensities.csv')
ref=pd.read_csv(refpath);loads=pd.read_parquet(case/'network_loads.parquet');emissions=pd.read_parquet(case/'network_emissions.parquet')
ids=pd.Index([str(i) for i in range(1,len(ref)+1)]);bylink=loads.groupby(loads.link_id.astype(str)).trips.sum().reindex(ids,fill_value=0).to_numpy();delta=bylink-ref.N_TOT.to_numpy()
result=dict(role='fresh NetSy fixed-trip control against existing MASS-GT reference, not a new source run',source_sha256=hashlib.sha256(refpath.read_bytes()).hexdigest(),links=len(ids),max_abs_link_trips=float(np.abs(delta).max()),mae_link_trips=float(np.abs(delta).mean()),rmse_link_trips=float(np.sqrt(np.mean(delta**2))),sum_link_trip_difference=float(delta.sum()),emissions={})
network=gpd.read_file(case/'network.gpkg',ignore_geometry=True);network['link_id']=network.link_id.astype(str)
parcels=loads[loads.segment=='parcel_deliveries'].copy();parcels['link_id']=parcels.link_id.astype(str);parcels=parcels.merge(network[['link_id','road_type','length']],on='link_id')
factors=pd.read_csv(case/'emission_factors.csv');urban={'ETW_bibeko_30','GOW_bibeko_50','GOW_bibeko_70','WOW_bibeko_50','Verblijfsgebied_15'}
for pollutant,source_name in [('co2','CO2'),('so2','SO2'),('pm','PM'),('nox','NOX')]:
    ours=float(emissions[pollutant].to_numpy(dtype=float).sum());original=float(ref[source_name].sum()*1000)
    rows=parcels.merge(factors[factors.pollutant==pollutant],on=['vehicle','road_type'],how='left')
    correction=float(((rows.trips-1)*rows.length*(rows['empty']+rows.utilization*(rows.full-rows['empty']))).where(rows.road_type.isin(urban),0).sum())
    result['emissions'][pollutant]=dict(massgt_g=original,netsy_g=ours,difference_g=ours-original,predicted_source_parcel_accumulation_fix_g=correction,residual_g=ours-original-correction)
(case/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
