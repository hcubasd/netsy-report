"""Publication build checks and packaging; Python standard library only."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def configuration(root=ROOT):
    data = json.loads((root / 'publication.json').read_text())
    if not re.fullmatch(r'[a-z][a-z0-9-]*', data['id']):
        raise ValueError('publication id must be a lowercase filename-safe slug')
    if type(data['major']) is not int or data['major'] < 0:
        raise ValueError('major must be a nonnegative integer')
    if type(data['publish_pdf']) is not bool:
        raise ValueError('publish_pdf must be a boolean')
    if not isinstance(data['title'], str) or not data['title'].strip():
        raise ValueError('publication title is required')
    return data


def release_tag(tag, config):
    match = re.fullmatch(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', tag)
    if not match:
        raise ValueError('release tags must be vMAJOR.MINOR.PATCH without leading zeros')
    if int(match[1]) != config['major']:
        raise ValueError('tag major does not match publication.json')
    if config['major'] == 0 or not config['publish_pdf']:
        raise ValueError('PDF publication is disabled for this branch/template')
    return tag


def log_problems(text):
    patterns = (
        r'Overfull \\[hv]box',
        r'(?:Citation|Reference)[^\n]*undefined',
        r'There were undefined (?:references|citations)',
        r'Label(?:s| [^\n]*)[^\n]*multiply defined',
        r'There were multiply-defined labels',
        r'Please \(re\)run Biber',
        r'Please rerun LaTeX',
        r'Rerun to get cross-references right',
        r'No file [^\n]*\.bbl',
        r'^! ',
    )
    return [line for line in text.splitlines() if any(re.search(p, line, re.I) for p in patterns)]


def check(root=ROOT):
    configuration(root)
    log = root / 'build/main.log'
    if not log.is_file() or not (root / 'build/main.pdf').is_file():
        raise ValueError('build/main.log and build/main.pdf required; run make build')
    problems = log_problems(log.read_text(errors='replace'))
    blg = root / 'build/main.blg'
    if blg.exists():
        problems += [line for line in blg.read_text(errors='replace').splitlines()
                     if re.search(r'\b(?:WARN|ERROR|FATAL) -', line)]
    if problems:
        raise ValueError('Publication checks failed:\n' + '\n'.join(problems))
    print('Publication checks passed: no overfull boxes or unresolved references/citations.')


def output(*args):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else None


def collect(root=ROOT):
    check(root)
    config = configuration(root)
    dist = root / 'dist'
    dist.mkdir(exist_ok=True)
    shutil.copyfile(root / 'build/main.pdf', dist / (config['id'] + '.pdf'))
    versions = {tool: output(tool, '--version') for tool in ('pdflatex', 'latexmk', 'biber')}
    metadata = {
        'publication': config,
        'commit': output('git', 'rev-parse', '--verify', 'HEAD'),
        'working_tree_dirty': bool(output('git', 'status', '--porcelain')),
        'source_date_epoch': os.environ.get('SOURCE_DATE_EPOCH'),
        'container_image': os.environ.get('NETSY_TEX_IMAGE'),
        'tools': {tool: version.splitlines()[0] if version else None
                  for tool, version in versions.items()},
    }
    (dist / 'provenance.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print('Checked PDF and provenance written to dist/.')


def package(tag, root=ROOT):
    config = configuration(root)
    release_tag(tag, config)
    dist = root / 'dist'
    pdf = dist / (config['id'] + '.pdf')
    if not pdf.is_file():
        raise ValueError('checked build artifact is missing')
    meta = json.loads((dist / 'provenance.json').read_text())
    if meta['commit'] != output('git', 'rev-parse', 'HEAD') or meta['working_tree_dirty']:
        raise ValueError('artifact must come from the same clean source commit')
    archive = dist / f'{config["id"]}-{tag}-sources.tar.gz'
    subprocess.run(['git', 'archive', '--format=tar.gz', f'--prefix={config["id"]}-{tag}/',
                    '-o', str(archive), 'HEAD'], cwd=root, check=True)
    paths = sorted(p for p in dist.iterdir() if p.is_file() and p.name != 'SHA256SUMS')
    sums = []
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        sums.append(f'{digest}  {path.name}\n')
    (dist / 'SHA256SUMS').write_text(''.join(sums))


def main():
    if len(sys.argv) < 2:
        raise ValueError('expected check, collect, release TAG or package TAG')
    command = sys.argv[1]
    if command == 'check':
        check()
    elif command == 'collect':
        collect()
    elif command == 'release' and len(sys.argv) == 3:
        release_tag(sys.argv[2], configuration())
    elif command == 'package' and len(sys.argv) == 3:
        package(sys.argv[2])
    else:
        raise ValueError('expected check, collect, release TAG or package TAG')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
