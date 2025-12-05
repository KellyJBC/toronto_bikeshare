test_end_to_end.py

Light integration smoke test:
- Load raw data
- Clean and enrich
- Compute a couple of summaries
"""

from src.data_loading import load_raw_data
from src.data_cleaning import full_clean_pipeline
from src.analytics import hourly_trip_counts, daily_trip_counts


def test_end_to_end_pipeline_runs():
    df_raw = load_raw_data()
    df_clean = full_clean_pipeline(df_raw)
    hourly = hourly_trip_counts(df_clean)
    daily = daily_trip_counts(df_clean)

    assert not df_clean.empty
    assert not hourly.empty
    assert not daily.empty
