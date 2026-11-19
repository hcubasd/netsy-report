"""Scientific execution checks; run with the NetSy analysis environment."""
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0,'/workdir/netsy')
from tests.test_network import _loads,_trips
from complement_grades import terrain_grade
from path_cache import persistent_paths
from assess_case import float32_emissions
from netsy.synth.network_emissions import emissions_by_copert,emissions_by_factors
from tests.test_network import _csv,_network,_load_rows


class ExperimentControls(unittest.TestCase):
    def test_signed_nodes_and_unknown_fallback(self):
        grade,accepted=terrain_grade(np.array([0.,5.,0.,0.,np.nan]),
            np.array([5.,0.,9.,100.,1.]),np.array([100.,100.,20.,100.,100.]),np.ones(5,dtype=bool))
        np.testing.assert_array_equal(grade,[5,-5,0,0,0])
        np.testing.assert_array_equal(accepted,[True,True,False,False,False])

    def test_cached_assignment_is_identical_and_different_costs_do_not_reuse(self):
        trips=_trips([(7,'lorry',.5,1,3,'food'),(8,'van',.2,1,9,'parcels')])
        expected=_loads(trips)
        with tempfile.TemporaryDirectory() as tmp:
            with persistent_paths(tmp) as first:actual=_loads(trips)
            with persistent_paths(tmp) as second:reused=_loads(trips)
            pd.testing.assert_frame_equal(expected,actual)
            pd.testing.assert_frame_equal(expected,reused)
            self.assertGreater(first['computed'],0);self.assertEqual(second['computed'],0)
            self.assertGreater(second['reused'],0)
            changed_costs=_csv([('street','van',100)],['road_type','speed_class','cost'])
            expected_changed=_loads(trips,road_costs=changed_costs)
            with persistent_paths(tmp) as changed:actual_changed=_loads(trips,road_costs=changed_costs)
            pd.testing.assert_frame_equal(expected_changed,actual_changed)
            self.assertGreater(changed['computed'],0)

    def test_streaming_preserves_row_local_emission_results(self):
        loads=pd.concat([_load_rows(),_load_rows()],ignore_index=True)
        factors=_csv([('lorry','street','co2',100,300),('lorry','motorway','co2',150,350)],
                     ['vehicle','road_type','pollutant','empty','full'])
        types=_csv([('lorry','rigid')],['vehicle','vehicle_type'])
        coefficients=_csv([('rigid','co2',0,load,0,0,10+load,0,0,0,1,0) for load in [0,50,100]],
            ['vehicle_type','pollutant','gradient_bin','payload_bin','alpha','beta','gamma','delta','epsilon','zeta','eta','rf'])
        nonexhaust=_csv([],['vehicle_type','pollutant','emission_factor'])
        for function,extra in [(emissions_by_factors,[factors]),(emissions_by_copert,[types,coefficients,nonexhaust])]:
            full=float32_emissions(function(loads,_network(),*extra))[0].reset_index(drop=True)
            parts=[float32_emissions(function(loads.iloc[i:i+1],_network(),*extra))[0] for i in range(len(loads))]
            pd.testing.assert_frame_equal(full,pd.concat(parts,ignore_index=True))


if __name__=='__main__':unittest.main()
