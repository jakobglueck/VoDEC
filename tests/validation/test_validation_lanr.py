import pandas as pd
from app.core import utils

#-- test -- lanr formatter -- #
def test_format_lanr_column_with_valid_lanr():

    input_series = pd.Series(["14353423"])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] == "14353423"

def test_format_lanr_column_with_invalid_lanr_1():

    input_series = pd.Series(["9999123"])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] is None

def test_format_lanr_column_with_invalid_lanr_2():

    input_series = pd.Series(["33333330"])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] is None


def test_format_lanr_column_with_short_lanr():

    input_series = pd.Series(["14323"])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] is None

def test_format_lanr_column_with_empyt_lanr():

    input_series = pd.Series([""])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] is None

def test_format_lanr_column_with_alpabethic_lanr():

    input_series = pd.Series(["anc"])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] is None


def test_format_lanr_column_with_normal_lanr():

    input_series = pd.Series(["123456"])

    result_series = utils.validate_id_number_column(input_series,6)

    assert result_series[0] == "123456"
