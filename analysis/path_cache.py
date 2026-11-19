"""Execution-only cache for NetSy's origin-wise Dijkstra predecessor arrays.

The frozen assignment uses only predecessors. Hash the exact sparse graph,
ordering, precision and SciPy version; never reuse a path for a different cost.
"""
from contextlib import contextmanager
import hashlib
import importlib
import os
from pathlib import Path

import numpy as np
import scipy


@contextmanager
def persistent_paths(directory):
    module=importlib.import_module('netsy.synth.network_loads')
    original=module.dijkstra;directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    stats={'computed':0,'reused':0}
    def cached(graph, indices, return_predecessors):
        assert np.isscalar(indices) and return_predecessors is True
        if not hasattr(graph,'_paper_path_key'):
            digest=hashlib.sha256(('netsy-0.5.0|'+scipy.__version__+'|'+str(graph.shape)).encode())
            for array in [graph.indptr,graph.indices,graph.data]:
                digest.update(array.dtype.str.encode());digest.update(array.tobytes())
            graph._paper_path_key=digest.hexdigest()
        folder=directory/graph._paper_path_key;folder.mkdir(exist_ok=True)
        path=folder/f'{int(indices)}.npy'
        if path.exists():
            stats['reused']+=1
            return None,np.load(path,allow_pickle=False)
        result=original(graph,indices=indices,return_predecessors=True)
        temp=path.with_suffix(f'.{os.getpid()}.tmp.npy');np.save(temp,result[1],allow_pickle=False);temp.replace(path)
        stats['computed']+=1
        return result
    module.dijkstra=cached
    try:yield stats
    finally:module.dijkstra=original
