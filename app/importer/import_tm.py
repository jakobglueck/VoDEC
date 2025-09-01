import pandas as pd

SHEET_NAME = "TM aufbereitet"

def import_fam_sheet(file_path: str) -> pd.DataFrame:
    """
    Finds and reads the specified FAM sheet from an Excel file.
    
    Args:
        file_path: The path to the input Excel file.
        
    Returns:
        A pandas DataFrame with the raw data from the sheet.
        
    Raises:
        ValueError: If the specified sheet cannot be found in the file.
    """
    try:
        raw_df = pd.read_excel(file_path, sheet_name=SHEET_NAME, decimal=',')
        return raw_df
    except ValueError:
        raise ValueError(f"Sheet '{SHEET_NAME}' could not be found in the Excel file.")
    