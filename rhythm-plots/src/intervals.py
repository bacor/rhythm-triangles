import numpy as np
import os

CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CUR_DIR, os.path.pardir))


def report_intervals(intervals, title):
    pre = ">  "
    line = "—" * 30
    print(f"{title}\n{line}")
    print(f"{pre}Length      {len(intervals)}")
    print(f"{pre}NA count    {np.isnan(intervals).sum()}")
    print(f"{pre}Minimum     {np.min(intervals):.2e}s")
    print(f"{pre}Mean        {np.mean(intervals):.2e}s")
    print(f"{pre}Maximum     {np.max(intervals):.2e}s")
    print(f"{line}\n")


def save_intervals(intervals, group, name, report=False):
    if report:
        report_intervals(intervals, f"Saving {group}/{name}")
    path = os.path.join(ROOT_DIR, "intervals", group, f"{name}-intervals.txt")
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    np.savetxt(path, intervals)


def load_intervals(group, name):
    path = os.path.join(ROOT_DIR, "intervals", group, f"{name}-intervals.txt")
    return np.loadtxt(path)


def drop_na(x):
    return x[np.logical_not(np.isnan(x))]
