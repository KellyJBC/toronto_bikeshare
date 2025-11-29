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
