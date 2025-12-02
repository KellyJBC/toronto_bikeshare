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
