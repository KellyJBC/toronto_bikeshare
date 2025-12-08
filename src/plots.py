from typing import Dict, Literal, Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

from data_cleaning import (
    TRIP_DATE_COL,
    START_HOUR_COL,
    TRIP_DURATION_MIN_COL,
)

from analytics import (
    hourly_trip_counts,
    daily_trip_counts,
    weekly_trip_counts,
    popular_stations,
    user_type_summary,
    monthly_trip_counts,
)

from data_loading import load_station_coordinates

# We use the raw column name here so we don't depend on other modules for this constant
START_TIME_COL = "Start Time"


def hourly_trip_counts(df: pd.DataFrame) -> pd.DataFrame:
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

def plot_daily_trends(df: pd.DataFrame):
    daily_df = daily_trip_counts(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(daily_df["trip_date"], daily_df["trip_count"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Daily Ridership")
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def plot_weekly_trends(df: pd.DataFrame):
    weekly_df = weekly_trip_counts(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(weekly_df["week_label"], weekly_df["trip_count"], marker="o")
    ax.set_xlabel("ISO Week")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Weekly Ridership")
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig

def plot_popular_stations(df: pd.DataFrame, top_n: int = 10, by: str = "start"):
    stations_df = popular_stations(df, top_n=top_n, by=by)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(stations_df["station_name"], stations_df["trip_count"])
    ax.set_xlabel("Number of Trips")
    ax.set_ylabel("Station")
    title_prefix = "Start" if by == "start" else "End"
    ax.set_title(f"Top {top_n} {title_prefix} Stations")
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def plot_hour_weekday_heatmap(df: pd.DataFrame):
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
    
def plot_duration_histogram(df: pd.DataFrame):
    if "trip_duration_min" not in df.columns:
        raise ValueError("trip_duration_min not found; run parse_and_enrich_datetime().")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["trip_duration_min"], bins=50)
    ax.set_xlabel("Trip Duration (minutes)")
    ax.set_ylabel("Frequency")
    ax.set_title("Trip Duration Distribution")
    fig.tight_layout()
    return fig

def plot_monthly_trends(df: pd.DataFrame):
    monthly_df = monthly_trip_counts(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_df["year_month"], monthly_df["trip_count"], marker="o")
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Monthly Ridership")
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


def plot_trip_duration_hist(df: pd.DataFrame):
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

def plot_user_type_comparison(df: pd.DataFrame):
    summary = user_type_summary(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(summary["User Type"], summary["trip_count"])
    ax.set_xlabel("User Type")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Trips by User Type")
    fig.tight_layout()
    return fig


def plot_hourly_usage(df: pd.DataFrame):
    hourly_df = hourly_trip_counts(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(hourly_df["start_hour"], hourly_df["trip_count"])
    
    # Resumido: Usamos .set() para configurar todo en una línea
    ax.set(xlabel="Hour of Day", ylabel="Number of Trips", title="Trips per Hour", xticks=range(24))
    
    fig.tight_layout()
    return fig

def build_station_map_figure(df: pd.DataFrame) -> Optional["px.scatter_mapbox"]:
    coords = load_station_coordinates()
    if coords is None: return None # Retorno temprano en una línea

    # Misma lógica de agrupación, solo formateada más compacta
    start_usage = (df.groupby("Start Station Id").size()
                   .reset_index(name="trip_count")
                   .rename(columns={"Start Station Id": "station_id"}))

    merged = start_usage.merge(coords, on="station_id", how="left").dropna(subset=["lat", "lon"])

    fig = px.scatter_mapbox(
        merged, lat="lat", lon="lon", size="trip_count", color="trip_count",
        hover_name="station_name", zoom=11, height=500, title="Station Usage Map (Start Stations)"
    )
    
    # Resumido: Unimos los estilos y márgenes en una sola actualización
    fig.update_layout(mapbox_style="open-street-map", margin=dict(r=0, t=50, l=0, b=0))
    
    return fig

