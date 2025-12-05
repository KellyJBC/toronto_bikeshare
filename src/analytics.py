
from typing import Dict, Literal

import pandas as pd

try:
    # Intento 1: Cuando analytics.py se importa como parte del paquete src
    from .data_cleaning import (
        TRIP_DATE_COL,
        START_HOUR_COL,
    )
    from .data_loading import START_TIME_COL
except ImportError:
    # Intento 2: Cuando analytics.py se ejecuta directamente
    try:
        from data_cleaning import (
            TRIP_DATE_COL,
            START_HOUR_COL,
            TRIP_DURATION_MIN_COL,
            START_WEEKDAY_COL,
            START_MONTH_COL
        )
        from data_loading import START_TIME_COL
    except ImportError:
        # Intento 3: Cuando se ejecuta desde otro directorio
        import sys
        import os
        
        # Agregar el directorio actual al path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from data_cleaning import (
            TRIP_DATE_COL,
            START_HOUR_COL,
            TRIP_DURATION_MIN_COL,
            START_WEEKDAY_COL,
            START_MONTH_COL
        )
        from data_loading import START_TIME_COL

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

def daily_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group by trip_date and count trips.

    Returns columns:
    - trip_date
    - trip_count
    """
    if TRIP_DATE_COL not in df.columns:
        raise ValueError(f"{TRIP_DATE_COL} not found. Did you run parse_and_enrich_datetime()?")

    grouped = (
        df.groupby(TRIP_DATE_COL)
        .size()
        .reset_index(name="trip_count")
        .sort_values(TRIP_DATE_COL)
    )
    return grouped


def weekly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group trips by ISO week number using TRIP_DATE_COL.
    """
    if TRIP_DATE_COL not in df.columns:
        raise ValueError(f"{TRIP_DATE_COL} not found. Did you run parse_and_enrich_datetime()?")

    temp = df.copy()
    temp["week_label"] = temp[TRIP_DATE_COL].dt.strftime("%G-W%V")

    grouped = (
        temp.groupby("week_label")
        .size()
        .reset_index(name="trip_count")
        .sort_values("week_label")
    )
    return grouped

def popular_stations(
    df: pd.DataFrame,
    top_n: int = 10,
    by: Literal["start", "end"] = "start",
) -> pd.DataFrame:
    """
    Compute top N popular stations.

    Parameters
    ----------
    by : "start" or "end"
        Whether to use Start Station Name or End Station Name.

    Returns columns:
    - station_name
    - trip_count
    """
    if by == "start":
        col = "Start Station Name"
    elif by == "end":
        col = "End Station Name"
    else:
        raise ValueError("Parameter 'by' must be 'start' or 'end'.")

    grouped = (
        df.groupby(col)
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
        .head(top_n)
    )
    grouped = grouped.rename(columns={col: "station_name"})
    return grouped

def user_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize trips by user type.

    Returns columns:
    - User Type
    - trip_count
    - avg_duration_min
    """
    if TRIP_DURATION_MIN_COL not in df.columns:
        raise ValueError(f"{TRIP_DURATION_MIN_COL} not found. Did you run parse_and_enrich_datetime()?")

    grouped = (
        df.groupby("User Type")
        .agg(
            trip_count=("Trip Id", "count"),
            avg_duration_min=(TRIP_DURATION_MIN_COL, "mean"),
        )
        .reset_index()
        .sort_values("trip_count", ascending=False)
    )
    return grouped
