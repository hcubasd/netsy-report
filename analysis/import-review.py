"""Import dated search/evidence metadata and typeset an auditable search appendix.

Usage: python analysis/import-review.py /path/to/canonical-literature-audit
PDFs and raw service responses remain outside this repository. This script does
not invent retrospective screening decisions or merge conceptual publication versions.
"""
from pathlib import Path
import json,sys,re,hashlib,csv
ROOT=Path(__file__).resolve().parents[1];AUDIT=Path(sys.argv[1]).resolve();PASS=AUDIT/'access-pass-2026-11-16';COL=AUDIT.parent/'canonical-literature'
NAMES=['Demand generation and economic representation','Spatial exchange and OD inference','Logistics decisions and shipment formation','Vehicle activity, tours and scheduling','Network models and route choice','Energy and emissions','Data availability, representation and transferability']
def esc(s):
 return str(s).replace('\\',r'\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#').replace('{',r'\{').replace('}',r'\}')
queries=[]
for stage,date,root,plan in [('I','2026-11-11',AUDIT,json.loads((AUDIT/'active-queries.json').read_text())),('II','2026-11-12',AUDIT/'round-2',json.loads((AUDIT/'round-2/search-plan.json').read_text()))]:
 for folder,qs in sorted(plan.items()):
  for i,item in enumerate(qs,1):
   name=item if isinstance(item,str) else item[0];p=root/folder/'search-history'/name;spec=json.loads((p/'queries.json').read_text())
   engines={}
   for engine in ['openalex','crossref']:
    raw=json.loads((p/(engine+'.json')).read_text());resp=raw.get('response',{});items=resp.get('results',[]) if engine=='openalex' else resp.get('message',{}).get('items',[])
    engines[engine]=dict(query=spec[engine],parameters=raw['parameters'],retrieved_at_utc=raw['retrieved_at_utc'],request_url=raw['url'],returned=len(items),error=raw.get('error'))
   queries.append(dict(id=f'A{int(folder[:2])}-{stage}-{i}',folder=folder,stage=stage,date=date,iteration=name,limit=spec['limit_per_engine'],role='active retained exploratory query',engines=engines))
latest=json.loads((PASS/'search-register.json').read_text());grouped={}
for q in latest:grouped.setdefault((q['folder'],q['query_id']),{})[q['engine']]=q
for (folder,qid),engines in sorted(grouped.items()):
 queries.append(dict(id=('M' if folder=='mass-gt-reference' else f'A{int(folder[:2])}')+'-III-'+qid,folder=folder,stage='III',date='2026-11-16',iteration=qid,limit=100,role=engines['openalex']['role'],engines={e:dict(query=v['string'],parameters=v['parameters'],retrieved_at_utc=v['retrieved_at_utc'],request_url=v['url'],returned=v['returned'],reported_total=v['reported_total'],error=v.get('error')) for e,v in engines.items()}))
(ROOT/'results/review-searches.json').write_text(json.dumps(dict(scope='Dated bounded searches; retained exploratory queries and explicit model-name refinement. Search hits are not included studies.',queries=queries),ensure_ascii=False,indent=2)+'\n')
# Reassess every held PDF by explicit eligibility; do not pretend every database record was screened.
evidence=[]
old=json.loads((AUDIT/'collection-manifest.json').read_text())
for stage,records in old.items():
 for r in records:
  pdf=COL/r['file'];partial=r.get('partial_document',False) or 'abstract-only' in pdf.name or 'first-page-only' in pdf.name
  context=r.get('doi','').lower() in ['10.1007/bf01386390','10.2172/1496012']
  evidence.append(dict(id=f"{stage}-{r['bucket'][:2]}-{r['record_id']}",title=r['title'],doi=r.get('doi',''),domains=[int(r['bucket'][:2])],cohort='previous reading collection',pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pages=r.get('pages',r.get('file_pages')),decision='awaiting full text' if partial else 'background only' if context else 'included',decision_reason='One-page partial; methods/results unavailable' if partial else 'Generic algorithm exposition or discovery compendium, not substantive domain findings' if context else 'Inspectable formulation, assessment or data specification within scope',reading=r.get('review',r.get('reading')),source_url=r.get('source_url'),retrieval_route=stage+' database or explicitly recorded supplement; see original search/access audit',file_name=pdf.name))
