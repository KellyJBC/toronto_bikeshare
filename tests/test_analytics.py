import pandas as pd

from src.analytics import (
    hourly_trip_counts,
    daily_trip_counts,
    weekly_trip_counts,
    popular_stations,
)
from src.data_cleaning import TRIP_DATE_COL, START_HOUR_COL
from src.data_loading import START_TIME_COL


def sample_enriched_df():
    data = {
        "Trip Id": [1, 2, 3, 4],
        "Trip  Duration": [300, 600, 900, 1200],
        "Start Station Id": [1, 1, 2, 2],
        "Start Time": [
            "08/01/2024 08:00",
            "08/01/2024 09:00",
            "08/02/2024 08:00",
            "08/02/2024 09:00",
        ],
        "Start Station Name": ["A", "A", "B", "B"],
        "End Station Id": [10, 10, 20, 20],
        "End Time": [
            "08/01/2024 08:05",
            "08/01/2024 09:10",
            "08/02/2024 08:15",
            "08/02/2024 09:20",
        ],
        "End Station Name": ["X", "X", "Y", "Y"],
        "Bike Id": [1, 2, 3, 4],
        "User Type": ["Casual Member", "Member", "Member", "Casual Member"],
        "Model": ["ICONIC", "ICONIC", "ICONIC", "ICONIC"],
    }
    df = pd.DataFrame(data)
    df[START_TIME_COL] = pd.to_datetime(df["Start Time"], format="%m/%d/%Y %H:%M")
    df[TRIP_DATE_COL] = df[START_TIME_COL].dt.date
    df[START_HOUR_COL] = df[START_TIME_COL].dt.hour
    return df


def test_hourly_trip_counts():
    df = sample_enriched_df()
    hourly = hourly_trip_counts(df)
    assert hourly["trip_count"].sum() == len(df)
    assert set(hourly["start_hour"]) == {8, 9}
