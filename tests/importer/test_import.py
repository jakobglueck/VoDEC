from pathlib import Path
import pandas as pd
import pytest
from app.importer import import_fam
from app.importer import import_tm

def test_import_fam_succeeds_when_file_and_sheet_exist():

    current_file = Path(__file__)
    project_root = current_file.parent.parent
    asset_file_path = project_root / "test_assets" / "test_excel.xlsx"

    try:
        result_df = import_fam.import_fam_sheet(asset_file_path)

        assert isinstance(result_df, pd.DataFrame)
        
    except Exception as e:
        pytest.fail(f"Function raised an unexpected exception: {e}")

def test_import_tm_succeeds_when_file_and_sheet_exist():

    current_file = Path(__file__)
    project_root = current_file.parent.parent
    asset_file_path = project_root / "test_assets" / "test_excel.xlsx"

    try:
        result_df = import_tm.import_tm_sheet(asset_file_path)

        assert isinstance(result_df, pd.DataFrame)
        
    except Exception as e:
        pytest.fail(f"Function raised an unexpected exception: {e}")
