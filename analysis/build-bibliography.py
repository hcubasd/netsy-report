"""Rebuild cited-source bibliography from cached DOI metadata and verified source corrections."""
from pathlib import Path
import concurrent.futures,json,sys,urllib.request
ROOT=Path(__file__).resolve().parents[1]
DOIS={
'balla2023':'10.1016/j.tra.2023.103780',
'davis2024':'10.1016/j.tra.2024.104107',
'ferguson2012':'10.1016/j.jtrangeo.2012.04.013',
'smit2010':'10.1016/j.atmosenv.2010.05.022',
'ligterink2012':'10.1016/j.trd.2012.05.009',
'sakai2020':'10.1016/j.tre.2020.102017',
'microhubs2024':'10.1016/j.rtbm.2024.101186',
'harmony2024':'10.1016/j.trpro.2024.03.034',
'thoen2020emissions':'10.1109/FISTS46898.2020.9264858',
'mohammed2023':'10.1177/03611981221147049',
'holguin2008':'10.1007/s11067-007-9053-4',
'massgt2025':'10.1016/j.simpat.2025.103140',
'massgt2018':'10.1016/j.procs.2018.04.021',
'massgt2022':'10.1016/j.tranpol.2020.07.010',
'shoman2023':'10.1007/s42421-023-00065-y',
'chow2010':'10.1007/s11116-010-9281-1',
'petri2016':'10.7225/toms.v05.n02.001',
'nadi2024':'10.1016/j.trc.2023.104413',
'dias2026':'10.1016/j.ubtr.2026.100031',
'prismascr2018':'10.7326/M18-0850',
'prismas2021':'10.1186/s13643-020-01542-z',
'oliveira2022':'10.3390/su141610300',
'wisetjindawat2009':'10.11175/eastpro.2009.0.154.0',
'ryan2009':'10.1111/j.1538-4632.2009.00750.x',
'mcleod2019':'10.1016/j.tranpol.2018.11.007',
'pani2021':'10.1007/s11067-021-09530-z',
'li2023':'10.3390/su15129808',
'raothanachonkun2007':'10.11175/eastpro.2007.0.147.0',
'rong2024':'10.1145/3682058',
'basso2022':'10.3390/su14052645',
 'tavasszy2020':'10.18757/jscms.2020.1992',
'combes2012':'10.3141/2269-11',
'combes2016':'10.18757/ejtir.2016.16.1.3112',
'abate2019':'10.1007/s11116-018-9856-9',
'ahmed2023':'10.1007/s11116-022-10289-6',
'piendl2022':'10.18757/ejtir.2022.22.2.5662',
'vidal2013':'10.1016/j.ejor.2013.02.053',
'thoen2020':'10.1016/j.tre.2020.101989',
'lyu2021':'10.3390/infrastructures6120180',
'feng2013':'10.18757/ejtir.2013.13.4.3004',
'hwang2021':'10.3390/su13116369',
'wang2018':'10.1016/j.trb.2018.03.011',
'hua2025':'10.3390/act14010010',
'wang2026':'10.3390/en19215260',
'tirico2025':'10.1016/j.scs.2025.106354',
'prisma2020':'10.1136/bmj.n71'}
cache=ROOT/'references/metadata.json';metadata=json.loads(cache.read_text()) if cache.exists() else {}
def one(item):
 key,doi=item;u='https://api.crossref.org/works/'+doi
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'NetSy literature draft metadata verification'}),timeout=25) as r:j=json.load(r)['message']
 return key,{k:j[k] for k in ['DOI','title','author','container-title','volume','issue','page','article-number','published','published-print','published-online','publisher','type'] if k in j}
if '--offline' not in sys.argv:
 missing=[(k,d) for k,d in DOIS.items() if k not in metadata]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for key,j in pool.map(one,missing):metadata[key]=j
 cache.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
assert set(DOIS)<=set(metadata)
def esc(s):
 return str(s).replace('\\','\\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')
