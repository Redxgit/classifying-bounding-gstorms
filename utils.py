import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

# ASY-H thresholds for storm intensity levels
ASY_H_THRESHOLD_LOW = 130
ASY_H_THRESHOLD_MODERATE = 170
ASY_H_THRESHOLD_INTENSE = 290
ASY_H_THRESHOLD_SUPERINTENSE = 540

# SYM-H thresholds for storm intensity levels
SYM_H_THRESHOLD_LOW = -90
SYM_H_THRESHOLD_MODERATE = -130
SYM_H_THRESHOLD_INTENSE = -230
SYM_H_THRESHOLD_SUPERINTENSE = -390

# Number of days before and after an index peak for superposed epoch analysis
SUPERPOSED_DAYS_BEFORE = 5
SUPERPOSED_DAYS_AFTER = 5
SUPERPOSED_OFFSET_DAYS_BEFORE = pd.Timedelta(days=SUPERPOSED_DAYS_BEFORE)
SUPERPOSED_OFFSET_DAYS_AFTER = pd.Timedelta(days=SUPERPOSED_DAYS_AFTER)

# Colors for different storm intensity levels
COLOR_SUPERINTENSE = "darkmagenta"
COLOR_INTENSE = "firebrick"
COLOR_MODERATE = "goldenrod"
COLOR_LOW = "yellow"
COLOR_INACTIVE = "olivedrab"

# Number of days before and after a storm for storm analysis
STORM_DAYS_BEFORE = 2
STORM_DAYS_AFTER = 4
STORM_DAYS_BEFORE_OFFSET = pd.Timedelta(days=STORM_DAYS_BEFORE)
STORM_DAYS_AFTER_OFFSET = pd.Timedelta(days=STORM_DAYS_AFTER)

# Minimum days before and after a storm for analysis
MINIMUM_DAYS_BEFORE = pd.Timedelta(days=1)
MINIMUM_DAYS_AFTER = pd.Timedelta(days=1)

# Configure matplotlib settings
plt.rcParams["figure.dpi"] = 150
global_figsize = (8, 4)
sns.set_theme(style="whitegrid")
sns.set_context("paper")


def get_summary_df_asy(storm_dfs):
    # Define column names for the summary DataFrame
    sum_cols = ["Start date", "End date", "TD", "Max ASY-H"]

    summary_df = pd.DataFrame(columns=sum_cols)

    # Iterate over storm DataFrames
    for stdf in storm_dfs:
        dat = [
            stdf.index[0],  # Start date of the storm
            stdf.index[-1],  # End date of the storm
            stdf.index[-1] - stdf.index[0],  # Time duration of the storm
            stdf["ASY_H"].max(),  # Maximum ASY-H value during the storm
        ]

        # Append the storm summary data to the summary DataFrame
        summary_df = pd.concat(
            [
                summary_df,
                pd.DataFrame(data=[dat], columns=sum_cols),
            ],
            ignore_index=True,
        )

    return summary_df


def get_summary_df_sym(storm_dfs):
    # Define column names for the summary DataFrame
    sum_cols = ["Start date", "End date", "TD", "Min SYM-H"]

    summary_df = pd.DataFrame(columns=sum_cols)

    # Iterate over storm DataFrames
    for stdf in storm_dfs:
        dat = [
            stdf.index[0],  # Start date of the storm
            stdf.index[-1],  # End date of the storm
            stdf.index[-1] - stdf.index[0],  # Time duration of the storm
            stdf["SYM_H"].min(),  # Minimum SYM-H value during the storm
        ]

        # Append the storm summary data to the summary DataFrame
        summary_df = pd.concat(
            [
                summary_df,
                pd.DataFrame(data=[dat], columns=sum_cols),
            ],
            ignore_index=True,
        )

    return summary_df


