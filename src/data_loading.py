from pathlib import Path
from typing import Optional

import pandas as pd

# Constants for default paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_TRIP_CSV = DATA_DIR / "financial_transactions_toronto_bike.csv"
DEFAULT_STATION_COORDS_CSV = DATA_DIR / "stations_coordinates.csv"

# Expected columns in the trip CSV (from the provided file)
EXPECTED_TRIP_COLUMNS = [
    "Trip Id",
    "Trip  Duration",
    "Start Station Id",
    "Start Time",
    "Start Station Name",
    "End Station Id",
    "End Time",
    "End Station Name",
    "Bike Id",
    "User Type",
    "Model",
]


def load_raw_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the raw Toronto bike-sharing CSV into a pandas DataFrame.

    Parameters
    ----------
    csv_path : str or None
        Optional path to the CSV. If None, uses DEFAULT_TRIP_CSV.

    Returns
    -------
    df : pandas.DataFrame
        Loaded DataFrame with the expected columns.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If required columns are missing.
    """
    path = Path(csv_path) if csv_path is not None else DEFAULT_TRIP_CSV

    if not path.exists():
        raise FileNotFoundError(f"Trip CSV not found at: {path}")

    df = pd.read_csv(path)

    missing = [col for col in EXPECTED_TRIP_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Trip CSV missing expected columns: {missing}")

    return df