def entry(kind,key,fields):return '@'+kind+'{'+key+',\n'+''.join('  '+k+' = {'+esc(v)+'},\n' for k,v in fields.items() if v is not None)+'}\n'
years={'massgt2022':2022,'nadi2024':2024,'shoman2023':2023,'mcleod2019':2019,'abate2019':2019,'ahmed2023':2023,'tavasszy2020':2020}
versions={'massgt2022':'2022 journal issue; first available online in 2020','nadi2024':'2024 journal issue; TNO-deposited published version consulted','mcleod2019':'Accepted manuscript consulted','combes2012':'Deposited author manuscript consulted','abate2019':'Accepted manuscript consulted','vidal2013':'CIRRELT-2012-05 working-paper version consulted','rong2024':'arXiv:2306.10048v4 consulted','raothanachonkun2007':'Conference-proceedings version consulted'}
out=[]
for key,doi in DOIS.items():
 j=metadata[key];authors=' and '.join(('others' if a.get('family')=='others' else a.get('family','')+', '+a.get('given','')) for a in j.get('author',[]) if a.get('family'))
 if key=='davis2024':authors='Davis, III, Haggai and Landes, Hector and Namdarpour, Farnoosh and Yang, Hai and Chow, Joseph Y. J. and Ozbay, Kaan'
 if key=='massgt2022':authors='de Bok, Michiel and Tavasszy, Lóránt and Thoen, Sebastiaan'
 if key=='wisetjindawat2009':authors='Wisetjindawat, Wisinee and Marchal, Fabrice and Yamamoto, Koshi'
 if key=='raothanachonkun2007':authors='Raothanachonkun, Pairoj and Sano, Kazushi and Matsumoto, Shoji'
 if key=='abate2019':authors='Abate, Megersa and Vierth, Inge and Karlsson, Rune and de Jong, Gerard and Baak, Jaap'
 if key=='tirico2025':authors='Tirico, Michele and Le Bescond, Valentin and Sengelin, Delphine and Gastineau, Pascal and Can, Arnaud'
 if key=='oliveira2022':authors='de Oliveira, Leise Kelli and de Araújo, Gracielle Gonçalves Ferreira and Bertoncini, Bruno Vieira and Pinheiro, Carlos David Pedrosa and da Silva, Francisco Gildemir Ferreira'
 if key=='prisma2020':authors+=' and others'
 year=years.get(key,j.get('published-print',j.get('published',{})).get('date-parts',[[None]])[0][0])
 f={'author':authors,'title':'{'+j['title'][0]+'}','date':year,'journaltitle':j.get('container-title',[''])[0],'volume':j.get('volume'),'number':j.get('issue'),'pages':j.get('page'),'eid':j.get('article-number') if not j.get('page') else None,'doi':doi,'note':versions.get(key)}
 if key=='thoen2020emissions':f['booktitle']=f.pop('journaltitle')
 out.append(entry('inproceedings' if key=='thoen2020emissions' else 'article',key,f))