newmanifest=json.loads((PASS/'download-manifest.json').read_text());newnotes={r['id']:r for r in json.loads((PASS/'study-notes.json').read_text())}
for r in newmanifest:
 if not r.get('file') or r['id']=='P01':continue
 n=newnotes.get(r['id'],{}).copy()
 if r['id']=='G08':n.update(pdf_pages=[1,7,24,42],reading_depth='Identity and selected purpose, stratification and response-handling excerpts reassessed',preliminary_use='Historical Swedish survey configuration, not independent replication of the 2025 method report',limitation='Earlier edition; sector coverage and disclosure constrain local application')
 if r['id']=='L01':n.update(pdf_pages=[1,2,3,4,5,6,15],reading_depth='Selected data, routing/emissions and scenario sections reassessed',limitation='Operator-specific observational inputs; policy comparisons are scenario outputs, not independent measured pollutant validation')
 if r['id']=='M11':n.update(pdf_pages=[2,3,4,5],reading_depth='Version/control page, contents, introduction and conceptual model reassessed',limitation='2023 v3.0 technical manual at fixed checkout; not identical by assumption to the 2025 publication')
 if r['id']=='M01':n['pdf_pages']=sorted(set(n.get('pdf_pages',[])+[4,5,6,7,8,9,15]))
 evidence.append(dict(id=r['id'],title=r['title'],doi=r.get('doi',''),domains=r['buckets'],cohort='designated local reference' if r['id'] in ['L01','M11'] else '16 November additions',pdf_sha256=r['sha256'],pages=r['pages'],decision='included',decision_reason='Inspectable formulation, assessment or data specification within scope',reading=n,source_url=r.get('source_url'),retrieval_route=r.get('route'),query_membership=r.get('database_membership',[]),file_name=Path(r['file']).name))
# Institutional retrieval is a dated supplementary route, not a new topical search.
overlay_path=ROOT/'references/institutional-review.json'
institutional=json.loads(overlay_path.read_text()) if overlay_path.exists() else dict(sources=[])
received=[r for r in institutional['sources'] if r['decision']=='included']
resolved={r['doi'].lower() for r in received}
# Replace the two one-page placeholders with complete papers; retain historical files in the external audit.
evidence=[r for r in evidence if not (r['decision']=='awaiting full text' and r.get('doi','').lower() in resolved)]
evidence += received

# Link held sources to actual query IDs; keep supplements explicitly separate.
for source in evidence:
 memberships=[]
 for q in queries:
  if q['stage'] in ['I','II']:
   base=AUDIT if q['stage']=='I' else AUDIT/'round-2'
   rp=base/q['folder']/'search-history'/q['iteration']/'records.json'
  else:rp=PASS/q['folder']/'searches'/q['iteration']/'records.json'
  if not rp.exists():continue
  for rec in json.loads(rp.read_text()):
   d=(rec.get('doi') or '').lower()
   match=source.get('doi') and d==source['doi'].lower()
   if not source.get('doi'):match=re.sub(r'\W','',source['title'].lower())==re.sub(r'\W','',(rec.get('title') or '').lower())
   if match:
    for m in rec.get('matches',rec.get('found_by',[])):
     memberships.append(dict(query_id=q['id'],engine=m['engine'],rank=m['rank']))
 source['query_membership']=memberships
 if source['id']=='U03':
  source['related_publisher_doi']=source['doi'];source['doi']='10.48550/arxiv.2511.17875';source['consulted_version']='arXiv:2511.17875v2; author preprint'
 if source['id'].endswith('-D046') and source['doi']=='10.2172/1505336':source['source_type']='Model-development proposal, not completed empirical validation'
