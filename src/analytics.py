
from typing import Dict, Literal

# -----------------------------------------------------------------------
# Import handling:
# The following block allows analytics.py to be imported or executed
# -----------------------------------------------------------------------

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

# =======================================================================
#                               ANALYTICS
# =======================================================================



def hourly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the total number of trips occurring in each hour of the day.

    Returns:
            - START_HOUR_COL (int): Hour of day
            - trip_count (int): Number of trips recorded in that hour

    Raises:
        ValueError: If START_HOUR_COL is missing from the dataframe.
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
    Compute the total number of trips per calendar day.

    Returns:
            - TRIP_DATE_COL (datetime.date)
            - trip_count (int)

    Raises:
        ValueError: If TRIP_DATE_COL is missing.
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
    Compute the number of trips grouped by ISO week number.
    Week labels follow the ISO format YYYY-Www.

    Returns:
            - week_label (str): ISO week label (example: 2024-W31)
            - trip_count (int)

    Raises:
        ValueError: If TRIP_DATE_COL is missing.
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
    Compute the top N most frequently used stations.

    Args:
        df (pd.DataFrame): Dataframe containing station name columns.
        top_n (int): Number of top stations to return.
        by (Literal["start", "end"]): Whether to use the start or end
            station column.

    Returns:
            - station_name (str)
            - trip_count (int)

    Raises:
        ValueError: If the `by` argument is not "start" or "end".
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

    Raises:
        ValueError: If TRIP_DURATION_MIN_COL is missing.
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
    

def trip_duration_summary(df: pd.DataFrame, quantiles=None) -> Dict[str, float]:
    """
    Summary statistics for trip duration (in minutes).

    Returns a dictionary with keys:
    - mean, median, min, max, and selected percentiles.

    Parameters
    ----------
    quantiles : list[float] or None
                Percentiles to compute, example: [0.25, 0.75].
    """
    
    if quantiles is None:
        quantiles = [0.25, 0.5, 0.75]

    if TRIP_DURATION_MIN_COL not in df.columns:
        raise ValueError(f"{TRIP_DURATION_MIN_COL} not found. Did you run parse_and_enrich_datetime()?")

    series = df[TRIP_DURATION_MIN_COL].dropna()
    if series.empty:
        return {}

    result: Dict[str, float] = {
        "mean": float(series.mean()),
        "median": float(series.median()),
        "min": float(series.min()),
        "max": float(series.max()),
    }

    q_values = series.quantile(quantiles)
    for q, value in zip(quantiles, q_values):
        key = f"q{int(q*100)}"
        result[key] = float(value)

    return result
