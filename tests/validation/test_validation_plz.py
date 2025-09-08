import pandas as pd
from app.core import utils

#-- test -- plz formatter -- #
def test_format_plz_column_with_valid_plz():

    input_series = pd.Series(["06618"])

    result_series = utils.validate_plz_column(input_series)

    assert result_series[0] == "06618"

def test_format_plz_column_with_invalid_plz():

    input_series = pd.Series(["979789"])

    result_series = utils.validate_plz_column(input_series)

    assert result_series[0] is None

def test_format_plz_column_with_short_plz():

    input_series = pd.Series(["6618"])

    result_series = utils.validate_plz_column(input_series)

    assert result_series[0] == "06618"

def test_format_plz_column_with_short_plz():

    input_series = pd.Series(["PLZ"])

    result_series = utils.validate_plz_column(input_series)

    assert result_series[0] is None

def test_format_plz_column_with_whitespace():

    input_series = pd.Series(["  06618  "])

    result_series = utils.validate_plz_column(input_series)

    assert result_series[0] == "06618"

def test_format_plz_column_with_alphanumeric_input():

    input_series = pd.Series(["D-06618", "09111A"])

    result_series = utils.validate_plz_column(input_series)

    assert result_series[0] is None
    assert result_series[1] is None