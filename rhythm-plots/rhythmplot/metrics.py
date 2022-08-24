import numpy as np

from .motifs import normalize, ngram_motifs
from .motifs import integer_ratio_motifs



def anisochrony(motifs):
    length = motifs.shape[1]
    isochronous_motif = np.repeat(1 / length, length)
    diff = motifs - isochronous_motif[np.newaxis, :]
    anisochronies = np.linalg.norm(diff, ord=1, axis=1)
    constant = length / (2*length - 2)
    return constant * anisochronies

def MA(intervals, order=2):
    motifs, _ = normalize(ngram_motifs(intervals, length=order))
    return np.mean(anisochrony(motifs))

def nPVI(intervals):
    return 200 * MA(intervals, order=2)

def orig_nPVI(intervals):
    terms = (intervals[:-1] - intervals[1:]) / ((intervals[:-1] + intervals[1:])/2)
    return 100 * np.mean(np.abs(terms))


# TODO normalize to give corners unit distance?
def irrationality(motifs, factors=[1, 2, 3]):
    length = 3
    refs, _ = integer_ratio_motifs(factors, motifs.shape[1])
    distances = np.zeros((motifs.shape[0], len(refs)))
    for i, reference in enumerate(refs):
        diff = motifs - reference[np.newaxis, :]
        dist = np.linalg.norm(diff, ord=2, axis=1)
        distances[:, i] = dist
    constant = length / (2*length - 2)
    return constant * distances.min(axis=1)