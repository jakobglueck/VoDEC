import pandas as pd
import pytest
from app.core.utils import check_placeholder_or_incorrect_input_characters

def test_placeholder_with_real_data_scenario():
    """
    test to check if the function check_placeholder_or_incorrect_input_characters will mark the right values
    """
    input_data = {
        'ID': [1, 2, 3, 4, 5, 6, 7],
        'Produkt': ['Apfel', 'Banane', ' ', 'Dattel', 'Erdbeere', 'Feige', 'Granatapfel'],
        'Verfügbarkeit': ['Ja', 'Nein', '?', 'Ja', 'NA', 'Ja', 'NULL'],
        'Preis': ['1.99', '2.50', '3.00', 'N/A', '5.50', '-', '1.20'],
        'Menge': [10, 20, 5, 15, 30, 25, 'Not a Number']
    }

    input_df = pd.DataFrame(input_data)

    result_df = check_placeholder_or_incorrect_input_characters(input_df)

    print(result_df)

    expected_data = {
        'ID': [1, 2, 3, 4, 5, 6, 7],
        'Produkt': ['Apfel', 'Banane', None, 'Dattel', 'Erdbeere', 'Feige', 'Granatapfel'],
        'Verfügbarkeit': ['Ja', 'Nein', None, 'Ja', None, 'Ja', None],
        'Preis': ['1.99', '2.50', '3.00', None, '5.50', None, '1.20'],
        'Menge': [10, 20, 5, 15, 30, 25, None]
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['Menge'] = expected_df['Menge'].astype(object)

    pd.testing.assert_frame_equal(result_df, expected_df)

def test_placeholder_with_real_data_scenario_placeholder_in_names():
    """
    test to check if the function check_placeholder_or_incorrect_input_characters will mark the right values in names etc. 
    """
    input_data = {
        'Name': ['Peter', 'Heinz-Karl', '-', 'Sven-Ole', '  -  ', 'N/A'],
        'Status': ['Aktiv', 'Inaktiv', 'Aktiv', 'Aktiv', '?', '']
    }

    input_df = pd.DataFrame(input_data)

    result_df = check_placeholder_or_incorrect_input_characters(input_df)

    print(result_df)

    expected_data = {
        'Name': ['Peter', 'Heinz-Karl', None, 'Sven-Ole', None, None],
        'Status': ['Aktiv', 'Inaktiv', 'Aktiv', 'Aktiv', None, None]
    }

    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result_df, expected_df)
