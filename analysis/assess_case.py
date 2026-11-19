"""Stream frozen NetSy emission functions over identical saved link activity.

Row-local batching changes execution memory use, not the formula. Save float32
row emissions as the CLI does, aggregate in float64, and report inherited factor
support explicitly rather than interpreting missing factors as physical zeros.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from netsy.cli.synth_network_emissions import _read
from netsy.synth.network_emissions import emissions_by_copert, emissions_by_factors


def float32_emissions(frame):
    keys={'link_id','time_interval','vehicle','segment','combustion','payload_bin'}
    columns=[c for c in frame if c not in keys]
    frame[columns]=frame[columns].astype('float32')
    return frame,columns


def main():
    p=argparse.ArgumentParser();p.add_argument('case',type=Path);p.add_argument('--seed',type=int,required=True)
    p.add_argument('--routing',required=True);p.add_argument('--coefficient',type=float,required=True);a=p.parse_args()
    case=a.case;start=time.monotonic()
    network=_read(str(case/'network.gpkg'))
    factors=_read(str(case/'emission_factors.csv'))
    types=_read(str(case/'copert_vehicles.csv'));coeff=_read(str(case/'copert_v_coefficients.csv'))
    nonexhaust=_read(str(case/'non_exhaust_factors.csv'))
    index=pd.Index(network.link_id.astype(str));length=network.length.to_numpy(float)
    classes=_read(str(case/'assignment_vehicles.csv')).vehicle.astype(str).tolist()
    support=[]
    for vehicle in classes:
        support.append(set(factors.loc[(factors.vehicle.astype(str)==vehicle)&(factors.pollutant=='co2'),'road_type']))
    common=set.intersection(*support)-{'voedingslink','Veerverbinding'}
    if not common:raise ValueError('No common inherited CO2 road-type support')
    common_link=network.road_type.isin(common).to_numpy()
    physical=~network.road_type.isin(['voedingslink','Veerverbinding']).to_numpy()
    trusted=(network.grade_status=='terrain_proxy').to_numpy()
    summary=dict(seed=a.seed,routing=a.routing,grade_coefficient=a.coefficient,
                 cohort='exploratory pilot' if a.seed<=5 else 'fixed follow-up',
                 common_road_types=sorted(common),factor_comparison='inherited versus assumed modern COPERT fleet/configuration, not pure formula or accuracy test',
                 load_rows=0,segments=[],activity={},emissions={})
    methods=['factors','copert']+(['copert-flat'] if a.routing=='massgt' and a.coefficient==0 else [])
    totals={m:{'all_g':{},'common_g':{},'parcel_common_g':{}} for m in methods}
    spatial={m:np.zeros(len(network)) for m in methods}
    parcel_spatial={m:np.zeros(len(network)) for m in methods}
    writers={};segments=set();activity={k:0.0 for k in ['network_vkt','physical_vkt','common_vkt','parcel_network_vkt','parcel_common_vkt','terrain_proxy_physical_vkt','physical_grade_weighted_km_percent','empty_network_vkt']}
    flat=network.copy();flat['grade']=0
    try:
        for batch in pq.ParquetFile(case/'network_loads.parquet').iter_batches(batch_size=250000):
            loads=batch.to_pandas();idx=index.get_indexer(loads.link_id.astype(str))
            if (idx<0).any():raise ValueError('Unmatched load link')
            parcel=(loads.segment.astype(str)=='parcel_deliveries').to_numpy()
            segments.update(loads.segment.astype(str).unique())
            vkt=loads.trips.to_numpy(float)*length[idx];mask=common_link[idx];road=physical[idx]
            for name,value in [('network_vkt',vkt.sum()),('physical_vkt',vkt[road].sum()),('common_vkt',vkt[mask].sum()),
                               ('parcel_network_vkt',vkt[parcel].sum()),('parcel_common_vkt',vkt[parcel&mask].sum()),
                               ('terrain_proxy_physical_vkt',vkt[road&trusted[idx]].sum()),
                               ('physical_grade_weighted_km_percent',(vkt[road]*np.abs(network.grade.to_numpy(float)[idx[road]])).sum()),
                               ('empty_network_vkt',vkt[loads.utilization.to_numpy(float)==0].sum())]:activity[name]+=float(value)
            summary['load_rows']+=len(loads)
            for method in methods:
                if method=='factors':frame=emissions_by_factors(loads,network,factors)
                else:frame=emissions_by_copert(loads,flat if method=='copert-flat' else network,types,coeff,nonexhaust)
                if len(frame)!=len(loads) or not np.array_equal(frame.link_id.astype(str).to_numpy(),loads.link_id.astype(str).to_numpy()):
                    raise ValueError('Emission merge changed row identity')
                frame,columns=float32_emissions(frame)
                table=pa.Table.from_pandas(frame,preserve_index=False)
                if method not in writers:writers[method]=pq.ParquetWriter(case/f'emissions-{method}.parquet',table.schema)
                writers[method].write_table(table)
                for pollutant in columns:
                    values=frame[pollutant].to_numpy(dtype=float)
                    if not np.isfinite(values).all():raise ValueError(f'Nonfinite {method}/{pollutant} emissions')
                    for scope,selection in [('all_g',slice(None)),('common_g',mask),('parcel_common_g',mask&parcel)]:
                        totals[method][scope][pollutant]=totals[method][scope].get(pollutant,0.0)+float(values[selection].sum(dtype=np.float64))
                    if pollutant=='co2':
                        np.add.at(spatial[method],idx[mask],values[mask]);np.add.at(parcel_spatial[method],idx[mask&parcel],values[mask&parcel])
    finally:
        for writer in writers.values():writer.close()
    if 'parcel_deliveries' not in segments:raise ValueError('Parcel stream not identified')
    summary['activity']=activity;summary['emissions']=totals;summary['segments']=sorted(segments)
    summary['terrain_proxy_vkt_share']=activity['terrain_proxy_physical_vkt']/activity['physical_vkt']
    summary['common_vkt_share']=activity['common_vkt']/activity['physical_vkt']
    trips=gpd.read_file(case/'delivery_tours.gpkg',ignore_geometry=True)
    summary['parcel_operations']={'tours':int(trips.tour_id.nunique()),'trips':len(trips),'delivered_parcels':float(trips.parcels.sum())}
    spatial_frame=pd.DataFrame({'link_id':index,'common_support':common_link})
    for method in methods:
        spatial_frame[method+'_co2_g']=spatial[method];spatial_frame[method+'_parcel_co2_g']=parcel_spatial[method]
    spatial_frame.to_parquet(case/'spatial-summary.parquet',index=False)
    summary['elapsed_seconds']=time.monotonic()-start
    summary['loads_sha256']=hashlib.sha256((case/'network_loads.parquet').read_bytes()).hexdigest()
    (case/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'case':str(case),'rows':summary['load_rows'],'seconds':summary['elapsed_seconds'],'co2_common_g':{m:totals[m]['common_g']['co2'] for m in methods}},indent=2),flush=True)


if __name__=='__main__':main()