with (ROOT/'results/source-search-map.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,lineterminator='\n',fieldnames=['source_id','title','doi','query_id','engine','rank','supplementary_route']);w.writeheader()
 for source in evidence:
  ms=source['query_membership'] or [dict(query_id='',engine='',rank='')]
  for m in ms:w.writerow(dict(source_id=source['id'],title=source['title'],doi=source['doi'],**m,supplementary_route=source['retrieval_route'] if not m['query_id'] else ''))
# Save supplementary discovery/access expressions as executed, not idealized Boolean queries.
web=[]
for line in (PASS/'search-strategy-and-strings.md').read_text().splitlines():
 if line.startswith('- `') and line.endswith('`'):web.append(line[3:-1])
(ROOT/'results/review-supplements.json').write_text(json.dumps(dict(date='2026-11-16',web_discovery_and_access_queries=web,note='Includes unsuccessful access lookups; these are supplementary retrieval, not additional included studies.'),indent=2,ensure_ascii=False)+'\n')

assert len(evidence)==(61 if received else 52)
assert sum(r['decision']=='included' for r in evidence)==(59 if received else 48)
assert sum(r['decision']=='background only' for r in evidence)==2
assert sum(r['decision']=='awaiting full text' for r in evidence)==(0 if received else 2)
(ROOT/'references/review-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'results/review-selection.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,lineterminator='\n',fieldnames=['id','title','doi','domains','decision','reason']);w.writeheader()
 for r in evidence:w.writerow(dict(id=r['id'],title=r['title'],doi=r['doi'],domains=';'.join(map(str,r['domains'])),decision=r['decision'],reason=r['decision_reason']))
# Port the outstanding request list, without access logs or machine-specific paths.
requests=[]
for r in newmanifest:
 if not r.get('file') and r['id']!='P01' and r.get('doi','').lower() not in resolved:requests.append({k:r[k] for k in ['id','title','doi','buckets','reason','status'] if k in r})
(ROOT/'references/access-pending.json').write_text(json.dumps(requests,ensure_ascii=False,indent=2)+'\n')
A=[r'\section{Search and selection record}\label{app:search}',r'''This appendix reports the retrieval that produced the available collection,
including its limits. Search strings are reproduced as executed, rather than
rewritten into an idealized strategy after seeing the results. The versioned
protocol, literal requests and source-reading metadata accompany the manuscript
in \texttt{docs/review-protocol.md}, \texttt{results/review-searches.json} and
\texttt{references/review-evidence.json}. Large source PDFs and raw responses
remain in the external reading/audit collection.

\subsection{Search strategy and sources}
The first two rounds used OpenAlex full-text/metadata search and Crossref ranked
bibliographic queries, with at most 25 records per engine and configuration.
The 16 November extension used 100. Publication-date ceilings followed the
search date; there was no lower year bound. Exact parameter values and UTC
retrieval timestamps are retained in the machine-readable register. These are
ranked windows, not complete database exports. Search expressions are
engine-specific: conceptual Boolean syntax submitted to OpenAlex and term-based
Crossref queries do not establish equivalent coverage.

Eight complementary search strands comprise six subject searches, a separate
search on data availability and transferability, and MASS-GT reference discovery.
Their evidence is synthesized by functional responsibility, as described in
Section~\ref{sec:review-framework}; data feasibility and the reference
configuration inform every section. Historical identifiers A1--A7 and M remain
unchanged. MASS-GT is not appended with OR to every subject query. The first name query returned
non-transport material because of ambiguous name/token matching; the
transport-qualified refinement is shown alongside that pilot. Superseded query
variants from earlier rounds remain in the raw audit; the retained variants
below define their active snapshots. Targeted repository/title lookups serve
retrieval and identity checks, not independent evidence of topical coverage.

\subsection{Eligibility, selection and current accounting}\label{app:selection}
Eligible sources provide an identifiable formulation, empirical assessment or
data specification informing a functional responsibility or its information
requirements. Journal and conference papers,
author versions, theses, books and official guidance are eligible, with source
type retained. Optimization-only evidence is interpreted as planning evidence;
conceptual proposals are not empirical validation. Generic shortest-path
exposition and a literature-discovery compendium are background only. Partial
files and abstracts cannot support performance findings. Search language and
geographical scope are stated in Section~\ref{sec:slr-methodology}.

DOIs are normalized and titles used where DOIs are absent. Duplicates can occur
across queries and search strands; a source may inform several responsibilities
without being
counted several times. Publication versions remain linked but distinguishable.
For the November extension, the consolidated index contains 2,120 DOI/title-key
records from 2,367 returned hits. These are retrieval counts, not numbers of
eligible studies. Earlier round totals are not added to them as if globally
unique. The current reassessment covers the held-document cohort. Institutional retrieval
on 18 November supplied twelve files: eleven relevant complete papers and an
unrelated electricity-course syllabus, excluded at eligibility checking. Two
complete papers replace earlier one-page placeholders. The accounting is:

\begin{center}
\begin{tabular}{lr}
\toprule
Available-document accounting & Documents \\
\midrule
Initial held PDFs (16 November) & 52 \\
\quad Complete documents & 50 \\
\quad One-page partial documents & 2 \\
Institutionally supplied files (18 November) & 12 \\
\quad Relevant complete papers & 11 \\
\quad Unrelated syllabus excluded & 1 \\
Earlier partial placeholders replaced & 2 \\
Current complete-document cohort & 61 \\
\quad Retained as substantive evidence & 59 \\
\quad Retained as background only & 2 \\
\bottomrule
\end{tabular}
\end{center}

The commodity OD synthesis and emissions-validation review previously held as
one-page files are now available in full; their placeholders are superseded,
not counted as separate studies. Twenty-eight access requests remain unresolved,
including three of the original fourteen priorities. These access counts are
separate from the complete-document cohort.
The remaining database hits are deferred rather than
assigned invented full-text exclusion reasons. No complete identification-to-
inclusion PRISMA flow is claimed. AI-assisted prioritization and extraction have
not been independently duplicated. Full-text availability and single-assessor
judgement can influence the synthesis even when reported transparently.

\subsection{Extraction and appraisal record}
The retained metadata records the source/version, inspected PDF pages, modelling
object, formulation, data role, assessment design and inference limits. Public
tabulations, confidential microdata, borrowed parameters and synthetic inputs
are distinguished. Controls used to construct a model do not become independent
validation data merely because their totals match. Reviews and related
publications are not independent votes for consensus. Narrative findings are
conditional on the inspected evidence; no pooled quality or accuracy score is
computed.

\subsection{Exact topic and model-name searches}
Round I is dated 11 November, round II 12 November and round III 16 November
2026. The following identifiers also link sources and queries in the supporting
metadata. Both engine strings are printed even when only one retrieved a
particular paper. Supplementary sources need not have database-query membership.
''']
for folder in [f'{i:02}-'+['demand-generation','spatial-exchange','logistics-decisions','vehicle-operations','network-models','energy-emissions','data-availability'][i-1] for i in range(1,8)]+['mass-gt-reference']:
 title='MASS-GT reference discovery' if folder=='mass-gt-reference' else NAMES[int(folder[:2])-1]
 A.append('\\subsubsection{'+esc(title)+'}')
 for q in [q for q in queries if q['folder']==folder]:
  A.append('\\paragraph{'+esc(q['id'])+' ('+q['date']+').} Limit: '+str(q['limit'])+' per engine. '+('Model-name pilot; superseded by the transport-qualified refinement.' if 'superseded' in q['role'] else ''))
  for engine in ['openalex','crossref']:
   A += ['\\noindent '+('OpenAlex' if engine=='openalex' else 'Crossref')+':',r'\begin{quote}\footnotesize\ttfamily\raggedright',esc(q['engines'][engine]['query']),r'\end{quote}']
A += [r'\subsection{Supplementary web discovery and access searches}', r'''The following expressions were used for targeted discovery, identity or access
follow-up on 16 November. Not every query returned a retained source. They are
separate from the paired topical searches and are not equivalent to database
eligibility decisions.''', r'\begin{longtable}{@{}p{.08\linewidth}p{.86\linewidth}@{}}',r'\toprule ID & Expression \\ \midrule\endhead']
for i,q in enumerate(web,1):A.append('S'+str(i)+' & '+esc(q)+r' \\[.4em]')
A.append(r'\bottomrule\end{longtable}')

A+=[r'''\subsection{Supplementary retrieval and the fixed reference}
The official MASS-GT project bibliography and its overview repository identify
model publications in addition to model-name searching. Targeted backward
tracing from \textcite{massgt2025} selected the SimMobility, CRISTAL and FRETURB
references for access follow-up; this was not exhaustive snowballing. Other
supplements include foundational books, theses, official FHWA and EMEP/EEA
manuals, Eurostat guidance, UK model-review material and Trafikanalys survey
documentation. Their institutions, versions and retrieval routes are retained
with each source. Exact-title and DOI searches sought public full text and
verified identities. Sources obtained through these routes are not represented
as products of a bucket string that did not retrieve them.

The Swedish operator-level study is an explicitly designated application case
\parencite{dias2026}. MASS-GT technical documentation version~3.0, dated
6 July 2023, is retained at checkout
\begin{quote}\footnotesize\ttfamily\raggedright
4f727c3633bf5edabc1b0d0fa081a9e232bf169a
\end{quote}
This fixes the technical reference; it does not establish that the 2025 article
specifies exactly that checkout. Published descriptions, code and scenario
inputs require separate reconciliation for later numerical comparisons.

\subsection{Remaining priority full texts awaiting access}
The sources below are retrieval priorities, not supporting full-text evidence
for the present findings. Some have public repository copies whose download
endpoints failed; others require an institutional-access attempt. Failure to
retrieve is not a scientific exclusion. Additional lower-priority requests are
retained in the supporting access list.
\begin{longtable}{@{}p{.10\linewidth}p{.84\linewidth}@{}}
\toprule ID & Source and DOI \\
\midrule\endhead
''']
priority=['D16','D03','D06','U01','M07','M06','M09','M08','C01','A09','A08','A01','A03','A05'];byid={r['id']:r for r in requests}
for id in priority:
 if id not in byid:continue
 r=byid[id];A.append(esc(id)+' & '+esc(r['title'])+r'\newline '+r'\url{https://doi.org/'+r['doi']+r'} \\[.6em]')
A += [r'\bottomrule\end{longtable}',r'''\subsection{Amendment and update boundary}
The 16 November revision added a data-availability search strand, separate
MASS-GT discovery and explicit data-access extraction. The protocol for this
reassessment was recorded after exploratory collection, not backdated. The
18 November amendment incorporates eleven institutionally supplied complete
papers after identity, completeness and eligibility checks, excluding one
unrelated upload. Original search dates and expressions are unchanged: this is
retrieval of previously identified sources, not a new database search. Relevant
methods, data, results and limitations were inspected; the IEEE emissions paper
required page-rendered OCR and visual checking because embedded text was corrupt.
Release v0.1.0 fixed this evidence snapshot. A subsequent 18 November
amendment reorganizes the narrative into seven functional responsibilities,
informed by eight search strands. Data requirements and the MASS-GT reference
are integrated within each responsibility. The search expressions, retrieval
dates, source cohort and selection decisions are unchanged; no new database
search or independent screening is implied. Historical metadata fields named
\texttt{domains} retain A1--A7 retrieval-topic identifiers, not functional
section numbers. Release v0.2.0 fixes this functional synthesis framework.
Remaining access gaps and search-coverage limitations stay explicit. No conclusion about NetSy's
implemented formulation, numerical superiority or general transferability is
implied by this review.
''']
(ROOT/'manuscript/sections/slr/search-appendix.tex').write_text('\n'.join(line.rstrip() for line in '\n\n'.join(A).splitlines()).rstrip()+'\n')
print('Imported',len(queries),'query pairs and',len(evidence),'held-source decisions; appendix generated.')
