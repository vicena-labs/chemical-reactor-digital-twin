import numpy as np
from chemical_reactor_twin.measured_validation import fourth_order,first_order,metrics

def test_fourth_order_initial_and_monotone():
 p=fourth_order([0,1,10],.1); assert p[0]==1 and np.all(np.diff(p)<0)
def test_first_order_initial_and_monotone():
 p=first_order([0,1,10],.1); assert p[0]==1 and np.all(np.diff(p)<0)
def test_fourth_order_slower_tail(): assert fourth_order([100],.1)[0]>first_order([100],.1)[0]
def test_exact_metrics(): assert metrics([1,.5],[1,.5])["rmse_normalized"]==0
