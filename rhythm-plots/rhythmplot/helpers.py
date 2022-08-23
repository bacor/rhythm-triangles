import numpy as np
import os
from typing import Optional, Callable
import matplotlib.pyplot as plt

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

def get_figure_saver(group: str, save_pdf: Optional[bool] = True, save_png: Optional[bool] = True, 
    dir: Optional[str] = 'figures', **default_kws) -> Callable:
    """Return a function that saves figures as pdf and/or png. This allows you
    to easily turn on/off figure exporting, and you can specify options globally"""
    dir_path = os.path.join(ROOT_DIR, dir, group)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    def savefig(name, **kws):
        _kws = dict(dpi=300, transparent=True)
        _kws.update(default_kws)
        _kws.update(kws)
        if save_pdf:
            plt.savefig(os.path.join(dir_path, f'{group}-{name}.pdf'), **_kws)
        if save_png:
            plt.savefig(os.path.join(dir_path, f'{group}-{name}.png'), **_kws)
        if not save_pdf and not save_png:
            print(
                'Note: to store the figure, enable save_pdf or save_png in '
                'get_figure_saver.'
            )

    return savefig



def defaults(kws, **default_kws):
    default_kws.update(kws)
    return default_kws


_corners = np.array([[0, 0], [1, 0], [0.5, 0.75**0.5]])
(x1, y1), (x2, y2), (x3, y3) = _corners
_T = np.array([[0 - x3, x2 - x3], [y1 - y3, y2 - y3]])
_T_inv = np.linalg.inv(_T)

def  xy2bc(X):
    diff = X - _corners[-1][np.newaxis, :]
    lamb = np.zeros((X.shape[0], 3))
    lamb[:, :2] =  _T_inv.dot(diff.T).T
    lamb[:, 2] = 1 - lamb[:, 0] - lamb[:, 1]
    return lamb

def uniform_subsample_triangle(limit, margin=0):
    X = np.random.rand(limit, 2)
    samples = xy2bc(X)
    all_positive = (samples >= 0).all(axis=1)
    within_margin = samples.min(axis=1) > margin
    return samples[all_positive & within_margin]