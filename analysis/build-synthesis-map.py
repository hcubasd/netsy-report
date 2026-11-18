"""Index citations in the functional findings; do not rewrite retrieval metadata.

Run from any directory. The map describes narrative use, not a fresh appraisal
or a claim that a paper was retrieved by its current synthesis section.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
framework = json.loads((ROOT / 'results/synthesis-framework.json').read_text())
text = (ROOT / 'manuscript/sections/slr/review.tex').read_text()
bib = (ROOT / 'references/references.bib').read_text()
entries = dict(re.findall(r'@\w+\{([^,]+),(.*?)(?=\n@|\Z)', bib, re.S))
evidence = json.loads((ROOT / 'references/review-evidence.json').read_text())

rows = []
for item in framework['functional_responsibilities']:
    section = text.split('\\label{' + item['latex_label'] + '}', 1)[1]
    section = re.split(r'\\(?:subsubsection|subsection)\{', section, maxsplit=1)[0]
    assert '\\paragraph{Data requirements and feasibility.}' in section, item['id']
    assert '\\paragraph{MASS-GT reference.}' in section, item['id']
    keys = sorted({key.strip() for group in re.findall(
        r'\\(?:[Tt]extcite|[Pp]arencite|[Cc]ite)(?:\[[^\]]*\])*\{([^}]+)\}', section
    ) for key in group.split(',')})
    for key in keys:
        if key not in entries:
            raise ValueError(f'Unknown bibliography key: {key}')
        match = re.search(r'\bdoi\s*=\s*\{([^}]+)\}', entries[key], re.I)
        doi = match[1] if match else ''
        ids = [source['id'] for source in evidence if doi and
               source.get('doi', '').lower() == doi.lower()]
        rows.append({'function_id': item['id'], 'function': item['name'],
                     'bib_key': key, 'doi': doi, 'held_evidence_ids': ';'.join(ids)})

with (ROOT / 'results/source-function-map.csv').open('w', newline='') as output:
    writer = csv.DictWriter(output, fieldnames=[
        'function_id', 'function', 'bib_key', 'doi', 'held_evidence_ids'
    ], lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print(f'Indexed {len(rows)} citation/function relationships across seven sections.')
