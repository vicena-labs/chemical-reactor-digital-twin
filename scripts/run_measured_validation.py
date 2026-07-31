#!/usr/bin/env python3
import argparse
from chemical_reactor_twin.measured_validation import run_silica_validation
p=argparse.ArgumentParser(); p.add_argument("workbook"); p.add_argument("--output",default="outputs/measured_silica"); a=p.parse_args(); s=run_silica_validation(a.workbook,a.output); x=s["aggregate"]
print("Scientific status:",s["scientific_status"]); print("Experiments:",x["experiments"]); print("Median fourth-order RMSE:",round(x["median_fourth_order_rmse_normalized"],4)); print("Median first-order RMSE:",round(x["median_first_order_rmse_normalized"],4)); print("Fourth-order better:",x["fourth_order_better_count"],"/",x["experiments"]); print("Median interval coverage:",round(x["median_interval_coverage"],4))
