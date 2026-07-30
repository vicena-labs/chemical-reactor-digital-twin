import unittest
import numpy as np
from chemical_reactor_twin import ReactionNetwork, simulate_batch, simulate_cstr, simulate_pfr

class ReactorTests(unittest.TestCase):
    def setUp(self):
        self.net = ReactionNetwork(["A","B"], [[-1,1]], [5.0], [8000.0], [[1,0]], [-10000.0])
    def test_batch_conservation(self):
        r = simulate_batch(self.net, [1000,0], 320, 50, adiabatic=False, ua=1e6, coolant_temperature=320)
        np.testing.assert_allclose(r.concentration.sum(axis=1), 1000, rtol=2e-6, atol=1e-5)
    def test_zero_time_limit_via_short_time(self):
        r = simulate_batch(self.net, [1000,0], 320, 1e-9, adiabatic=True, n_points=2)
        np.testing.assert_allclose(r.concentration[0], r.concentration[-1], rtol=0, atol=1e-6)
    def test_no_reaction_limit(self):
        net = ReactionNetwork(["A","B"], [[-1,1]], [0.0], [0.0], [[1,0]], [0.0])
        r = simulate_pfr(net, [1000,0], 320, 100)
        np.testing.assert_allclose(r.concentration[-1], [1000,0], atol=1e-10)
    def test_cstr_mass_balance(self):
        r = simulate_cstr(self.net, [1000,0], 320, 20, adiabatic=True)
        self.assertLess(r.diagnostics["residual_norm"], 1e-5)
        self.assertAlmostEqual(float(r.concentration.sum()), 1000, places=4)
    def test_pfr_more_conversion_than_cstr_first_order(self):
        c = simulate_cstr(self.net, [1000,0], 320, 20, adiabatic=False, ua_over_volume=1e9, coolant_temperature=320)
        p = simulate_pfr(self.net, [1000,0], 320, 20, adiabatic=False, ua_over_volume=1e9, coolant_temperature=320)
        self.assertLess(p.concentration[-1,0], c.concentration[-1,0])
    def test_reject_negative_concentration(self):
        with self.assertRaises(ValueError):
            simulate_batch(self.net, [-1,0], 320, 10)

if __name__ == "__main__": unittest.main()
