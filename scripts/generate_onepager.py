"""Generate the A4 landscape one-page visual from executable synthetic results."""
from pathlib import Path
import sys
sys.path.insert(0, "src")
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from chemical_reactor_twin import ReactionNetwork, simulate_batch, simulate_cstr, simulate_pfr

net = ReactionNetwork(["A","B","C"], [[-1,1,0],[-1,0,1]], [20,2], [12000,15000],
                      [[1,0,0],[1,0,0]], [-20000,-30000])
feed = np.array([1000.,0.,0.])
b = simulate_batch(net, feed, 330, 120, volume=0.001, ua=25, coolant_temperature=330)
taus = np.linspace(5,100,20)
xc, xp = [], []
for tau in taus:
    c = simulate_cstr(net, feed, 330, tau, ua_over_volume=25000, coolant_temperature=330)
    p = simulate_pfr(net, feed, 330, tau, ua_over_volume=25000, coolant_temperature=330)
    xc.append(1-c.concentration[-1,0]/1000); xp.append(1-p.concentration[-1,0]/1000)
ms=json.loads(Path("outputs/measured_silica/summary.json").read_text())
mm=pd.read_csv("outputs/measured_silica/per_experiment_metrics.csv")
conv = 1-b.concentration[-1,0]/1000
sel = b.concentration[-1,1]/(b.concentration[-1,1]+b.concentration[-1,2])
fig = plt.figure(figsize=(11.69,8.27), facecolor="#f5f7fa")
gs = fig.add_gridspec(4, 4, height_ratios=[0.75,1.0,2.3,0.8], hspace=.55, wspace=.45)
ax = fig.add_subplot(gs[0,:]); ax.axis("off"); ax.set_facecolor("#13233a")
ax.add_patch(plt.Rectangle((0,0),1,1,transform=ax.transAxes,color="#13233a"))
ax.text(.03,.63,"CHEMICAL REACTOR DIGITAL TWIN",color="white",fontsize=22,weight="bold")
ax.text(.03,.22,"Measured silica kinetics benchmark | Open source MIT | vicena.ai",color="#c8d7ea",fontsize=11)
cards = ["Batch, CSTR, PFR","61 measured experiments","Fourth vs first order","Explicit failure boundary"]
for i,t in enumerate(cards):
    a=fig.add_subplot(gs[1,i]); a.axis("off"); a.add_patch(plt.Rectangle((0,0),1,1,transform=a.transAxes,color="white",ec="#cad3df"))
    a.text(.5,.63,t,ha="center",va="center",weight="bold",fontsize=10,color="#13233a")
    a.text(.5,.25,["Mass + energy balances","Time-split validation","44.42% median RMSE gain","Coverage only 0.10"][i],ha="center",fontsize=8,color="#4b5b6b")
a=fig.add_subplot(gs[2,:2]); a.plot(b.coordinate,b.concentration[:,0],label="A"); a.plot(b.coordinate,b.concentration[:,1],label="B"); a.plot(b.coordinate,b.concentration[:,2],label="C"); a.set(xlabel="Time (s)",ylabel="Concentration (mol/m3)",title="Synthetic batch trajectory"); a.legend(); a.grid(alpha=.25)
a=fig.add_subplot(gs[2,2:]); a.scatter(mm.baseline_rmse_normalized,mm.model_rmse_normalized,c=mm.temperature_c,cmap="plasma",s=28); lm=max(mm.baseline_rmse_normalized.max(),mm.model_rmse_normalized.max()); a.plot([0,lm],[0,lm],"--",color="0.35"); a.set(xlabel="First-order test RMSE",ylabel="Fourth-order test RMSE",title="Measured late-time extrapolation"); a.grid(alpha=.25)
a=fig.add_subplot(gs[3,:]); a.axis("off"); a.add_patch(plt.Rectangle((0,0),1,1,transform=a.transAxes,color="#13233a"))
metrics=f"Measured: 61 experiments | median fourth-order RMSE {ms['aggregate']['median_fourth_order_rmse_normalized']:.3f} | first-order {ms['aggregate']['median_first_order_rmse_normalized']:.3f} | coverage {ms['aggregate']['median_interval_coverage']:.2f}"
a.text(.5,.68,metrics,ha="center",color="white",weight="bold",fontsize=10)
a.text(.5,.27,"1 Validate data  |  2 Simulate  |  3 Calibrate  |  4 Hold-out validate  |  5 Analyze and optimize safely",ha="center",color="#c8d7ea",fontsize=9)
fig.suptitle("Measured benchmark with failed interval coverage, not a predictive, safety, or scale-up signoff",y=.01,fontsize=9,color="#8a2530")
Path("assets").mkdir(exist_ok=True)
fig.savefig("assets/chemical-reactor-digital-twin-onepager.png",dpi=180,bbox_inches="tight")
fig.savefig("Chemical_Reactor_Digital_Twin_OnePager.pdf",bbox_inches="tight")
print("conversion",conv); print("selectivity_B",sel); print("peak_temperature_K",float(b.temperature.max()))
