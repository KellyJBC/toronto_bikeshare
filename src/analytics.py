from typing import Dict, Literal

import pandas as pd

from .data_cleaning import (
    TRIP_DATE_COL,
    START_HOUR_COL,
    START_WEEKDAY_COL,
    START_MONTH_COL,
    TRIP_DURATION_MIN_COL
)

from .data_loading import (
    START_TIME_COL,  # if needed
)


def hourly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group by start_hour and count trips.

    Returns a DataFrame with columns:
    - start_hour (int)
    - trip_count (int)
    """
    if START_HOUR_COL not in df.columns:
        raise ValueError(f"{START_HOUR_COL} not found. Did you run parse_and_enrich_datetime()?")

    grouped = (
        df.groupby(START_HOUR_COL)
        .size()
        .reset_index(name="trip_count")
        .sort_values(START_HOUR_COL)
    )
    return grouped
