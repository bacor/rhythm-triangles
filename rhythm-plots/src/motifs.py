import numpy as np
from typing import Optional, Dict, List, Callable, Iterable, Union, Tuple


def split_at(array, value):
    """Split an array after every index where it contains `value`."""
    matches = np.isnan(array) if np.isnan(value) else array == value
    splitpoints = np.where(matches)[0] + 1
    if splitpoints[-1] == len(array):
        splitpoints = splitpoints[:-1]
    return np.array_split(array, splitpoints)


def split_at_nan(array, skip_empty=False):
    sections = []
    for section in split_at(array, np.nan):
        if np.isnan(section[-1]):
            section = section[:-1]
        if len(section) > 0 or not skip_empty:
            sections.append(section)
    return sections


def sliding_window(array, window):
    """Returns a matrix where every row corresponds to a window from the array"""
    if window > len(array):
        return np.array([])
    N = len(array) - window + 1
    repeated_windows = np.tile(np.arange(window), (N, 1))
    indices = repeated_windows + np.arange(N)[:, np.newaxis]
    return array[indices]


def ngram_motifs(data: np.array, length: int) -> np.array:
    """Create a matrix of ngram motifs from the data

    >>> ngram_motifs(np.array([1, 2, 3, 4, np.nan, 5, 6]), 2)
    array([[1., 2.],
       [2., 3.],
       [3., 4.],
       [5., 6.]])

    Parameters
    ----------
    data : np.array
        An iterable with data. np.nan values should indicate section endings,
        and no ngrams that cross section boundaries are included.
    length : int
        Length n of the n-gram

    Returns
    -------
    np.array
        A (num_motifs x n) array with motifs
    """
    data = np.array(data)
    if not np.isnan(data[-1]):
        data = np.r_[data, np.nan]

    sections = split_at_nan(data)
    motifs = []
    for section in sections:
        section_motifs = sliding_window(section, length)
        motifs.extend(section_motifs)
    return np.array(motifs)


def normalize(motifs):
    duration = motifs.sum(axis=1)
    motifs = motifs / duration[:, np.newaxis]
    return motifs, duration


def filter_motifs(motifs, duration, min_dur=0, max_dur=np.inf, limit=-1, shuffle=True):
    """Select a subset of motifs: select only those motifs whose
    duration is between the minimum and maximum duration (min_dur, max_ddur),
    limit to a certain number of motifs, and optionally shuffle the motifs.
    """
    match = (duration > min_dur) & (duration < max_dur)
    index = np.arange(len(motifs))[match]
    if limit == -1 or limit > len(index):
        limit = len(index)
    if shuffle:
        index = np.random.choice(index, size=limit, replace=False)
    else:
        index = index[:limit]
    return motifs[index, :], duration[index], index


def string_motifs(
    strings: Iterable[str],
    length: int,
    aggregator: Optional[Union[Dict, Callable]] = None,
    sep: Optional[str] = "-",
    return_motifs: Optional[bool] = False,
) -> Union[List[str], Tuple[List[str], List[List[str]]]]:
    """Generate motifs from categorical data, typically to produce labels for
    motifs. The motifs (ngrams of strings) are aggregated, for example by
    joining them using some separator.

    cats = ['a', 'b', 'c', 'd', 'e', np.nan, 'c', 'd', 'e', 'a']
    string_motifs(cats, length=3)
    >>> ['a-b-c', 'b-c-d', 'c-d-e', 'c-d-e', 'd-e-a']
    string_motifs(cats, 3, sep='')
    >>> ['abc', 'bcd', 'cde', 'cde', 'dea']
    string_motifs(cats, 3, aggregator=lambda motif: "".join([m.upper() for m in motif]))
    >>> ['ABC', 'BCD', 'CDE', 'CDE', 'DEA']
    string_motifs(cats, 3, aggregator=dict(a='A1', b='B2', c='C3', d='D4', e='E5'), sep="_")
    >>> ['A1_B2_C3', 'B2_C3_D4', 'C3_D4_E5', 'C3_D4_E5', 'D4_E5_A1']

    Parameters
    ----------
    strings : Iterable[str]
        Strings or something that can be turned into a string
    length : int
        The motif length
    aggregator : Optional[Union[Dict, Callable]], optional
        Something that produces a single string from a motif of strings.
        Can be a dictionary that maps elements in a motif to strings, which are
        then joined with a separator `sep`. Can also be a function that maps
        takes a motif as an input and outputs a string. The default is to join
        the parts of a motif by the separator sep.
    sep : Optional[str], optional
        The separator, not used if the labeler is a function, by default "-"
    return_motifs : Optional[bool], optional
        If true it returns both the aggregated strings and the string
        motifs, by default False

    Returns
    -------
    Union[List[str], Tuple[List[str], List[List[str]]]]
        The labels (aggregated strings) if return_motifs is False, otherwise both
        the labels and (unaggregated) string motifs
    """
    values = [c for c in set(strings) if type(c) is str or not np.isnan(c)]

    # Set up aggregator
    if aggregator is None:
        aggregator = {v: v for v in values}
    if type(aggregator) == dict:
        aggregator_map = aggregator
        aggregator = lambda motif: sep.join([aggregator_map[m] for m in motif])
    if not callable(aggregator):
        raise ValueError("Aggregator should be a dictionary or a callable")

    # First convert to indices, since otherwise the ngram_motis doesn't work.
    val2idx = {val: idx for idx, val in enumerate(values)}
    idx2val = {idx: val for val, idx in val2idx.items()}
    indices = [val2idx.get(val, np.nan) for val in strings]
    motifs = ngram_motifs(indices, length=length)

    # Convert back to categories and compute labels
    cat_motifs = [[idx2val.get(m, np.nan) for m in motif] for motif in motifs]
    labels = [aggregator(motif) for motif in cat_motifs]
    return (labels, cat_motifs) if return_motifs else labels


def separate_sequences(df, column='sequence'):
    import pandas as pd
    """Add empty rows between sequences in a dataframe"""
    data = []
    for seq in df[column].dropna().unique():
        sequence = df.query(f'{column}=="{seq}"').values
        sequence = np.r_[sequence, [[np.nan] * sequence.shape[1]]]
        data.extend(sequence)
    return pd.DataFrame(data, columns=df.columns)