import numpy as np
from chemical_reactor_twin import ReactionNetwork, simulate_batch
net = ReactionNetwork(["A","B"], [[-1,1]], [10.0], [10000.0], [[1,0]], [-15000.0])
r = simulate_batch(net, [1000,0], 325, 60, adiabatic=True)
print("conversion", 1-r.concentration[-1,0]/1000)
print("maximum temperature K", r.temperature.max())
print("solver diagnostics", r.diagnostics)
