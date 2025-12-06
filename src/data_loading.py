from pathlib import Path
from typing import Optional

import pandas as pd

# Column name constants
TRIP_ID_COL = "Trip Id"
START_TIME_COL = "Start Time"
END_TIME_COL = "End Time"
USER_TYPE_COL = "User Type"

# Default file and directory paths
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
            An optional path to a CSV file. If not provided, the function defaults
            to using the project’s main trip file located at `DEFAULT_TRIP_CSV`.

    Returns
    -------
    df : pandas.DataFrame
         A DataFrame containing all required trip fields.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If required columns are missing.


    Notes:
        - This function does not alter the data; it only loads and validates it.
        - The returned DataFrame should be passed into the cleaning pipeline.    
    """

    path = Path(csv_path) if csv_path is not None else DEFAULT_TRIP_CSV
    
    # Verify the file exists before attempting to read it
    if not path.exists():
        raise FileNotFoundError(f"Trip CSV not found at: {path}")

    df = pd.read_csv(path)
    
    # Confirm that the dataset includes all required fields
    missing = [col for col in EXPECTED_TRIP_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Trip CSV missing expected columns: {missing}")

    return df


def load_station_coordinates(csv_path: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Load the optional station coordinates file used for map visualizations

    Expected columns:
    - station_id
    - station_name
    - lat
    - lon

    If the file does not exist, returns None (map plot will be skipped).

    Parameters
    ----------
    csv_path : str or None
            Optional path to the station coordinate file. If not provided,
            the loader defaults to `DEFAULT_STATION_COORDS_CSV`.

    Returns
    -------
    df_coords : A DataFrame with station coordinate details, or None if the file
                does not exist.

    Raises:
        ValueError:
            If the file exists but required columns are missing.
        """
    
    path = Path(csv_path) if csv_path is not None else DEFAULT_STATION_COORDS_CSV
    # If the file is not provided, return None but do not raise an error
    if not path.exists():
        # This is not considered an error; map is optional.
        return None

    df = pd.read_csv(path)
    
    # Validate that the coordinate file contains all required fields
    required_cols = {"station_id", "station_name", "lat", "lon"}
    missing = required_cols.difference(df.columns)
    if missing:
        raise ValueError(f"Station coordinates CSV missing columns: {missing}")

    return df
