import pandas as pd
from app.core import utils

#-- test -- street formatter -- #
def test_format_street_column_with_valid_street_ß():

    input_series = pd.Series(["Leipziger Straße 5"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Leipziger Str. 5"

def test_format_street_column_with_valid_street_ß():

    input_series = pd.Series(["Olympiastraße 5"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Olympiastr. 5"

def test_format_street_column_with_valid_street_ss():

    input_series = pd.Series(["Leipziger Strasse 5"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Leipziger Str. 5"

def test_format_street_column_with_valid_street_ß():

    input_series = pd.Series(["Olympiastrasse 5"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Olympiastr. 5"


def test_format_street_column_with_invalid_street():

    input_series = pd.Series(["979789"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] is None

def test_format_street_column_with_short_street():

    input_series = pd.Series(["Leipziger Str. 5"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Leipziger Str. 5"

def test_format_street_column_with_short_street():

    input_series = pd.Series(["Weg 1b"])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Weg 1b"

def test_format_street_column_with_whitespace():

    input_series = pd.Series(["  Weg     1b  "])

    result_series = utils.validate_street_column(input_series)

    assert result_series[0] == "Weg 1b"
