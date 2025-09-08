
import pandas as pd
from app.core import utils

#-- test -- Name formatter -- #
def test_format_name_column_with_valid_name():

    input_series = pd.Series(["MAX MUSTERMANN"])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] == "Max Mustermann"

def test_format_name_column_with_upper_and_lower_case():

    input_series = pd.Series(["MaX MuSTERmANN"])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] == "Max Mustermann"

def test_format_name_column_with_numeric_input():

    input_series = pd.Series(["12345"])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] is None

def test_format_name_column_with_empty_input():

    input_series = pd.Series([None, "   "])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] is None
    assert result_series[1] is None

def test_format_name_column_with_punctuation():

    input_series = pd.Series(["klaus-peter", "dr. müller"])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] == "Klaus-Peter"
    assert result_series[1] == "Dr. Müller"

def test_format_name_column_with_alphanumeric_input():

    input_series = pd.Series(["Apollo13", "Musterfrau 2"])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] == "Apollo13"
    assert result_series[1] == "Musterfrau 2"

def test_format_name_column_with_extra_whitespace():
    input_series = pd.Series(["  max mustermann  ", "", "erika   musterfrau"])

    result_series = utils.format_and_clean_name_column(input_series)

    assert result_series[0] == "Max Mustermann"
    assert result_series[1] is None
    assert result_series[2] == "Erika Musterfrau"
