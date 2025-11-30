import pytest

from src.data_loading import load_raw_data, EXPECTED_TRIP_COLUMNS


def test_load_raw_data_returns_dataframe():
    df = load_raw_data()
    assert not df.empty, "DataFrame should not be empty"
    for col in EXPECTED_TRIP_COLUMNS:
        assert col in df.columns, f"Missing expected column: {col}"


def test_load_raw_data_missing_file_raises(tmp_path, monkeypatch):
    fake_path = tmp_path / "missing.csv"

    # Monkeypatch default path to a fake file
    from src import data_loading

    monkeypatch.setattr(data_loading, "DEFAULT_TRIP_CSV", fake_path)

    with pytest.raises(FileNotFoundError):
        load_raw_data()

import pandas as pd

from src.data_cleaning import (
    clean_basic,
    parse_and_enrich_datetime,
    TRIP_DATE_COL,
    START_HOUR_COL,
    START_WEEKDAY_COL,
    START_MONTH_COL,
    TRIP_DURATION_MIN_COL,
)


def sample_raw_df():
    data = {
        "Trip Id": [1, 2, 3],
        "Trip  Duration": [600, -10, 300],
        "Start Station Id": [111, 222, 333],
        "Start Time": ["08/01/2024 10:00", "08/01/2024 11:00", None],
        "Start Station Name": ["A", "B", "C"],
        "End Station Id": [444, 555, 666],
        "End Time": ["08/01/2024 10:10", "08/01/2024 11:05", "08/01/2024 11:10"],
        "End Station Name": ["D", "E", "F"],
        "Bike Id": [1, 2, 3],
        "User Type": ["Casual Member", "Member", None],
        "Model": ["ICONIC", "ICONIC", "ICONIC"],
    }
    return pd.DataFrame(data)


def test_clean_basic_drops_invalid_rows():
    df_raw = sample_raw_df()
    df_clean = clean_basic(df_raw)

    assert len(df_clean) == 1
    assert df_clean.iloc[0]["Trip Id"] == 1


def test_parse_and_enrich_datetime_adds_features():
    df_raw = sample_raw_df()
    df_clean = clean_basic(df_raw)
    df_feat = parse_and_enrich_datetime(df_clean)

    assert TRIP_DATE_COL in df_feat.columns
    assert START_HOUR_COL in df_feat.columns
    assert START_WEEKDAY_COL in df_feat.columns
    assert START_MONTH_COL in df_feat.columns
    assert TRIP_DURATION_MIN_COL in df_feat.columns

    # Check a specific value
    row = df_feat.iloc[0]
    assert row[TRIP_DATE_COL].year == 2024
    assert row[START_HOUR_COL] == 10
    assert row[TRIP_DURATION_MIN_COL] == 600 / 60.0
