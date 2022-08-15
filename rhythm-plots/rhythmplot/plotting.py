import numpy as np
from pandas import value_counts
import matplotlib.pyplot as plt
import ternary
from matplotlib.colors import Normalize
from matplotlib.colors import BoundaryNorm
from matplotlib.cm import ScalarMappable
from matplotlib.ticker import FuncFormatter

from .motifs import filter_motifs
from .helpers import defaults
from typing import Optional, Dict, List, Iterable, Union, Tuple


def rhythm_plot(
    scale,
    subdiv=1,
    grid=False,
    ax=None,
    boundary=True,
    dpi=None,
    labels=True,
    bottom_label="interval 1",
    right_label="interval 2",
    left_label="interval 3",
    bottom_label_offset=-0.025,
    right_label_offset=0.05,
    left_label_offset=0.05,
    label_kws={},
    grid_kws={},
    boundary_kws={},
):
    # Default arguments
    if ax is None:
        ax = plt.gca()
    kws = dict(linestyle=":")
    grid_kws = defaults(
        grid_kws,
        color="k",
        linewidth=0.5,
        left_kwargs=kws,
        right_kwargs=kws,
        horizontal_kwargs=kws,
    )
    boundary_kws = defaults(boundary_kws, linewidth=0.5)

    # Set up figure
    figure, tax = ternary.figure(scale=scale, ax=ax)
    multiple = scale / subdiv
    ax.axis("equal")
    ax.set_axis_off()

    # Decorate
    if dpi is not None:
        figure.dpi = 150
    if boundary:
        tax.boundary(**boundary_kws)
    if grid:
        tax.gridlines(multiple=multiple, **grid_kws)
    if subdiv > 1:
        ticks = [f"{x:.2f}" for x in np.linspace(0, 1, subdiv + 1)]
        tax.ticks(
            axis="lbr", multiple=multiple, offset=0.02, lw=0.5, ticks=ticks, fontsize=6
        )
        label_offset += 0.1
    if not labels:
        tax.bottom_axis_label('')
        tax.right_axis_label('')
        tax.left_axis_label('')
    else:
        if bottom_label:
            tax.bottom_axis_label(
                bottom_label, **defaults(label_kws, offset=bottom_label_offset, fontsize=7)
            )
        if right_label:
            tax.right_axis_label(
                right_label, **defaults(label_kws, offset=right_label_offset, fontsize=7)
            )
        if left_label:
            tax.left_axis_label(
                left_label, **defaults(label_kws, offset=left_label_offset, fontsize=7)
            )

    return figure, tax


def show_integer_ratios(tax, scale, factors=[1, 2, 3], color="k"):
    from itertools import product

    points = dict()
    for a, b, c in product(factors, factors, factors):
        total = a + b + c
        point = (a / total, b / total, c / total)
        if point not in points.keys():
            points[point] = (a, b, c)

    for point, (a, b, c) in points.items():
        point = np.array(point) * scale
        tax.scatter([point], marker="+", s=8, color=color, linewidth=0.25)
        tax.annotate(
            f"{a}{b}{c}",
            point,
            color=color,
            ha="center",
            va="bottom",
            fontsize=4.5,
            xytext=(0, 1),
            textcoords="offset points",
        )


def ternary_motif_plot(
    motifs: np.array,
    duration: np.array,
    min_dur: Optional[float] = None,
    max_dur: Optional[float] = None,
    dur_quantile: Optional[Tuple[float]] = (0.1, 0.8),
    limit: Optional[int] = 30000,
    jitter: Optional[float] = 0,
    scale: Optional[int] = 60,
    labels: Optional[Iterable[str]] = None,
    label_order: Optional[Iterable[str]] = None,
    c: Optional[Iterable] = None,
    cmap=None,
    cbar: Optional[bool] = True,
    norm=None,
    cbar_kws: Optional[Dict] = {},
    ratios: Optional[bool] = True,
    ratio_kws: Optional[Dict] = {},
    ax=None,
    plot_kws: Optional[Dict] = {},
    scatter_kws: Optional[Dict] = {},
):
    # Default parameters
    if not len(motifs) == len(duration):
        raise ValueError("Motifs and durations should be equally long")
    if ax is None:
        ax = plt.gca()
    if min_dur is None:
        min_dur = np.quantile(duration, dur_quantile[0])
    if max_dur is None:
        max_dur = np.quantile(duration, dur_quantile[1])

    # Determine colors and colormap depending on whether labels were passed
    if labels is None:
        cmap = "plasma_r" if cmap is None else cmap
        if c is None:
            colors = duration
            if norm is None:
                norm = Normalize(vmin=min_dur, vmax=max_dur)
        elif type(c) == str:
            colors = np.array([c] * len(motifs))
        else:
            colors = np.array(c)

    else:
        if not len(labels) == len(motifs):
            raise ValueError("Motifs and labels should be equally long")
        if label_order is None:
            label_order = value_counts(labels).index
        n_labels = len(label_order)
        idx2label = {idx: label for idx, label in enumerate(label_order)}
        label2idx = {label: idx for idx, label in idx2label.items()}
        colors = np.array([label2idx[label] for label in labels])
        cmap = "tab10" if cmap is None else cmap
        norm = BoundaryNorm(np.arange(-0.5, n_labels + 0.5), n_labels)

    # Filter the motifs
    X, _, idx = filter_motifs(
        motifs, duration, min_dur=min_dur, max_dur=max_dur, limit=limit
    )
    if jitter > 0:
        X += np.random.normal(0, jitter, size=X.shape)

    # Plot
    fig, tax = rhythm_plot(scale, **defaults(plot_kws, subdiv=1, dpi=150, ax=ax))
    tax.scatter(
        X * scale,
        c=colors[idx],
        vmin=None,
        vmax=None,  # Passed via norm
        norm=norm,
        cmap=cmap,
        **defaults(scatter_kws, s=1, alpha=0.3, lw=0),
    )

    if cbar:
        if labels is not None:
            _cbar_kws = dict(
                label="label",
                ticks=np.arange(0, n_labels),
                format=FuncFormatter(lambda x, pos: idx2label[int(pos)]),
                orientation='vertical'
            )
        else:
            _cbar_kws = dict(label="duration (s)", orientation='horizontal')

        if 'orientation' in cbar_kws:
            _cbar_kws['orientation'] = cbar_kws['orientation']
        if _cbar_kws['orientation'] == 'horizontal':
            _cbar_kws.update(pad=0.03, fraction=0.047 / 3*2)
        else:
            _cbar_kws.update(pad=-0.1, fraction=0.02)
        
        fontsize = cbar_kws.pop('fontsize', 7)
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        cbar = fig.colorbar(mappable, ax=ax, **defaults(
            cbar_kws, 
            **_cbar_kws
        ))
        cbar.ax.tick_params(labelsize=fontsize)
        cbar.set_label(cbar._label, size=fontsize)


    if ratios:
        show_integer_ratios(tax, scale, **defaults(ratio_kws, factors=[1, 2, 3]))

    if cbar:
        return fig, tax, cbar
    else:
        return fig, tax
