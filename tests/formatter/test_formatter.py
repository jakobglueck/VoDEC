import pandas as pd
import pytest
from app.core.utils import process_charges_and_positions

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
    