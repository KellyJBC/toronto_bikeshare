from typing import Dict, Literal, List

import pandas as pd

try:
    # Case 1: analytics.py imported as part of the src package
    from .data_cleaning import (
        TRIP_DATE_COL,
        START_HOUR_COL,
        TRIP_DURATION_MIN_COL,
        START_WEEKDAY_COL,
        START_MONTH_COL,
    )
    from .data_loading import START_TIME_COL
except ImportError:
    try:
        # Case 2: analytics.py executed directly from src directory
        from data_cleaning import (
            TRIP_DATE_COL,
            START_HOUR_COL,
            TRIP_DURATION_MIN_COL,
            START_WEEKDAY_COL,
            START_MONTH_COL,
        )
        from data_loading import START_TIME_COL
    except ImportError:
        # Case 3: executed from another directory – adjust sys.path
        import os
        import sys

        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)

        from data_cleaning import (
            TRIP_DATE_COL,
            START_HOUR_COL,
            TRIP_DURATION_MIN_COL,
            START_WEEKDAY_COL,
            START_MONTH_COL,
        )
        from data_loading import START_TIME_COL



# Helper functions for US-12 (refactor)

def _require_columns(df: pd.DataFrame, cols: list) -> None:
    """Raise ValueError if any required columns are missing."""
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {missing}")


def _group_count(
    df: pd.DataFrame,
    group_col: str,
    count_col_name: str = "trip_count",
) -> pd.DataFrame:
    """
    Group by a single column, count rows, and sort by that column.

    Returns a DataFrame with:
    - group_col
    - count_col_name
    """
    grouped = (
        df.groupby(group_col)
        .size()
        .reset_index(name=count_col_name)
        .sort_values(group_col)
    )
    return grouped



# Analytics functions

def hourly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Number of trips per hour of day (using START_HOUR_COL).
    """
    _require_columns(df, [START_HOUR_COL])
    return _group_count(df, START_HOUR_COL, "trip_count")


def daily_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Number of trips per calendar day (using TRIP_DATE_COL).
    """
    _require_columns(df, [TRIP_DATE_COL])
    return _group_count(df, TRIP_DATE_COL, "trip_count")


def weekly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Number of trips per ISO week of the start time (using START_TIME_COL).
    Adds a 'week_label' column like '2024-W31'.
    """
    _require_columns(df, [START_TIME_COL])

    temp = df.copy()
    temp["week_label"] = temp[START_TIME_COL].dt.strftime("%G-W%V")

    return _group_count(temp, "week_label", "trip_count")


def monthly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Number of trips per year-month of the start time (using START_TIME_COL).
    Adds a 'year_month' column like '2024-08'.
    """
    _require_columns(df, [START_TIME_COL])

    temp = df.copy()
    temp["year_month"] = temp[START_TIME_COL].dt.strftime("%Y-%m")

    return _group_count(temp, "year_month", "trip_count")


def popular_stations(
    df: pd.DataFrame,
    top_n: int = 10,
    by: Literal["start", "end"] = "start",
) -> pd.DataFrame:
    """
    Compute top N popular stations by start or end.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned trip data.
    top_n : int
        Number of stations to return.
    by : {'start', 'end'}
        Whether to use Start Station Name or End Station Name.

    Returns
    -------
    pd.DataFrame
        Columns:
        - station_name
        - trip_count
    """
    if by == "start":
        col = "Start Station Name"
    elif by == "end":
        col = "End Station Name"
    else:
        raise ValueError("Parameter 'by' must be 'start' or 'end'.")

    _require_columns(df, [col])

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

    Raises
    ------
    ValueError
        If TRIP_DURATION_MIN_COL is missing.
    """
    _require_columns(df, [TRIP_DURATION_MIN_COL])

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
        Percentiles to compute, e.g. [0.25, 0.75].
    """
    if quantiles is None:
        quantiles = [0.25, 0.5, 0.75]

    _require_columns(df, [TRIP_DURATION_MIN_COL])

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
        key = f"q{int(q * 100)}"
        result[key] = float(value)

    return result
