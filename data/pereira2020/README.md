Pereira *et al*. (2020)
=======================

- **Notebook:** [`pereira2020.ipynb`](../../notebooks/pereira2020.ipynb)
- **Paper:** Pereira, A. S., Kavanagh, E., Hobaiter, C., Slocombe, K. E., & Lameira, A. R. (2020). Chimpanzee lip-smacks confirm primate continuity for speech-rhythm evolution. *Biology Letters, 16*(5), 20200232. DOI: [10.1098/rsbl.2020.0232](https://doi.org/10.1098/rsbl.2020.0232).
- **Dataset**: available from the publisher via [https://royalsocietypublishing.org/doi/suppl/10.1098/rsbl.2020.0232](royalsocietypublishing.org/doi/suppl/10.1098/rsbl.2020.0232).
- **Dataset licence:** © 2020 The Author(s). Published by the Royal Society. All rights reserved.

-----

Data from this paper is available from the website of the publisher, but has not been included in this repository since it's not clear to me whether that would be allowed. After you downloaded those files you can use the [notebook](../../notebooks/pereira2020.ipynb) to generate the following two files which are used to make the rhythm plots:

`chimpanzee-lip-smack-data.csv` (not included)
-------------------------

A CSV file with all data from the original paper and the following columns:

- Origin
- Individual
- Bout number
- Bout peak
- Comments
- Standardized time series
- ys
- N
- duration
- intervals


`chimpanzee-lip-smack-intervals.txt` (not included)
----------------------------- 

A plain text file with one time interval on every line: this can be loaded directly with numpy's `np.loadtxt`.