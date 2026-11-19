"""Publish compact evidence from every completed paired pilot configuration."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,default=Path('results/dutch-pilot'));a=p.parse_args()
    out=a.output;out.mkdir(parents=True,exist_ok=True)
    records=[];summaries=[]
    for f in sorted(a.root.glob('seed-*/*/summary.json')):
        s=json.loads(f.read_text());summaries.append(s)
        for method,e in s['emissions'].items():
            if method=='copert-flat':continue
            r={k:s[k] for k in ['seed','routing','grade_coefficient','load_rows','terrain_proxy_vkt_share','common_vkt_share']}
            r.update(method=method,**s['activity'],**s['parcel_operations'])
            for scope,values in e.items():
                for pollutant,v in values.items():r[f'{scope}_{pollutant}']=v
            records.append(r)
    df=pd.DataFrame(records)
    expected={(s,r,c,m) for s in range(1,6) for r in ['massgt','savings'] for c in [0,.05,.2] for m in ['factors','copert']}
    actual=set(df[['seed','routing','grade_coefficient','method']].itertuples(index=False,name=None))
    if actual!=expected:raise ValueError(f'Incomplete experiment: missing {expected-actual}; extra {actual-expected}')
    assert (df.delivered_parcels==228707).all()
    import geopandas as gpd
    conservation=[]
    for seed in range(1,6):
        first=gpd.read_file(a.root/f'seed-{seed}'/'upstream'/'delivery_tours.gpkg',ignore_geometry=True)
        second=gpd.read_file(a.root/f'seed-{seed}'/'savings-tours'/'delivery_tours.gpkg',ignore_geometry=True)
        keys=['carrier','destination_zone_id']
        pd.testing.assert_series_equal(first.groupby(keys).parcels.sum().sort_index(),second.groupby(keys).parcels.sum().sort_index(),check_dtype=False)
        assert first.quantity.max()<=180 and second.quantity.max()<=180
        conservation.append(dict(seed=seed,delivered=int(first.parcels.sum()),inherited_tours=int(first.tour_id.nunique()),savings_tours=int(second.tour_id.nunique()),maximum_parcels_onboard_inherited=float(first.quantity.max()),maximum_parcels_onboard_savings=float(second.quantity.max()),customer_carrier_quantities_identical=True))
    (out/'parcel-conservation.json').write_text(json.dumps(conservation,indent=2)+'\n')
    upstream=[]
    for seed in range(1,6):
        folder=a.root/f'seed-{seed}'/'upstream'
        agents=gpd.read_file(folder/'agents.gpkg',ignore_geometry=True,columns=['size'])
        shipments=gpd.read_file(folder/'shipments.gpkg',ignore_geometry=True,columns=['quantity'])
        tours=gpd.read_file(folder/'tours.gpkg',ignore_geometry=True,columns=['tour_id'])
        upstream.append(dict(seed=seed,agents=len(agents),employment=float(agents['size'].sum()),shipments=len(shipments),shipment_tonnes=float(shipments.quantity.sum()),freight_tours=int(tours.tour_id.nunique()),freight_trips=len(tours)))
    pd.DataFrame(upstream).to_csv(out/'upstream-realizations.csv',index=False)
    audit=Path('/workdir/docs/validation/results/metrics.json')
    historical=json.loads(audit.read_text())['netsy_saved_baseline']
    baseline=df[(df.seed==1)&(df.routing=='massgt')&(df.grade_coefficient==0)&(df.method=='factors')].iloc[0]
    regression=dict(audit_sha256=hashlib.sha256(audit.read_bytes()).hexdigest(),role='fresh seed-1 regression against historical NetSy audit, not source validation',old_rows=historical['loads']['rows'],new_rows=int(baseline.load_rows),row_count_explanation='Payload-stratified assignment increases row count; aggregate activity and linear inherited factors are conserved.',vkt_difference=float(baseline.network_vkt-historical['loads']['vkt']),emissions_difference_g={k:float(baseline['all_g_'+k]-v) for k,v in historical['emissions_grams'].items()},tolerances=dict(vkt=1e-6,pollutant_g=1))
    assert abs(regression['vkt_difference'])<1e-6 and max(map(abs,regression['emissions_difference_g'].values()))<1
    assert upstream[0]['agents']==historical['agents']['count'] and upstream[0]['shipments']==historical['shipments']['count']
    (out/'baseline-regression.json').write_text(json.dumps(regression,indent=2)+'\n')

    df.to_csv(out/'configurations.csv',index=False)
    (out/'summaries.json').write_text(json.dumps(summaries,indent=2)+'\n')
    contrast=[]
    indexed=df.set_index(['seed','routing','grade_coefficient','method'])
    for seed in range(1,6):
        for method in ['factors','copert']:
            for coefficient in [0,.05,.2]:
                base=indexed.loc[(seed,'massgt',coefficient,method)]
                alt=indexed.loc[(seed,'savings',coefficient,method)]
                for metric in ['network_vkt','parcel_network_vkt','parcel_common_vkt','common_g_co2','parcel_common_g_co2']:
                    contrast.append(dict(seed=seed,contrast='scheduling',method=method,grade_coefficient=coefficient,metric=metric,
                                         baseline=float(base[metric]),alternative=float(alt[metric]),difference=float(alt[metric]-base[metric]),percent=float(100*(alt[metric]/base[metric]-1))))
            for routing in ['massgt','savings']:
                base=indexed.loc[(seed,routing,0,method)]
                for coefficient in [.05,.2]:
                    alt=indexed.loc[(seed,routing,coefficient,method)]
                    for metric in ['network_vkt','parcel_network_vkt','parcel_common_vkt','common_g_co2','parcel_common_g_co2','physical_grade_weighted_km_percent']:
                        contrast.append(dict(seed=seed,contrast='grade-'+routing,method=method,grade_coefficient=coefficient,metric=metric,
                                             baseline=float(base[metric]),alternative=float(alt[metric]),difference=float(alt[metric]-base[metric]),percent=float(100*(alt[metric]/base[metric]-1))))
    for seed in range(1,6):
        for routing in ['massgt','savings']:
            for coefficient in [0,.05,.2]:
                base=indexed.loc[(seed,routing,coefficient,'factors')]
                alt=indexed.loc[(seed,routing,coefficient,'copert')]
                for metric in ['common_g_co2','parcel_common_g_co2']:
                    contrast.append(dict(seed=seed,contrast='factor-'+routing,method='copert-vs-inherited',grade_coefficient=coefficient,metric=metric,
                                         baseline=float(base[metric]),alternative=float(alt[metric]),difference=float(alt[metric]-base[metric]),percent=float(100*(alt[metric]/base[metric]-1))))
    paired_checks=[]
    for seed in range(1,6):
        for coefficient in [0,.05,.2]:
            for method in ['factors','copert']:
                base=indexed.loc[(seed,'massgt',coefficient,method)];alt=indexed.loc[(seed,'savings',coefficient,method)]
                vkt_residual=(alt.network_vkt-base.network_vkt)-(alt.parcel_network_vkt-base.parcel_network_vkt)
                co2_residual=(alt.common_g_co2-base.common_g_co2)-(alt.parcel_common_g_co2-base.parcel_common_g_co2)
                if abs(vkt_residual)>1e-5 or abs(co2_residual)>1:raise ValueError('Scheduling altered nonparcel totals beyond numerical tolerance')
                paired_checks.append(dict(seed=seed,grade_coefficient=coefficient,method=method,nonparcel_vkt_residual=float(vkt_residual),nonparcel_co2_residual_g=float(co2_residual)))
    pd.DataFrame(paired_checks).to_csv(out/'paired-control-checks.csv',index=False)
    interactions=[]
    for seed in range(1,6):
        for coefficient in [0,.05,.2]:
            for metric in ['common_g_co2','parcel_common_g_co2']:
                f0=indexed.loc[(seed,'massgt',coefficient,'factors'),metric];f1=indexed.loc[(seed,'savings',coefficient,'factors'),metric]
                c0=indexed.loc[(seed,'massgt',coefficient,'copert'),metric];c1=indexed.loc[(seed,'savings',coefficient,'copert'),metric]
                interactions.append(dict(seed=seed,grade_coefficient=coefficient,metric=metric,scheduling_difference_inherited_g=f1-f0,scheduling_difference_copert_g=c1-c0,difference_of_differences_g=(c1-c0)-(f1-f0),relative_effect_difference_percentage_points=100*((c1/c0-1)-(f1/f0-1))))
    pd.DataFrame(interactions).to_csv(out/'scheduling-factor-interactions.csv',index=False)
    direct=[]
    for s in summaries:
        if 'copert-flat' in s['emissions']:
            for scope in ['common_g','parcel_common_g']:
                flat=s['emissions']['copert-flat'][scope]['co2'];graded=s['emissions']['copert'][scope]['co2']
                direct.append(dict(seed=s['seed'],scope=scope,flat_g=flat,graded_g=graded,percent=100*(graded/flat-1)))
    pd.DataFrame(direct).to_csv(out/'direct-grade-contrast.csv',index=False)
    contrasts=pd.DataFrame(contrast);contrasts.to_csv(out/'paired-contrasts.csv',index=False)
    aggregate=contrasts.groupby(['contrast','method','grade_coefficient','metric']).percent.agg(['mean','min','max','std','count']).reset_index()
    aggregate.to_csv(out/'contrast-summary.csv',index=False)
    # Grade tradeoffs: inherited scheduler, paired across upstream realizations.
    fig,axes=plt.subplots(1,3,figsize=(7,2.7),constrained_layout=True)
    for ax,(metric,label) in zip(axes,[('network_vkt','Network vehicle-km'),('common_g_co2','Common-support CO₂'),('physical_grade_weighted_km_percent','Absolute grade × VKT')]):
        methods=['factors','copert'] if metric=='common_g_co2' else ['factors']
        for method in methods:
            g=aggregate[(aggregate.contrast=='grade-massgt')&(aggregate.metric==metric)&(aggregate.method==method)].sort_values('grade_coefficient')
            x=np.r_[0,g.grade_coefficient];y=np.r_[0,g['mean']]
            low=np.r_[0,g['min']];high=np.r_[0,g['max']]
            ax.plot(x,y,'o-' if method=='factors' else 's--',color='black' if method=='factors' else '.5',lw=1,ms=4,label='Inherited' if method=='factors' else 'COPERT configuration')
            ax.fill_between(x,low,high,color='.8',alpha=.5)
        ax.axhline(0,color='.5',ls=':',lw=.7);ax.set_title(label,fontsize=9)
        ax.set_xlabel('Uphill coefficient',fontsize=8);ax.set_xticks([0,.05,.2]);ax.tick_params(labelsize=8)
    axes[0].set_ylabel('Change from zero penalty (%)',fontsize=9)
    axes[1].legend(fontsize=7,frameon=False)
    fig.savefig(out/'grade-effects.pdf');fig.savefig(out/'grade-effects.png',dpi=180);plt.close(fig)
    # Parcel outcomes coincide to displayed precision; avoid redundant replicate ranges.
    lines=['\\begin{tabular}{@{}lrrr@{}}\n\\toprule Scheduling contrast (\\%) & $u=0$ & $u=0.05$ & $u=0.20$ ' + r'\\' + '\n\\midrule\n']
    for label,method,metric in [('Parcel VKT','factors','parcel_common_vkt'),('Parcel CO$_2$, inherited','factors','parcel_common_g_co2'),('Parcel CO$_2$, COPERT','copert','parcel_common_g_co2')]:
        values=[]
        for c in [0,.05,.2]:
            g=aggregate[(aggregate.contrast=='scheduling')&(aggregate.method==method)&(aggregate.grade_coefficient==c)&(aggregate.metric==metric)].iloc[0]
            assert round(g['min'],2)==round(g['max'],2), 'Parcel replicate variation requires explicit ranges'
            values.append(f'{g["mean"]:+.2f}')
        lines.append(label+' & '+' & '.join(values)+' '+r'\\'+'\n')
    lines.append('\\bottomrule\n\\end{tabular}\n');(out/'scheduling-table.tex').write_text(''.join(lines))
    def result(contrast,method,coefficient,metric):
        return aggregate[(aggregate.contrast==contrast)&(aggregate.method==method)&(aggregate.grade_coefficient==coefficient)&(aggregate.metric==metric)].iloc[0]
    macros={}
    baseline=df[(df.routing=='massgt')&(df.grade_coefficient==0)]
    bf=baseline[baseline.method=='factors'];bc=baseline[baseline.method=='copert']
    macros['BaselineMeanVkt']=f'{bf.network_vkt.mean()/1e6:.3f}'
    macros['BaselineFactorTonnes']=f'{bf.common_g_co2.mean()/1e6:,.1f}'
    macros['BaselineCopertTonnes']=f'{bc.common_g_co2.mean()/1e6:,.1f}'
    macros['BaselineTerrainCoverage']=f'{100*bf.terrain_proxy_vkt_share.mean():.2f}'
    macros['BaselineCommonCoverage']=f'{100*bf.common_vkt_share.mean():.3f}'
    selections=[('SchedulingNetworkVkt','scheduling','factors',0,'network_vkt',4),('SchedulingParcelNetworkVkt','scheduling','factors',0,'parcel_network_vkt',2),('SchedulingParcelVkt','scheduling','factors',0,'parcel_common_vkt',2),('SchedulingFactorCo','scheduling','factors',0,'common_g_co2',4),('SchedulingCopertCo','scheduling','copert',0,'common_g_co2',4),('GradeNetworkVkt','grade-massgt','factors',.2,'network_vkt',4),('GradeFactorCo','grade-massgt','factors',.2,'common_g_co2',4),('GradeCopertCo','grade-massgt','copert',.2,'common_g_co2',4),('GradeExposure','grade-massgt','factors',.2,'physical_grade_weighted_km_percent',2),('FactorFleetCo','factor-massgt','copert-vs-inherited',0,'common_g_co2',2)]
    for name,contrast,method,c,metric,precision in selections:
        g=result(contrast,method,c,metric)
        for suffix,key in [('Mean','mean'),('Min','min'),('Max','max')]:macros[name+suffix]=f'{g[key]:+.{precision}f}'
    macros['DirectGradeCo']=f'{pd.DataFrame(direct).query("scope == 'common_g'").percent.mean():+.4f}'
    strong=df[(df.routing=='massgt')&(df.grade_coefficient==.2)&(df.method=='factors')]
    coverage=strong.set_index('seed').terrain_proxy_vkt_share-bf.set_index('seed').terrain_proxy_vkt_share
    macros['GradeCoverageChange']=f'{100*coverage.mean():+.3f}'
    (out/'metrics.tex').write_text(''.join('\\newcommand{\\'+name+'}{'+value+'}\n' for name,value in macros.items()))
    stages=[]
    for f in sorted(list(a.root.glob('seed-*/*/*-completed.json'))+list(a.root.glob('common/*-completed.json'))+list(a.root.glob('fixed-reference-trips/*-completed.json'))):
        stages.append(dict(path=str(f.relative_to(a.root)),**json.loads(f.read_text())))
    provenance=dict(model_commit='491b1d59c7d0cf5f8579f733afa6d1690a13abe6',root=str(a.root),replicates=[1,2,3,4,5],role='exploratory pilot; no confirmatory precision claim',stages=stages,analysis_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')})
    (out/'run-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(aggregate.to_string(index=False))


if __name__=='__main__':main()
