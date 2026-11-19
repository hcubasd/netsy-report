"""Record historical audit files without treating them as new paper results.

Usage: python analysis/inventory-evidence.py [AUDIT_DIRECTORY]
This inventories small audit records and inspects selected case inputs read-only;
it does not run NetSy or produce a complete input-data freeze.
"""
import csv
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path(sys.argv[1] if len(sys.argv) > 1 else '/workdir/docs/validation').resolve()
records = []
for relative in ['README.md'] + ['results/' + name + '.json' for name in [
    'metrics', 'assignment_control', 'assignment_residuals', 'vans',
    'microhub_control', 'copert_coverage', 'tour_regression'
]]:
    source = AUDIT / relative
    content = source.read_bytes()
    if source.suffix == '.json':
        json.loads(content)
    records.append({'path': str(source), 'sha256': hashlib.sha256(content).hexdigest(),
                    'bytes': len(content), 'role': 'historical audit; not rerun'})

case = AUDIT / 'copert'
with sqlite3.connect((case / 'network.gpkg').as_uri() + '?mode=ro', uri=True) as db:
    tables = [row[0] for row in db.execute(
        "SELECT table_name FROM gpkg_contents WHERE data_type='features'"
    )]
    if len(tables) != 1:
        raise ValueError('Select a network layer explicitly for this case')
    table = tables[0].replace('"', '""')
    columns = [row[1] for row in db.execute(f'PRAGMA table_info("{table}")')]
case_records = {}
for filename in ['copert_vehicles.csv', 'non_exhaust_factors.csv', 'time_intervals.csv']:
    source = case / filename
    content = source.read_bytes()
    with source.open() as stream:
        rows = list(csv.DictReader(stream))
    case_records[filename] = {'path': str(source), 'rows': len(rows),
                              'sha256': hashlib.sha256(content).hexdigest()}
    if filename == 'copert_vehicles.csv':
        case_records[filename]['declared_types'] = sorted({row['vehicle_type'] for row in rows})

data = {
    'inventoried_at_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'planning evidence inventory, not new model runs or validation',
    'proposed_netsy_freeze': '491b1d59c7d0cf5f8579f733afa6d1690a13abe6',
    'massgt_reference': '4f727c3633bf5edabc1b0d0fa081a9e232bf169a',
    'historical_run_revisions': 'See audit and its per-run records; do not relabel as the proposed freeze.',
    'complete_case_input_manifest': False,
    'audit_records': records,
    'selected_case_checks': {
        'network_path': str(case / 'network.gpkg'),
        'network_layer': tables[0],
        'grade_column_present': 'grade' in columns,
        'meaning_of_missing_grade': 'Existing COPERT implementation assumes flat grade; terrain is not observed.',
        'inputs': case_records,
    },
}
(ROOT / 'results/evidence-inventory.json').write_text(json.dumps(data, indent=2) + '\n')
print(f'Inventoried {len(records)} historical records; no simulations run.')
