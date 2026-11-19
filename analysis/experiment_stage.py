"""Run frozen NetSy CLI stages, serializing memory-heavy assignments."""
import fcntl
import json
import os
import sys
from pathlib import Path

from netsy.cli.main import main
from path_cache import persistent_paths

if __name__=='__main__':
    if 'network-loads' in sys.argv and os.environ.get('PAPER_PATH_CACHE'):
        cache=Path(os.environ['PAPER_PATH_CACHE']);cache.mkdir(exist_ok=True,parents=True)
        # Separate realization runners can assess emissions concurrently, but
        # national assignment finalization has a high transient memory peak.
        with (cache.parent/'assignment.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            with persistent_paths(cache) as stats:code=main(sys.argv[1:])
            Path('path-cache-stats.json').write_text(json.dumps(stats,indent=2)+'\n')
    else:code=main(sys.argv[1:])
    raise SystemExit(code)
