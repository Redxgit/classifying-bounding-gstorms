from cdasws import CdasWs
from cdasws.datarepresentation import DataRepresentation as dr
import numpy as np
import pandas as pd

if __name__ == "__main__":
    cdas = (
        CdasWs()
    )  # Create an instance of the CdasWs class to download the CDAWeb data

    # Define start and end dates for data retrieval, needs to be in UTC for the cdasws library
    start_date_sym_asy = pd.to_datetime("1981-01-01", utc=True)
    end_date = pd.to_datetime("2023-01-01", utc=True)

    # Print information about the data to be downloaded
    print(
        f"Downloading SYM-H and ASY-H data from {start_date_sym_asy} until {end_date}"
    )
    print(
        f"Data will be downloaded from the 'OMNI_HRO_5MIN' dataset with a 5 minute resolution"
    )

    # Get data from the specified dataset and variables within the specified time range
    # we use the XARRAY format to minimize dependencies
    status, data = cdas.get_data(
        "OMNI_HRO_5MIN",
        ["SYM_H", "ASY_H"],
        start_date_sym_asy,
        end_date,
        dataRepresentation=dr.XARRAY,
    )

    # Process the retrieved data and create a DataFrame
    sym_asy = pd.DataFrame(data=data["Epoch"], columns=["datetime"])
    sym_asy["datetime"] = pd.to_datetime(sym_asy["datetime"])
    sym_asy["SYM_H"] = data["SYM_H"].values
    sym_asy["ASY_H"] = data["ASY_H"].values
    sym_asy = sym_asy.set_index("datetime")
    # Remove the UTC formatting to ease the use
    sym_asy.index = sym_asy.index.tz_localize(None)
    sym_asy["SYM_H"] = sym_asy["SYM_H"].replace(99999, np.nan)
    sym_asy["ASY_H"] = sym_asy["ASY_H"].replace(99999, np.nan)

    print(f"Saving data to sym_asy_indices.pkl")

    # Save the DataFrame to a pickle file with gzip compression
    sym_asy.to_pickle("./sym_asy_indices.pkl", compression="gzip")
