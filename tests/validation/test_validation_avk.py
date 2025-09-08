import pandas as pd
from app.core import fam_formatter

#-- test -- avk formatter -- #
def test_format_avk_column_with_valid_avk_with_comma():

    input_series = pd.Series(["100,90"]) 

    result_series = fam_formatter.validate_medicine_price_column(input_series)

    assert result_series[0] == 100.90

def test_format_avk_column_with_valid_avk_with_currency():

    input_series = pd.Series(["100,90€"]) 

    result_series = fam_formatter.validate_medicine_price_column(input_series)

    assert result_series[0] == 100.90


def test_format_avk_column_with_invalid_avk():

    input_series = pd.Series(["-100,90€"]) 

    result_series = fam_formatter.validate_medicine_price_column(input_series)

    assert result_series[0] is None

def test_format_avk_column_with_valid_avk_with_currency():

    input_series = pd.Series(["0,00"]) 

    result_series = fam_formatter.validate_medicine_price_column(input_series)

    assert result_series[0] is None
