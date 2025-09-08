import pandas as pd
from app.core import fam_formatter

#-- test -- pharmacy owner formatter -- #
def test_format_pharmacy_owner_column_with_invalid_pharmacy_owner():

    input_series = pd.Series(["1435342313"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] is None

def test_format_pharmacy_owner_column_with_valid_pharmacy_owner_inh1():

    input_series = pd.Series(["Inh. Bernd Schmidt"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Bernd Schmidt"

def test_format_pharmacy_owner_column_with_valid_pharmacy_owner_inh2():

    input_series = pd.Series(["Inhaber Bernd Schmidt"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Bernd Schmidt"

def test_format_pharmacy_owner_column_with_valid_pharmacy_owner_eV1():

    input_series = pd.Series(["myCare e.V."])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "myCare"

def test_format_pharmacy_owner_column_with_valid_pharmacy_owner_eV2():

    input_series = pd.Series(["myCare eV"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "myCare"

def test_format_pharmacy_owner_column_with_valid_pharmacy_owner_eV3():

    input_series = pd.Series(["myCare e V"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "myCare"

def test_format_pharmacy_owner_column_with_valid_pharmacy_owner_ohg():

    input_series = pd.Series(["myCare OHG"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "myCare"

def test_owner_with_leading_and_trailing_whitespace():

    input_series = pd.Series(["  Adler Apotheke GmbH  "])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Adler Apotheke"

def test_owner_with_keyword_followed_by_comma():

    input_series = pd.Series(["Adler Apotheke GmbH,"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Adler Apotheke"

def test_owner_with_mixed_case_keywords():

    input_series = pd.Series(["Sonnen Apotheke gmbh", "Apotheke am Markt oHG"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Sonnen Apotheke"    
    assert result_series[1] == "Apotheke am Markt"

def test_owner_with_no_keywords_is_unchanged():

    input_series = pd.Series(["Apotheke am Rathaus"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Apotheke am Rathaus"

def test_owner_with_multiple_keywords():

    input_series = pd.Series(["Apotheke zum Einhorn e.K. Inhaber Max Mustermann"])

    result_series = fam_formatter.format_pharmacy_owner_column(input_series)

    assert result_series[0] == "Apotheke zum Einhorn Max Mustermann"
    