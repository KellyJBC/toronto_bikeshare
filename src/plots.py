from typing import Dict, Literal

import pandas as pd

from .data_cleaning import (
    TRIP_DATE_COL,
    START_HOUR_COL,
    TRIP_DURATION_MIN_COL,
)

# We use the raw column name here so we don't depend on other modules for this constant
START_TIME_COL = "Start Time"


def hourly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group by start_hour and count trips.

    Returns a DataFrame with columns:
    - start_hour (int)
    - trip_count (int)
    """
    if START_HOUR_COL not in df.columns:
        raise ValueError(
            f"{START_HOUR_COL} not found. Did you run parse_and_enrich_datetime()?"
        )

    grouped = (
        df.groupby(START_HOUR_COL)
        .size()
        .reset_index(name="trip_count")
        .sort_values(START_HOUR_COL)
    )
    return grouped


def daily_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group by trip_date and count trips.

    Returns columns:
    - trip_date
    - trip_count
    """
    if TRIP_DATE_COL not in df.columns:
        raise ValueError(
            f"{TRIP_DATE_COL} not found. Did you run parse_and_enrich_datetime()?"
        )

    grouped = (
        df.groupby(TRIP_DATE_COL)
        .size()
        .reset_index(name="trip_count")
        .sort_values(TRIP_DATE_COL)
    )
    return grouped


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_hour_weekday_heatmap(df: pd.DataFrame):
    """
    Heatmap Hour vs Weekday
    Required Data:
    - start_hour
    - start_weekday
    """

    # Days Order
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Create pivot table
    pivot = (
        df.pivot_table(
            index="start_weekday",
            columns="start_hour",
            values="Trip  Duration",   # cualquier valor, solo contamos filas
            aggfunc="count"
        )
        .reindex(weekday_order)        # asegura el orden correcto
        .fillna(0)
    )

    plt.figure(figsize=(10, 5))
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label="Trip Count")
    plt.xticks(ticks=np.arange(24), labels=np.arange(24))
    plt.yticks(ticks=np.arange(7), labels=weekday_order)
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")
    plt.title("Bike Trips Heatmap (Hour vs Weekday)")
    plt.tight_layout()
    plt.show()
    

def plot_trip_duration_hist(df: pd.DataFrame):
    """
    Histogram of Trip Duration (minutes)
    Requires column: trip_duration_min
    -Shows short vs. long trips
    -Detects outliers
    -Displays the shape of the distribution
    """

    if "trip_duration_min" not in df.columns:
        raise ValueError("trip_duration_min not found. Run parse_and_enrich_datetime first.")

    plt.figure(figsize=(8, 4))
    plt.hist(df["trip_duration_min"], bins=50)
    plt.xlabel("Trip Duration (minutes)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Trip Duration")
    plt.tight_layout()
    plt.show()


def plot_avg_trip_duration_daily(df: pd.DataFrame):
    """
    Plot the average trip duration per day.
    Requires:
    - trip_date
    - trip_duration_min
    """

    daily_avg = (
        df.groupby("trip_date")["trip_duration_min"]
        .mean()
        .reset_index()
        .sort_values("trip_date")
    )

    plt.figure(figsize=(10, 4))
    plt.plot(daily_avg["trip_date"], daily_avg["trip_duration_min"])
    plt.xlabel("Date")
    plt.ylabel("Avg Trip Duration (min)")
    plt.title("Daily Average Trip Duration")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


