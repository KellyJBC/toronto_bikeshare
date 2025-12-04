from typing import Dict, Literal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

from .data_cleaning import (
    TRIP_DATE_COL,
    START_HOUR_COL,
    TRIP_DURATION_MIN_COL,
)

from .analytics import (
    hourly_trip_counts,
    daily_trip_counts,
    weekly_trip_counts,
    popular_stations,
    user_type_summary,
    monthly_trip_counts,
)

from .data_loading import load_station_coordinates

def plot_hourly_usage(df: pd.DataFrame):
    hourly_df = hourly_trip_counts(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(hourly_df["start_hour"], hourly_df["trip_count"])
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Trips per Hour")
    ax.set_xticks(range(0, 24))
    fig.tight_layout()
    return fig
