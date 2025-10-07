import pandas as pd
import pytest
from app.core.data_rejection import analyze_rejections, REJECTION_CRITERIA_FAM, REJECTION_CRITERIA_TM

@pytest.fixture
def sample_data_for_rejection():
    """Creates a pair of raw and processed dataframes for testing FAM rejections."""
    raw_df = pd.DataFrame({
        'kasse': ['AOK', 'TK', 'IKK', 'DAK'],
        'patient_nr': ['1', '2', '3', None],
        'pzn': ['p1', 'p2', 'p3', 'p4'],
        'prescription_date': ['d1', 'd2', 'd3', 'd4'],
        'amount': [1, 1, 1, 1],
        'medicine_price': [10.0, 0.0, 50.0, 20.0], 
        'receipt_id': ['r1', 'r2', None, 'r4'],
        'vo_id': ['v1', 'v2', None, 'v4']
    })

    processed_df = raw_df.copy()
    processed_df.loc[1, 'medicine_price'] = None 
    processed_df.loc[2, 'receipt_id'] = None  
    processed_df.loc[2, 'vo_id'] = None
    processed_df.loc[3, 'patient_nr'] = None  
    
    return raw_df, processed_df

def test_analyze_fam_rejections(sample_data_for_rejection):
    """
    Tests if invalid FAM rows are correctly identified and separated based on criteria.
    """
    raw_df, processed_df = sample_data_for_rejection

    active_df, rejected_dict = analyze_rejections(
        raw_df=raw_df,
        processed_df=processed_df,
        criteria=REJECTION_CRITERIA_FAM
    )

    assert len(active_df) == 1 
    assert active_df.index.tolist() == [0]

    assert "avk ist ungültig (fehlt oder <= 0)" in rejected_dict
    assert "belegnr und vo_id fehlen beide" in rejected_dict
    assert "Essentielle Spalten (patnr, pzn, vo-datum, anzahl) sind unvollständig" in rejected_dict

    assert rejected_dict["avk ist ungültig (fehlt oder <= 0)"].index.tolist() == [1]

    assert rejected_dict["belegnr und vo_id fehlen beide"].index.tolist() == [2]

    assert rejected_dict["Essentielle Spalten (patnr, pzn, vo-datum, anzahl) sind unvollständig"].index.tolist() == [3]

def test_analyze_tm_rejections_raw_criteria():
    """
    Tests if raw criteria (like Botendienst PZN) are applied correctly.
    """
    raw_tm_df = pd.DataFrame({
        'PZN': ['123', '6461110', '456'],
        'other_col': [1, 2, 3]
    })
    
    botendienst_criteria = {"Botendienst-PZN (06461110)": REJECTION_CRITERIA_TM["Botendienst-PZN (06461110)"]}

    active_df, rejected_dict = analyze_rejections(
        raw_df=raw_tm_df,
        processed_df=raw_tm_df,
        criteria=botendienst_criteria,
        is_raw_criteria=True
    )
    
    assert len(active_df) == 2
    assert "Botendienst-PZN (06461110)" in rejected_dict
    assert rejected_dict["Botendienst-PZN (06461110)"].iloc[0]['PZN'] == '6461110'
