import pandas as pd
import pytest
from app.core.utils import process_charges_and_positions, add_validation_column, update_medicine_name_for_specific_pzn

def test_charge_position_with_real_data_scenario():
    """
    Test 1: Uses a simple list of unique PZNs, mimicking your real data.
    It should result in one single batch with sequential positions.
    """
    input_data = {
        'vo_id': ['V1', 'V1', 'V1'],
        'pzn':   ['14038870', '7223417', '4253443']
    }
    input_df = pd.DataFrame(input_data)

    result_df = process_charges_and_positions(input_df)

    assert result_df['charge_nr'].tolist() == [1, 1, 1]
    assert result_df['position'].tolist() == [1, 2, 3]

def test_charge_position_with_duplicates_in_batch():
    """
    Test 2: Includes a duplicate PZN within a single batch.
    The function should drop the duplicate.
    """
    input_data = {
        'vo_id': ['V2', 'V2', 'V2', 'V2'],
        'pzn':   ['A', 'B', 'B', 'C']
    }
    input_df = pd.DataFrame(input_data)

    result_df = process_charges_and_positions(input_df)

    assert result_df['pzn'].tolist() == ['A', 'B', 'C']
    assert result_df['charge_nr'].tolist() == [1, 1, 1]
    assert result_df['position'].tolist() == [1, 2, 3]

def test_charge_position_overwrites_existing_data():
    """
    Test 3: The input DataFrame already has incorrect charge/position numbers.
    The function should ignore them and calculate the correct new ones.
    """

    input_data = {
        'vo_id': ['V3', 'V3'],
        'pzn':   ['X', 'Y'],
        'charge_nr': [99, 99],
        'position': [5, 6]
    }
    input_df = pd.DataFrame(input_data)

    result_df = process_charges_and_positions(input_df)

    assert result_df['charge_nr'].tolist() == [1, 1]
    assert result_df['position'].tolist() == [1, 2]

def test_charge_position_with_three_batches():
    """
    Test 4: Uses a long list of PZNs with a repeating pattern
    to ensure that three distinct batches are correctly calculated.
    """

    input_data = {
        'vo_id': ['V4'] * 6, # 6 rows for the same vo_id
        'pzn':   ['A', 'B', 'A', 'B', 'A', 'B']
    }
    input_df = pd.DataFrame(input_data)

    result_df = process_charges_and_positions(input_df)

    assert result_df['charge_nr'].tolist() == [1, 1, 2, 2, 3, 3]

    assert result_df['position'].tolist() == [1, 2, 1, 2, 1, 2]

def test_update_medicine_name_for_specific_pzn():
    """Tests the normal case where a matching PZN is found and updated."""

    input_data = {
        'pzn': ['1234567', '9999100', '8765432'],
        'medicine_name': ['Addel Trace', 'Old Name', 'Kabiven Emuls Iv Inf 3-Kb']
    }
    df = pd.DataFrame(input_data)

    result_df = update_medicine_name_for_specific_pzn(df)

    assert result_df.loc[0, 'medicine_name'] == 'Addel Trace'
    assert result_df.loc[1, 'medicine_name'] == 'Par. Ernährung (reg.)'
    assert result_df.loc[2, 'medicine_name'] == 'Kabiven Emuls Iv Inf 3-Kb'

def test_add_validation_column_scenarios():
    """
    Tests all validation rules of the add_validation_column function.
    """
    input_data = {
        'patient_nr':          ['P1',  None, 'P3', 'P4', 'P5', 'P5', 'P7'],
        'pzn':                 ['Z1',  'Z2', 'Z3', 'Z4', 'Z5', 'Z5', 'Z7'],
        'medicine_price':      [10.5,  20.0, 0.00, 30.0, 40.0, 40.0, 50.0],
        'prescription_date':   ['01.09.2025', '02.09.2025', '03.09.2025', '04.09.2025', '05.09.2025', '05.09.2025', '06.09.2025'],
        'amount':              [1,     2,    3,    4,    5,    5,    None],
        'receipt_id':          ['R1',  'R2', 'R3', None, 'R5', 'R5', 'R7'],
        'vo_id':               ['V1',  'V2', 'V3', None, 'V5', 'V5', 'V7']
    }
    df = pd.DataFrame(input_data)

    result_df = add_validation_column(df)

    assert result_df.loc[0, 'valid'] == True
    assert result_df.loc[1, 'valid'] == False
    assert result_df.loc[2, 'valid'] == False
    assert result_df.loc[3, 'valid'] == False
    assert result_df.loc[4, 'valid'] == False
    assert result_df.loc[5, 'valid'] == False
    assert result_df.loc[6, 'valid'] == False
