"""Built with Vicena. Generate a safe, abstract A to B or C dataset."""
from pathlib import Path
import numpy as np
import pandas as pd
from chemical_reactor_twin import ReactionNetwork, simulate_batch

net = ReactionNetwork(["A","B","C"], [[-1,1,0],[-1,0,1]], [20,2], [12000,15000],
                      [[1,0,0],[1,0,0]], [-20000,-30000])
r = simulate_batch(net, [1000,0,0], 330, 120, volume=0.001, ua=25,
                   coolant_temperature=330, n_points=61)
rng = np.random.default_rng(42)
df = pd.DataFrame({"time_s": r.coordinate,
                   "A_mol_m3": np.clip(r.concentration[:,0] + rng.normal(0,2,len(r.coordinate)), 0, None),
                   "B_mol_m3": np.clip(r.concentration[:,1] + rng.normal(0,2,len(r.coordinate)), 0, None),
                   "temperature_K": r.temperature + rng.normal(0,0.03,len(r.coordinate))})
path = Path("datasets/synthetic/batch_concentration.csv")
df.to_csv(path, index=False)
print(path, len(df), float(df.A_mol_m3.iloc[-1]), float(df.temperature_K.max()))
