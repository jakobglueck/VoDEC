import pandas as pd
from app.core import utils

#-- test -- city formatter -- #
def test_format_city_column_with_valid_city():

    input_series = pd.Series(["Leipzig"])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] == "Leipzig"

def test_format_city_column_with_valid_city():

    input_series = pd.Series(["Leipzig", "Chemnitz"])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] == "Leipzig"
    assert result_series[1] == "Chemnitz"


def test_format_city_column_with_invalid_city():

    input_series = pd.Series(["979789"])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] is None

def test_format_city_column_with_short_city():

    input_series = pd.Series(["Wien"])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] == "Wien"

def test_format_city_column_with_low_case_city():

    input_series = pd.Series(["leipzig"])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] == "Leipzig"

def test_format_city_column_with_whitespace():

    input_series = pd.Series(["  Leipzig  "])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] == "Leipzig"

def test_format_city_column_with_whitespace_between():

    input_series = pd.Series(["  Bad Frankenhausen  "])

    result_series = utils.validate_city_column(input_series)

    assert result_series[0] == "Bad Frankenhausen"
