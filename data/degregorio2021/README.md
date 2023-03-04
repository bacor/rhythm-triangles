De Gregorio *et al*., 2021
==========================

- **Paper:** De Gregorio, C., Valente, D., Raimondi, T., Torti, V., Miaretsoa, L., Friard, O., Giacoma, C., Ravignani, A., & Gamba, M. (2021). Categorical rhythms in a singing primate. Current Biology, 31(20), R1379–R1380. DOI: [10.1016/j.cub.2021.09.032](https://doi.org/10.1016/j.cub.2021.09.032)
- **Dataset:** Available from the first author upon request.
- **Dataset license:** Unknown; intervals have therefore not been included.

-------

Data from this paper is available from the first author upon request, but has not been included in this repository as the original data is not available online. The following files are needed for the analyses:

`degregorio2021-data.csv` (not included)
----------------------------------------

A clean CSV file with the data from the paper. It is generated from the original data file in the notebook [degregorio2021.ipynb](../../notebooks/degregorio2021.ipynb), and has the following columns:

- index
- start
- duration
- interval
- label
- id_song
- id_group
- id_contribution
- id_individual
- name_individual
- sex

`degregorio2021-intervals.txt` (not included)
-----------------------------

A plain text file with one time interval on every line: this can be loaded directly with numpy's `np.loadtxt`.