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

