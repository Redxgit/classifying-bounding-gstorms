# classifying-bounding-gstorms

Repository for the paper Classifying and bounding geomagnetic storms based on the SYM-H and ASY-H indices

Required packages in requirements.txt

The data can be downloaded using ``python download_data.py`` and will create a pickle file in the data folder ``sym_asy_indices.pkl`` for the SYM-H and ASY-H indices and another pickle ``dst_index.pkl`` for the Dst data.

The data will be downloaded from the CDAWeb, the SYM and ASY indices will be downloaded from the ``OMNI_HRO_5MIN`` dataset with a 5 minute resolution. The data will be downloaded from 1981 until the end of 2022.

The repository contains 7 notebooks

* ``1-Distribution.ipynb``: Contains the calculations to resample the indices time-series, calculate the autocorrelation and perform CDF of each index using the selected percentiles to establish the thresholds for each class.

* ``2a-Storms-SYM-superposed.ipynb`` and ``2b-Storms-ASY-superposed.ipynb``: Contains the superposed epoch analysis for the SYM and ASY indices, the storms are selected and classified based on the thresholds calculated on the previous notebook and 5 days are selected before and after the peak value of each storm. Then, storms from the same class are averaged using the peak value of the index as the 0 epoch.

* ``3a-Find-Storms-SYM.ipynb`` and ``3b-Find-Storms-SYM.ipynb``: Identifies, classifies and plots the storms using the thresholds calculated in the distribution notebook. The selected bounds for each storms is 2 complete days before the first value in the low-intensity range until 4 complete days after the last one.

* ``4a-Particular-storms-SYM.ipynb`` and ``4b-Particular-storms-SYM.ipynb``: Plots particular storms, shading the area surrounding the peak in green for the initial phase and in blue for the recovery phase, following the flowchart of the paper.

There is also four .csv files in the data folder:

* ``dates_sym_superposed.csv`` and ``dates_asy_superposed.csv``: Contains storms used to perform the superposed epoch analysis. For each storm we save the start and end dates used for the superposed epoch plot, the peak value of the index and the classification of the storm.

* ``storm_sym.csv`` and ``storm_asy.csv``: Contains the identified and classified storms for each index.  For each storm we save the start date, end date, duration of the storm, the peak value of the index and the classification of the storm.
