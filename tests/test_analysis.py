import unittest
import numpy as np
from chemical_reactor_twin.analysis import validate_prediction, local_sensitivity
from chemical_reactor_twin.calibration import identifiability_report

class AnalysisTests(unittest.TestCase):
    def test_validation_exact(self):
        m = validate_prediction([1,2],[1,2])
        self.assertEqual(m["rmse"], 0.0)
    def test_sensitivity(self):
        s = local_sensitivity(lambda p: [p["x"]**2], {"x": 3.0})
        self.assertAlmostEqual(float(s["derivatives"]["x"][0]), 6.0, places=5)
    def test_identifiability_rank_deficient(self):
        r = identifiability_report(np.ones((5,2)))
        self.assertFalse(r["locally_identifiable"])

if __name__ == "__main__": unittest.main()
