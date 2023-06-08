# classifying-bounding-gstorms

Repository for the paper Classifying and bounding geomagnetic storms based on the SYM-H and ASY-H indices

Required packages in requirements.txt

The data can be downloaded using

```python
python download_data.py
```

The data will be downloaded from the CDAWeb, the SYM and ASY indices will be downloaded from the ``OMNI_HRO_5MIN`` dataset with a 5 minute resolution. The data will be downloaded from 1981 until the end of 2022.

The repository contains 5 notebooks

* ``Distribution.ipynb``: Contains the calculations to resample the indices time-series, calculate the autocorrelation and perform CDF of each index using the selected percentiles to establish the thresholds for each class.

* ``Storms-SYM-superposed.ipynb`` and ``Storms-ASY-superposed.ipynb``: Contains the superposed epoch analysis for the SYM and ASY indices, the storms are selected and classified based on the thresholds calculated on the previous notebook and 5 days are selected before and after the peak value of each storm. Then, storms from the same class are averaged using the peak value of the index as the 0 epoch.

* ``Find-Storms-SYM.ipynb`` and ``Find-Storms-SYM.ipynb``: Identifies, classifies and plots the storms using the thresholds calculated in the distribution notebook. The selected bounds for each storms is 2 complete days before the first value in the low-intensity range until 4 complete days after.

There is also four .csv files:

* ``dates_sym_superposed.csv`` and ``dates_asy_superposed.csv``: Contains storms used to perform the superposed epoch analysis. For each storm we save the start and end dates used for the superposed epoch plot, the peak value of the index and the classification of the storm.

* ``storm_sym.csv`` and ``storm_asy.csv``: Contains the identified and classified storms for each index.  For each storm we save the start date, end date, duration of the storm, the peak value of the index and the classification of the storm.
