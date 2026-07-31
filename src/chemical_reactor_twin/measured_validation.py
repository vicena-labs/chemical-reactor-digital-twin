"""Measured silica-polymerization kinetics validation."""
from dataclasses import dataclass,asdict
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.optimize import least_squares

@dataclass(frozen=True)
class TimeSplit:
    train:float=.60
    calibration:float=.20
    test:float=.20

def load_silica_workbook(path):
    raw=pd.read_excel(path,sheet_name=0,header=None); experiments=[]; raw_pairs=0
    for col in range(0,raw.shape[1],3):
        if col+1>=raw.shape[1]: continue
        try:
            name=str(raw.iat[0,col+1]); temp=float(raw.iat[1,col+1]); ph=float(raw.iat[2,col+1]); ionic=float(raw.iat[3,col+1])
        except (TypeError,ValueError): continue
        t=pd.to_numeric(raw.iloc[6:,col],errors="coerce"); c=pd.to_numeric(raw.iloc[6:,col+1],errors="coerce"); raw_pairs+=len(t)
        d=pd.DataFrame({"time_min":t,"silica_mmol_kg":c}).dropna(); d=d[(d.time_min>=0)&(d.silica_mmol_kg>0)].sort_values("time_min").drop_duplicates("time_min")
        if len(d)<8: continue
        d["experiment_id"]=f"{name}_column_{col}"; d["source_experiment"]=name; d["temperature_c"]=temp; d["ph"]=ph; d["ionic_strength_mol_kg"]=ionic; d["normalized_silica"]=d.silica_mmol_kg/float(d.silica_mmol_kg.iloc[0]); experiments.append(d)
    if not experiments: raise ValueError("No experiments with at least eight valid observations")
    out=pd.concat(experiments,ignore_index=True); return out,{"workbook_slots":int(raw_pairs),"accepted_observations":int(len(out)),"experiments":int(out.experiment_id.nunique()),"quality_gate":"numeric time >= 0 min, silica > 0 mmol/kg, unique time, at least 8 observations per experiment"}

def fourth_order(t,k): return np.power(1+3*k*np.asarray(t,float),-1/3)
def first_order(t,k): return np.exp(-k*np.asarray(t,float))
def metrics(o,p):
    o=np.asarray(o,float); p=np.asarray(p,float); e=p-o; ss=np.sum((o-o.mean())**2)
    return {"n":int(len(o)),"mae_normalized":float(np.mean(abs(e))),"rmse_normalized":float(np.sqrt(np.mean(e*e))),"bias_normalized":float(np.mean(e)),"r2":float(1-np.sum(e*e)/ss) if ss else float("nan")}

def _fit_experiment(g,split=TimeSplit()):
    g=g.sort_values("time_min"); n=len(g); a=max(4,int(n*split.train)); b=max(a+2,int(n*(split.train+split.calibration))); train=g.iloc[:a]; cal=g.iloc[a:b]; test=g.iloc[b:]
    if min(len(cal),len(test))<1: raise ValueError("Insufficient calibration or test observations")
    k4=float(least_squares(lambda x:fourth_order(train.time_min,x[0])-train.normalized_silica,[1e-4],bounds=(0,np.inf)).x[0]); k1=float(least_squares(lambda x:first_order(train.time_min,x[0])-train.normalized_silica,[1e-3],bounds=(0,np.inf)).x[0]); cp=fourth_order(cal.time_min,k4); p4=fourth_order(test.time_min,k4); p1=first_order(test.time_min,k1); q=float(np.quantile(np.abs(cal.normalized_silica.to_numpy()-cp),.90,method="higher")); pred=test[["experiment_id","source_experiment","temperature_c","ph","ionic_strength_mol_kg","time_min","silica_mmol_kg","normalized_silica"]].copy(); pred["fourth_order_prediction"]=p4; pred["first_order_baseline"]=p1; pred["lower_90"]=np.clip(p4-q,0,np.inf); pred["upper_90"]=p4+q; coverage=float(np.mean((pred.normalized_silica>=pred.lower_90)&(pred.normalized_silica<=pred.upper_90))); summary={"experiment_id":str(g.experiment_id.iloc[0]),"source_experiment":str(g.source_experiment.iloc[0]),"temperature_c":float(g.temperature_c.iloc[0]),"ph":float(g.ph.iloc[0]),"ionic_strength_mol_kg":float(g.ionic_strength_mol_kg.iloc[0]),"rows":{"train":len(train),"calibration":len(cal),"test":len(test)},"fitted":{"normalized_fourth_order_k_per_min":k4,"first_order_k_per_min":k1},"fourth_order":metrics(pred.normalized_silica,pred.fourth_order_prediction),"first_order_baseline":metrics(pred.normalized_silica,pred.first_order_baseline),"absolute_residual_90_normalized":q,"empirical_interval_coverage":coverage}; return summary,pred

def run_silica_validation(path,output):
    data,quality=load_silica_workbook(path); summaries=[]; predictions=[]
    for _,g in data.groupby("experiment_id",sort=True): s,p=_fit_experiment(g); summaries.append(s); predictions.append(p)
    table=pd.DataFrame([{"experiment_id":s["experiment_id"],"temperature_c":s["temperature_c"],"ph":s["ph"],"ionic_strength_mol_kg":s["ionic_strength_mol_kg"],**{f"model_{k}":v for k,v in s["fourth_order"].items()},**{f"baseline_{k}":v for k,v in s["first_order_baseline"].items()},"interval_coverage":s["empirical_interval_coverage"]} for s in summaries]); out=Path(output); out.mkdir(parents=True,exist_ok=True); table.to_csv(out/"per_experiment_metrics.csv",index=False); pd.concat(predictions,ignore_index=True).to_csv(out/"test_predictions.csv",index=False)
    result={"scientific_status":"Measured-data Level 1 evidence for within-experiment silica polymerization time extrapolation","claim_boundary":"Does not validate a universal mechanism, cross-condition prediction, reactor scale-up, heat release, transport, or process safety","dataset":{"name":"Silica polymerization experimental data","doi":"10.5281/zenodo.8324851","raw_sha256":"6e8d65f177305e1bc95b5effb2124bc1f32af94422a66454c1918bf3785226dc"},"split_fractions":asdict(TimeSplit()),"quality":quality,"aggregate":{"experiments":len(table),"median_fourth_order_rmse_normalized":float(table.model_rmse_normalized.median()),"median_first_order_rmse_normalized":float(table.baseline_rmse_normalized.median()),"fourth_order_better_count":int((table.model_rmse_normalized<table.baseline_rmse_normalized).sum()),"median_fourth_order_r2":float(table.model_r2.median()),"median_interval_coverage":float(table.interval_coverage.median())},"per_experiment":summaries}; (out/"summary.json").write_text(json.dumps(result,indent=2)+"\n"); return result