def plot_storm_asy(dfx, summary_df, storm_to_plot):
    # Check the type of storm_to_plot to determine how to extract the storm information
    # If its the index of the summary dataframe or a date
    if type(storm_to_plot) is int:
        plot_start = summary_df.iloc[storm_to_plot, :]["Start date"]
        plot_end = summary_df.iloc[storm_to_plot, :]["End date"]
        row = summary_df.iloc[storm_to_plot, :]

    elif type(storm_to_plot) is str:
        dt = pd.to_datetime(storm_to_plot, infer_datetime_format=True, utc=True)
        row = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt), :
        ].squeeze()
        plot_start = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt),
            "Start date",
        ].item()
        plot_end = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt), "End date"
        ].item()

    # Print information about the storm being plotted
    print(f"Plotting storm {storm_to_plot}")
    print(row)

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(8, 3))

    # Plot the ASY-H values for the specified storm period
    dfx[plot_start:plot_end]["ASY_H"].plot(legend=False, xlabel="Date", ax=ax)

    # Set the y-axis label
    ax.set_ylabel("ASY-H (nT)", fontsize=7)

    # Add horizontal lines to represent different ASY-H thresholds for storm intensity levels
    max_asy = dfx[plot_start:plot_end]["ASY_H"].max()
    if max_asy >= ASY_H_THRESHOLD_LOW:
        ax.axhline(ASY_H_THRESHOLD_LOW, linestyle="--", color=COLOR_LOW)

        if max_asy >= ASY_H_THRESHOLD_MODERATE:
            ax.axhline(ASY_H_THRESHOLD_MODERATE, linestyle="--", color=COLOR_MODERATE)

            if max_asy >= ASY_H_THRESHOLD_INTENSE:
                ax.axhline(ASY_H_THRESHOLD_INTENSE, linestyle="--", color=COLOR_INTENSE)

                if max_asy >= ASY_H_THRESHOLD_SUPERINTENSE:
                    ax.axhline(
                        ASY_H_THRESHOLD_SUPERINTENSE, linestyle="--", color=COLOR_SUPERINTENSE
                    )

    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:>8.0f}"))

    return ax


def plot_storm_sym(dfx, summary_df, storm_to_plot):
    # Check the type of storm_to_plot to determine how to extract the storm information
    # If its the index of the summary dataframe or a date
    if type(storm_to_plot) is int:
        plot_start = summary_df.iloc[storm_to_plot, :]["Start date"]
        plot_end = summary_df.iloc[storm_to_plot, :]["End date"]
        row = summary_df.iloc[storm_to_plot, :]

    elif type(storm_to_plot) is str:
        dt = pd.to_datetime(storm_to_plot, infer_datetime_format=True)
        row = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt), :
        ].squeeze()
        plot_start = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt),
            "Start date",
        ].item()
        plot_end = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt), "End date"
        ].item()

    # Print information about the storm being plotted
    print(f"Plotting storm {storm_to_plot}")
    print(row)

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(8, 3))

    # Plot the SYM-H values for the specified storm period
    dfx[plot_start:plot_end]["SYM_H"].plot(legend=False, xlabel="Date", ax=ax)

    # Set the y-axis label
    ax.set_ylabel("SYM-H (nT)", fontsize=7)

    # Add horizontal lines to represent different SYM-H thresholds for storm intensity levels
    min_sym = dfx[plot_start:plot_end]["SYM_H"].min()
    if min_sym <= SYM_H_THRESHOLD_LOW:
        ax.axhline(SYM_H_THRESHOLD_LOW, linestyle="--", color=COLOR_LOW)

        if min_sym <= SYM_H_THRESHOLD_MODERATE:
            ax.axhline(SYM_H_THRESHOLD_MODERATE, linestyle="--", color=COLOR_MODERATE)

            if min_sym <= SYM_H_THRESHOLD_INTENSE:
                ax.axhline(SYM_H_THRESHOLD_INTENSE, linestyle="--", color=COLOR_INTENSE)

                if min_sym <= SYM_H_THRESHOLD_SUPERINTENSE:
                    ax.axhline(
                        SYM_H_THRESHOLD_SUPERINTENSE, linestyle="--", color=COLOR_SUPERINTENSE
                    )

    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:>8.0f}"))

    return ax


def get_storm(dfx, summary_df, storm_to_get):
    # Check the type of storm_to_get to determine how to extract the storm information
    if type(storm_to_get) is int:
        get_start = summary_df.iloc[storm_to_get, :]["Start date"]
        get_end = summary_df.iloc[storm_to_get, :]["End date"]

    elif type(storm_to_get) is str:
        dt = pd.to_datetime(storm_to_get, infer_datetime_format=True, utc=True)
        get_start = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt),
            "Start date",
        ].item()
        get_end = summary_df.loc[
            (summary_df["Start date"] < dt) & (summary_df["End date"] > dt), "End date"
        ].item()

    # Return the selected storm data as a copy of the corresponding portion of the dataframe
    return dfx[get_start:get_end].copy()
