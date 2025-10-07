import pandas as pd
import pytest
from app.core.data_analyzer import (
    analyze_price_consistency,
    determine_price_type,
    calculate_total_avk_sum,
    check_void_tm_consistency,
    detect_date_format,
    generate_analysis_notes
)

@pytest.fixture
def sample_fam_df():
    """Provides a sample processed FAM DataFrame."""
    return pd.DataFrame({
        'pzn': ['PZN1', 'PZN1', 'PZN2', '09999100', '9999100'],
        'medicine_price': [10.0, 20.0, 30.0, 5.0, 6.0],
        'amount': [1, 2, 1, 1, 1],
        'vo_id': ['V1', 'V2', 'V3', 'V4', 'V5']
    })

@pytest.fixture
def sample_tm_df():
    """Provides a sample processed TM DataFrame."""
    return pd.DataFrame({'vo_id': ['V1', 'V2', 'V3', 'V4']})

def test_analyze_price_consistency(sample_fam_df):
    """Tests the price consistency logic."""
    assert analyze_price_consistency(sample_fam_df) == "Yes"
    
    inconsistent_df = pd.concat([sample_fam_df, pd.DataFrame({
        'pzn': ['PZN1'], 'medicine_price': [13.0], 'amount': [1], 'vo_id': ['V6']
    })], ignore_index=True)
    assert analyze_price_consistency(inconsistent_df) == "No"

def test_determine_price_type():
    """Tests the GP vs EP detection logic."""

    gp_data_1 = {'pzn': ['GP1', 'GP1'], 'medicine_price': [15.0, 30.0], 'amount': [1, 2]}

    ep_data = {'pzn': ['EP1', 'EP1'], 'medicine_price': [25.0, 25.0], 'amount': [1, 2]}

    gp_data_2 = {'pzn': ['GP2', 'GP2'], 'medicine_price': [100.0, 50.0], 'amount': [2, 1]}

    df1 = pd.DataFrame(gp_data_1)
    df2 = pd.DataFrame(ep_data)
    df3 = pd.DataFrame(gp_data_2)
    df = pd.concat([df1, df2, df3], ignore_index=True)

    assert determine_price_type(df) == "GP"

def test_calculate_total_avk_sum():
    """Tests the total AVK sum calculation."""
    data = {'medicine_price': [10.0, 20.0], 'amount': [2, 3]}
    df = pd.DataFrame(data)
    assert calculate_total_avk_sum(df, "GP") == 30.0
    assert calculate_total_avk_sum(df, "EP") == 80.0 

def test_detect_date_format():
    """Tests the date format detection."""
    df1 = pd.DataFrame({'vo-datum': ['01.01.2024']})
    assert detect_date_format(df1) == "dd.mm.yyyy"
    
    df2 = pd.DataFrame({'vo-datum': ['2024-01-01 12:00:00']})
    assert detect_date_format(df2) == "yyyy-mm-dd"

    df3 = pd.DataFrame({'vo-datum': ['20240101']})
    assert detect_date_format(df3) == "yyyymmdd"

def test_check_void_tm_consistency(sample_fam_df, sample_tm_df):
    """Tests the VO-ID consistency check, which should now pass."""

    assert check_void_tm_consistency(sample_fam_df, sample_tm_df) == "No"

    consistent_tm_df = pd.concat([sample_tm_df, pd.DataFrame({'vo_id': ['V5']})], ignore_index=True)
    assert check_void_tm_consistency(sample_fam_df, consistent_tm_df) == "Yes"

def test_generate_analysis_notes(sample_fam_df, sample_tm_df):
    """Tests that the main notes generation function runs without errors."""
    raw_fam = pd.DataFrame({'vo-datum': ['01.01.2024'] * 10})
    raw_tm = pd.DataFrame({'data': range(12)})
    
    notes = generate_analysis_notes(
        raw_fam_df=raw_fam,
        processed_fam_df=sample_fam_df,
        raw_tm_df=raw_tm,
        processed_tm_df=sample_tm_df
    )
    
    assert isinstance(notes, dict)
    assert "Anzahl Zeilen FAM original:" in notes
    assert notes["Anzahl Zeilen FAM aufbereitet:"] == 5
    assert notes["VO-ID & TM stimmig?"] == "No"
