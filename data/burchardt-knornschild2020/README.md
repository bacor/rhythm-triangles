Data for Burchardt and Knörnschild 2020
=======================================

- **Notebook:** [`burchardt-knornschild2020.ipynb`](../../notebooks/burchardt-knornschild2020.ipynb)
- **Paper:** Burchardt LS, Knörnschild M (2020) Comparison of methods for rhythm analysis of complex animals’ acoustic signals. *PLoS Computational Biology 16*(4): e1007755. DOI: [10.1371/journal.pcbi.1007755](https://doi.org/10.1371/journal.pcbi.1007755)
- **Dataset:** [DOI 10.1371/journal.pcbi.1007755.s006](https://doi.org/10.1371/journal.pcbi.1007755.s006)
- **Copyright:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/), © 2020 Burchardt, Knörnschild.

----

The authors provide an Excel file [pcbi.1007755.s006.xlsx](original-data/pcbi.1007755.s006.xlsx). I manually exported the three tables in the excel file to three csv files:

- [bat-carollia-perspicillata.csv](original-data/bat-carollia-perspicillata.csv) contains the table `IOI C.persp`
- [bat-saccopteryx-bilineata.csv](original-data/bat-saccopteryx-bilineata.csv) contains the table `IOI S.bil`
- [whale-physeter-macrocephalus.csv](original-data/whale-physeter-macrocephalus.csv) contains the table `IOI P .mac1`

These tables are further preprocessed in the notebook [burchardt-knornschild2020.ipynb](../../notebooks/burchardt-knornschild2020.ipynb) to produce the csv files in this directory, that are used in later analyses. See the notebook for more details.

- bat-carollia-perspicillata-data.csv
- bat-carollia-perspicillata-intervals.txt
- bat-saccopteryx-bilineata-data.csv
- bat-saccopteryx-bilineata-intervals.txt
- whale-physeter-macrocephalus-data.csv
- whale-physeter-macrocephalus-intervals.txt