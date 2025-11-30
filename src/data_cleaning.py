"""
data_cleaning.py

User Stories:
- US-02: Clean and validate basic fields (TDD)
- US-03: Parse datetime and derive time features (TDD)
"""

from typing import Tuple

import numpy as np
import pandas as pd

TRIP_DURATION_COL = "Trip  Duration"
START_TIME_COL = "Start Time"
END_TIME_COL = "End Time"
USER_TYPE_COL = "User Type"

# New feature columns
TRIP_DATE_COL = "trip_date"
START_HOUR_COL = "start_hour"
START_WEEKDAY_COL = "start_weekday"
START_MONTH_COL = "start_month"
TRIP_DURATION_MIN_COL = "trip_duration_min"


def clean_basic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning:
    - Drop rows with missing Start Time, End Time, or User Type.
    - Ensure trip duration is non-negative (drop negative durations).

    Parameters
    ----------
    df : pandas.DataFrame
        Raw DataFrame loaded from CSV.

    Returns
    -------
    cleaned_df : pandas.DataFrame
    """
    df = df.copy()

    # Drop rows with missing key columns
    df = df.dropna(subset=[START_TIME_COL, END_TIME_COL, USER_TYPE_COL])

    # Ensure duration is non-negative
    if TRIP_DURATION_COL in df.columns:
        df = df[df[TRIP_DURATION_COL] >= 0]

    # Optionally reset index
    df = df.reset_index(drop=True)
    return df

def parse_and_enrich_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse Start Time and End Time as datetime and derive useful features:
    - trip_date
    - start_hour
    - start_weekday
    - start_month
    - trip_duration_min (from seconds)

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    df_features : pandas.DataFrame
    """
    df = df.copy()

    # Parse datetimes (format: MM/DD/YYYY HH:MM)
    df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL], format="%m/%d/%Y %H:%M")
    df[END_TIME_COL] = pd.to_datetime(df[END_TIME_COL], format="%m/%d/%Y %H:%M")

    # Derive features
    df[TRIP_DATE_COL] = df[START_TIME_COL].dt.date
    df[START_HOUR_COL] = df[START_TIME_COL].dt.hour
    df[START_WEEKDAY_COL] = df[START_TIME_COL].dt.day_name()
    df[START_MONTH_COL] = df[START_TIME_COL].dt.strftime("%B")

    # Duration in minutes
    if TRIP_DURATION_COL in df.columns:
        df[TRIP_DURATION_MIN_COL] = df[TRIP_DURATION_COL] / 60.0
    else:
        df[TRIP_DURATION_MIN_COL] = np.nan

    return df


def full_clean_pipeline(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function used in notebooks and dashboard.

    Steps:
    - clean_basic()
    - parse_and_enrich_datetime()

    Returns a fully cleaned and feature-enriched DataFrame.
    """
    df = clean_basic(df_raw)
    df = parse_and_enrich_datetime(df)
    return df