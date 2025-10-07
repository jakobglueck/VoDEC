import pandas as pd
import pytest
from app.exporter.workbook_builder import export_to_single_workbook

@pytest.fixture
def sample_active_fam_df():
    """Creates a sample DataFrame for cleaned FAM data with German column names."""
    data = {
        "kasse": ["AOK Plus"],
        "patnr": ["98765"],
        "pzn": ["12345678"],
        "am-name": ["Testarzneimittel"],
        "avk": [19.99],
        "vo-datum": ["01.07.2024"],
        "anzahl": [1]
    }

    all_cols = [
        "kasse", "patnr", "pzn", "am-name", "avk", "vo-datum", "anzahl", "lanr",
        "arzt-titel", "arzt-vorname", "arzt-nachname", "arzt-str", "arzt-plz",
        "arzt-ort", "apo-name", "apo-plz", "apo-ort", "bsnr", "betriebsbez.",
        "apo-str", "arzt-tel", "kv-bezirk", "FA-Bezeichnung", "rolle", "abrdatum",
        "lanrtmp", "belegnr", "arzt-id", "apo-inhaber",
        "applikationsfertige Einheiten", "vo-id"
    ]
    df = pd.DataFrame(data)
    for col in all_cols:
        if col not in df.columns:
            df[col] = None 
    return df[all_cols]


@pytest.fixture
def sample_active_tm_df():
    """Creates a sample DataFrame for cleaned TM data."""
    data = {
        "VO-ID": ["V12345"],
        "PZN": ["12345678"],
        "Bezeichnung": ["Testarzneimittel Detail"],
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_analysis_notes():
    """Creates a sample dictionary for the analysis notes."""
    return {
        "Anzahl Zeilen FAM original:": 15,
        "Anzahl Zeilen FAM aufbereitet:": 10,
        "Preis konsistent innerhalb der Daten?": "Yes",
    }

@pytest.fixture
def sample_rejected_fam_data():
    """Creates a sample dictionary for rejected FAM rows."""
    rejected_df = pd.DataFrame({
        "kasse": ["BKK Billig"],
        "patnr": ["55555"],
        "avk": [0.0],
    })
    return {
        "avk ist ungültig (fehlt oder <= 0)": rejected_df
    }

def test_export_to_single_workbook(
    tmp_path,
    sample_active_fam_df,
    sample_active_tm_df,
    sample_analysis_notes,
    sample_rejected_fam_data,
):
    """
    Tests the creation of the complete Excel workbook with all sheets.
    """
    output_file = tmp_path / "final_report.xlsx"

    export_to_single_workbook(
        output_path=str(output_file),
        active_fam_df=sample_active_fam_df,
        active_tm_df=sample_active_tm_df,
        analysis_notes=sample_analysis_notes,
        rejected_fam_data=sample_rejected_fam_data,
        rejected_tm_data={}
    )

    assert output_file.exists()

    xls = pd.ExcelFile(output_file)

    expected_sheets = [
        "FAM_aufbereitet",
        "TM_aufbereitet",
        "Analyse_Hinweise",
        "Ausschuss_FAM",
    ]
    assert all(sheet in xls.sheet_names for sheet in expected_sheets)
    assert "Ausschuss_TM" not in xls.sheet_names

    df_fam_from_excel = pd.read_excel(xls, sheet_name="FAM_aufbereitet")

    for col in sample_active_fam_df.columns:
        if sample_active_fam_df[col].dtype == 'object':

            df_fam_from_excel[col] = df_fam_from_excel[col].astype(str).replace('nan', pd.NA)

    pd.testing.assert_frame_equal(df_fam_from_excel, sample_active_fam_df)

    df_notes = pd.read_excel(xls, sheet_name="Analyse_Hinweise", header=None)
    assert df_notes.iloc[0, 0] == "Anzahl Zeilen FAM original:"
    assert df_notes.iloc[0, 1] == 15
    assert df_notes.iloc[2, 0] == "Preis konsistent innerhalb der Daten?"
    assert df_notes.iloc[2, 1] == "Yes"

    df_rejected = pd.read_excel(xls, sheet_name="Ausschuss_FAM", header=None)
    
    expected_header = 'Folgende Zeilen wurden aus dem Sheet "FAM ihpE aufbereitet" herausgeschnitten, da avk ist ungültig (fehlt oder <= 0):'
    assert df_rejected.iloc[0, 0] == expected_header

    assert "kasse" in str(df_rejected.iloc[2, 0])

    assert str(df_rejected.iloc[3, 0]) == "BKK Billig"
    assert str(df_rejected.iloc[3, 1]) == "55555"
