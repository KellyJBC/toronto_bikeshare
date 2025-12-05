from pathlib import Path
from typing import Optional

import pandas as pd

# Column name constants
TRIP_ID_COL = "Trip Id"
START_TIME_COL = "Start Time"
END_TIME_COL = "End Time"
USER_TYPE_COL = "User Type"

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


def load_station_coordinates(csv_path: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Load optional station coordinates CSV for map visualization.

    Expected columns:
    - station_id
    - station_name
    - lat
    - lon

    If the file does not exist, returns None (map plot will be skipped).

    Parameters
    ----------
    csv_path : str or None
        Optional path to the CSV. If None, uses DEFAULT_STATION_COORDS_CSV.

    Returns
    -------
    df_coords : pandas.DataFrame or None
    """
    path = Path(csv_path) if csv_path is not None else DEFAULT_STATION_COORDS_CSV
    if not path.exists():
        # This is not considered an error; map is optional.
        return None

    df = pd.read_csv(path)

    required_cols = {"station_id", "station_name", "lat", "lon"}
    missing = required_cols.difference(df.columns)
    if missing:
        raise ValueError(f"Station coordinates CSV missing columns: {missing}")

    return df