hand=[('report','kitchenham2007',{'author':'Kitchenham, Barbara and Charters, Stuart','title':'Guidelines for Performing Systematic Literature Reviews in Software Engineering','institution':'Keele University and Durham University','type':'Technical report','number':'EBSE-2007-01','date':2007,'url':'https://ebse.webspace.durham.ac.uk/ebse-bibliography/guidelines-for-performing-systematic-literature-reviews-in-software-engineering/'}),
('report','ncfrp2012',{'author':'Holguín-Veras, José and Jaller, Miguel and Sánchez-Díaz, Iván and Wojtowicz, Jeffrey and Campbell, Shama and Levinson, Herbert and Lawson, Catherine and Powers, Erica Levine and Tavasszy, Lorant','title':'Freight Trip Generation and Land Use','institution':'Transportation Research Board','type':'NCHRP Report 739 / NCFRP Report 19','date':2012,'doi':'10.17226/22659'}),
('book','sheffi1985',{'author':'Sheffi, Yossi','title':'Urban Transportation Networks: Equilibrium Analysis with Mathematical Programming Methods','publisher':'Prentice-Hall','date':1985,'url':'https://sheffi.mit.edu/book/urban-transportation-networks'}),
('thesis','celik2001',{'author':'Çelik, Hüseyin Murat','title':'Spatial Interaction Modeling of Interregional Commodity Flows','type':'PhD thesis','institution':'The Ohio State University','date':2001,'url':'https://etd.ohiolink.edu/acprod/odb_etd/etd/r/1501/10?clear=10&p10_accession_num=osu1384446243'}),
('report','odolinski2024',{'author':'Odolinski, Kristofer and Ek, Karin','title':'Estimating the Impact of Transport Costs on Firms’ Choice of Transport Chain and Shipment Size','institution':'Swedish National Road and Transport Research Institute (VTI)','type':'Working paper','number':'2024:5','date':2024,'url':'https://www.transportportal.se/VTISWoPEc/VTI%202024%205.pdf'}),
('report','tahlyan2017',{'author':'Tahlyan, Divyakant and Pinjari, Abdul R. and Luong, Trang D. and Ozkul, Seckin','title':'Truck Route Choice Modeling Using Large Streams of GPS Data','institution':'Center for Advanced Infrastructure and Transportation, Rutgers University','number':'CAIT-UTC-NC32','type':'Final report','date':2017,'url':'https://rosap.ntl.bts.gov/view/dot/34888'}),
('report','eeaRoad2026',{'author':'Ntziachristos, Leonidas and Samaras, Zissis','title':'Road Transport: Passenger Cars, Light Commercial Trucks, Heavy-Duty Vehicles Including Buses, Mopeds and Motorcycles','institution':'European Environment Agency','type':'EMEP/EEA Air Pollutant Emission Inventory Guidebook 2023','date':2026,'note':'Chapter 1.A.3.b.i--iv; June 2026 update','url':'https://copert.emisia.com/wp-content/uploads/2026/09/1.A.3.b.i-iv-Road-transport-June-2026.pdf'}),
('report','eeaWear2026',{'author':'Ntziachristos, Leonidas and Boulter, Paul','title':'Road Transport: Automobile Tyre and Brake Wear; Automobile Road Abrasion','institution':'European Environment Agency','type':'EMEP/EEA Air Pollutant Emission Inventory Guidebook 2023','date':2026,'note':'Chapters 1.A.3.b.vi--vii; May 2026 update','url':'https://copert.emisia.com/wp-content/uploads/2026/09/1.A.3.b.vi-vii-Road-tyre-and-brake-wear-May-2026.pdf'})]
hand += [
('report','moore2017',{'author':'Moore, Amy M.','title':'Proposed Methodology for a Tour-Based Freight Model','institution':'Oak Ridge National Laboratory','number':'ORNL/SPR-2017/522','date':2017,'doi':'10.2172/1505336','note':'Model-development proposal; not a completed validation study'}),
('report','fhwa2018',{'author':'{Federal Highway Administration}','title':'Behavioral/Agent-Based Supply Chain Modeling Research Synthesis and Guide','institution':'U.S. Department of Transportation','number':'FHWA-HOP-18-003','date':2018,'url':'https://ops.fhwa.dot.gov/publications/fhwahop18003/fhwahop18003.pdf'}),
('report','fhwa2017',{'author':'{Federal Highway Administration}','title':'Freight Demand Modeling and Data Improvement Handbook','institution':'U.S. Department of Transportation','number':'FHWA-HOP-18-018','date':2017,'url':'https://ops.fhwa.dot.gov/publications/fhwahop18018/fhwahop18018.pdf'}),
('report','williams2024',{'author':'Williams, Ian','title':'Peer Review: Freight Analysis and Modelling Environment (FAME) -- Stage 1','institution':'UK Department for Transport','date':'2024-03-21','note':'Final version 3.0','url':'https://assets.publishing.service.gov.uk/media/6718b8a138149ce9d09e3895/dft-peer-review-freight-analysis-modelling-environment.pdf'}),
('report','eurostat2025',{'author':'{Eurostat}','title':'Road Freight Transport Methodology','institution':'European Commission','date':2025,'note':'2025 revised edition','url':'https://ec.europa.eu/eurostat/cache/metadata/Annexes/road_go_esms_an_Road_freight_transport_methodo.pdf'}),
('report','trafa2026quality',{'author':'{Trafikanalys}','title':'Kvalitetsdeklaration: Varuflödesundersökningen 2025','institution':'Trafikanalys','date':'2026-09-18','note':'Version 1; Swedish commodity-flow survey quality declaration','url':'https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf'}),
('report','trafa2026method',{'author':'{Trafikanalys}','title':'Metodrapport: Varuflödesundersökningen 2025','institution':'Trafikanalys','number':'Statistik 2026:33','date':'2026-09-18','url':'https://www.trafa.se/globalassets/statistik/varufloden/2025/metodrapport-varuflodesundersokningen-2025.pdf'}),
('report','trafa2022',{'author':'{Trafikanalys}','title':'Metodrapport: Varuflödesundersökningen 2021','institution':'Trafikanalys','number':'Statistik 2022:33','date':2022,'url':'https://www.trafa.se/globalassets/statistik/varufloden/metodrapport-varuflodesundersokningen-2021.pdf'}),
('report','massgtmanual2023',{'author':'de Bok, Michiel and Nadi, Ali and Tavasszy, Lorant and Thoen, Sebastiaan and Eggers, Larissa','title':'MASS-GT Documentation','institution':'Delft University of Technology and Significance','date':'2023-07-06','note':'Version 3.0, HARMONY Tactical Freight Simulator; local reference checkout 4f727c3633bf5edabc1b0d0fa081a9e232bf169a','url':'https://github.com/mass-gt/tfs-harmony'}),
('online','ismael2026',{'author':'Ismael, Abdelrahman and Cokyasar, Taner','title':'Modeling and Calibration of Supplier Selection Problem in Freight Agent-Based Simulations','date':2026,'doi':'10.48550/arXiv.2511.17875','eprint':'2511.17875','eprinttype':'arxiv','note':'Author preprint, version 2; not the publisher version','url':'https://arxiv.org/abs/2511.17875v2'})
]
out +=[entry(*x) for x in hand]
(ROOT/'references/references.bib').write_text('\n'.join(out))
print('Wrote',len(out),'bibliographic entries')
