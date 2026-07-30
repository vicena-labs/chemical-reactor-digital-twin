"""Built with Vicena. Run transparent batch, CSTR, and PFR reference cases."""
import json
import numpy as np
from chemical_reactor_twin import ReactionNetwork, simulate_batch, simulate_cstr, simulate_pfr

net = ReactionNetwork(["A","B","C"], [[-1,1,0],[-1,0,1]], [20,2], [12000,15000],
                      [[1,0,0],[1,0,0]], [-20000,-30000])
feed = np.array([1000.0,0.0,0.0])
batch = simulate_batch(net, feed, 330, 120, volume=0.001, ua=25, coolant_temperature=330)
cstr = simulate_cstr(net, feed, 330, 60, ua_over_volume=25000, coolant_temperature=330)
pfr = simulate_pfr(net, feed, 330, 60, ua_over_volume=25000, coolant_temperature=330)
summary = {}
for name, result in [("batch",batch),("cstr",cstr),("pfr",pfr)]:
    conversion = 1 - result.concentration[-1,0]/feed[0]
    selectivity = result.concentration[-1,1] / max(result.concentration[-1,1]+result.concentration[-1,2],1e-12)
    summary[name] = {"conversion": float(conversion), "selectivity_B": float(selectivity),
                     "outlet_temperature_K": float(result.temperature[-1]), "diagnostics": result.diagnostics}
print(json.dumps(summary, indent=2))
