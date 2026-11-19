"""Isolated, resumable Dutch experiments using frozen NetSy 0.5.0.

Prepare upstream realizations first; assignment requires the completed terrain
adapter. No historical case outputs or original case inputs are overwritten.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

HERE=Path(__file__).resolve().parent
MODEL=Path('/workdir/netsy')
FREEZE='491b1d59c7d0cf5f8579f733afa6d1690a13abe6'
OUTPUTS={'agents.gpkg','shipments.gpkg','routed_shipments.gpkg','routed_parcel_demand.csv',
         'tours.gpkg','tour_shipments.csv','parcel_demand.csv','delivery_tours.gpkg',
         'network_loads.parquet','network_emissions.parquet','trip_matrices.omx','timings.json'}


def link_inputs(inputs,case,skip=()):
    case.mkdir(parents=True,exist_ok=True)
    for p in inputs.iterdir():
        if p.is_file() and p.name not in skip and not (case/p.name).exists():
            (case/p.name).symlink_to(p.resolve())


def stage(case,name,command,output,env):
    stamp=case/(name+'-completed.json')
    if stamp.exists() and (case/output).exists():
        return
    start=time.monotonic();print(case.name,name,'start',flush=True)
    with (case/(name+'.log')).open('w') as log:
        result=subprocess.run(command,cwd=case,env=env,stdout=log,stderr=subprocess.STDOUT)
    record=dict(command=command,seconds=time.monotonic()-start,returncode=result.returncode,
                model_commit=FREEZE,output=output)
    if result.returncode:
        (case/(name+'-failed.json')).write_text(json.dumps(record,indent=2)+'\n')
        print((case/(name+'.log')).read_text()[-4000:],flush=True)
        raise RuntimeError(f'{case}: {name} failed')
    if not (case/output).exists():raise RuntimeError(f'{case}: expected {output}')
    stamp.write_text(json.dumps(record,indent=2)+'\n');print(case.name,name,round(record['seconds'],2),'seconds',flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--seeds',nargs='+',type=int,default=[1,2,3,4,5]);p.add_argument('--prepare',action='store_true');p.add_argument('--execute',action='store_true');p.add_argument('--assign-only',action='store_true');p.add_argument('--coefficients',nargs='+',type=float,default=[0,.05,.2]);a=p.parse_args()
    root=a.root.resolve();root.mkdir(parents=True,exist_ok=True);inputs=root/'inputs';inputs.mkdir(exist_ok=True)
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=MODEL,text=True).strip()!=FREEZE:
        raise ValueError('Model is not the planned frozen commit')
    if subprocess.check_output(['git','status','--porcelain'],cwd=MODEL,text=True).strip():
        raise ValueError('Frozen model worktree must be clean')
    if not (root/'input-snapshot.json').exists():
        manifest=[]
        for f in sorted(Path('/workdir/netherlands').iterdir()):
            if f.is_file() and f.name not in OUTPUTS and f.suffix in ['.csv','.gpkg','.omx']:
                shutil.copy2(f,inputs/f.name)
                manifest.append(dict(name=f.name,source=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
        (root/'input-snapshot.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (root/'environment.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
    env=dict(os.environ,PYTHONPATH=str(MODEL/'src'),NETSY_WORKERS='1',PAPER_PATH_CACHE=str(root/'path-cache'))
    def cli(*args):return [sys.executable,str(HERE/'experiment_stage.py'),'synth',*args,'--force']
    for seed in a.seeds:
        upstream=root/f'seed-{seed}'/'upstream';link_inputs(inputs,upstream)
        if a.prepare:
            for name,args,output in [
                ('agents',['--seed',str(seed),'--min-size','4'],'agents.gpkg'),
                ('shipments',['--seed',str(seed)],'shipments.gpkg'),
                ('tours',['--seed',str(seed)],'tours.gpkg'),
                ('parcel-demand',[],'parcel_demand.csv'),
                ('deliveries',['--seed',str(seed)],'delivery_tours.gpkg')]:
                stage(upstream,name,cli(name,*args),output,env)
            common=root/'common';link_inputs(inputs,common)
            stage(common,'trip-matrices',cli('trip-matrices'),'trip_matrices.omx',env)
            if not (upstream/'trip_matrices.omx').exists():(upstream/'trip_matrices.omx').symlink_to(common/'trip_matrices.omx')
            savings=root/f'seed-{seed}'/'savings-tours';link_inputs(inputs,savings)
            if not (savings/'parcel_demand.csv').exists():(savings/'parcel_demand.csv').symlink_to(upstream/'parcel_demand.csv')
            stage(savings,'deliveries',cli('deliveries','--seed',str(seed),'--routing','savings'),'delivery_tours.gpkg',env)
        if not a.execute:continue
        terrain=root.parent/'elevation'/'network.gpkg'
        if not terrain.exists() and (not a.assign_only or any(a.coefficients)):
            raise ValueError('Terrain completion must finish first except zero-cost assignment-only controls')
        for routing in ['massgt','savings']:
            for coefficient in a.coefficients:
                tag='g'+str(float(coefficient)).replace('.','p')
                case=root/f'seed-{seed}'/(routing+'-'+tag)
                link_inputs(inputs,case,skip=['network.gpkg','assignment_vehicles.csv'])
                target=terrain if terrain.exists() else inputs/'network.gpkg'
                if (case/'network.gpkg').is_symlink() and (case/'network.gpkg').resolve()!=target.resolve():
                    (case/'network.gpkg').unlink()
                if not (case/'network.gpkg').exists():(case/'network.gpkg').symlink_to(target)
                vehicles=pd.read_csv(inputs/'assignment_vehicles.csv')
                vehicles['uphill_cost_per_km_per_percent']=coefficient
                vehicles['downhill_cost_per_km_per_percent']=0
                vehicles.to_csv(case/'assignment_vehicles.csv',index=False)
                for name,source in [('tours.gpkg',upstream/'tours.gpkg'),
                                    ('trip_matrices.omx',upstream/'trip_matrices.omx'),
                                    ('delivery_tours.gpkg',upstream/'delivery_tours.gpkg' if routing=='massgt' else root/f'seed-{seed}'/'savings-tours'/'delivery_tours.gpkg')]:
                    if not source.is_file():raise ValueError(f'Upstream output not ready: {source}')
                    if not (case/name).exists():(case/name).symlink_to(source.resolve())
                stage(case,'network-loads',cli('network-loads','--payload-strata'),'network_loads.parquet',env)
                if a.assign_only:continue
                command=[sys.executable,str(HERE/'assess_case.py'),str(case),'--seed',str(seed),'--routing',routing,'--coefficient',str(coefficient)]
                stage(case,'assessment',command,'summary.json',env)


if __name__=='__main__':main()
