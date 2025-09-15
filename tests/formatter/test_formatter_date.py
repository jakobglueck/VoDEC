import pandas as pd
from app.core import fam_formatter
from datetime import datetime, timedelta

def test_date_with_valid_ddmmyyyy_format():

    input_series = pd.Series(["08.09.2025"]) 

    result_series = fam_formatter.validate_prescription_date_column(input_series)

    assert result_series[0] == "08.09.2025"

def test_date_with_various_valid_formats():

    input_series = pd.Series(["20241130"]) 

    result_series = fam_formatter.validate_prescription_date_column(input_series)

    assert result_series[0] == "30.11.2024"

def test_date_with_various_valid_formats():

    input_series = pd.Series(["20241130","20240930"]) 

    result_series = fam_formatter.validate_prescription_date_column(input_series)

    assert result_series[0] == "30.11.2024"
    assert result_series[1] == "30.09.2024"

def test_date_that_is_too_old_is_invalid():

    two_years_ago = datetime.now() - timedelta(days=731) 

    date_str = two_years_ago.strftime("%d.%m.%Y")
    
    input_series = pd.Series([date_str])

    result_series = fam_formatter.validate_prescription_date_column(input_series)

    assert result_series[0] is None

def test_date_in_the_future_is_invalid():

    tomorrow = datetime.now() + timedelta(days=1)

    date_str = tomorrow.strftime("%d.%m.%Y")

    input_series = pd.Series([date_str])

    result_series = fam_formatter.validate_prescription_date_column(input_series)

    assert result_series[0] is None

def test_date_with_invalid_and_empty_formats():

    input_series = pd.Series(["not a date", None, "   ", "32.13.2024"])

    result_series = fam_formatter.validate_prescription_date_column(input_series)

    assert result_series[0] is None
    assert result_series[1] is None
    assert result_series[2] is None
    assert result_series[3] is None
