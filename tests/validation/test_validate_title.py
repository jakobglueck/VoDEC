import pandas as pd
from app.core import fam_formatter

#-- test -- avk formatter -- #
def test_format_title_column_with_valid_title_dr():

    input_series = pd.Series(["Dr."]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr."

def test_format_title_column_with_valid_title_dr_dr():

    input_series = pd.Series(["Dr. Dr."]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr. Dr."

def test_format_title_column_with_valid_title_dr_med1():

    input_series = pd.Series(["Dr. med."]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr."

def test_format_title_column_with_valid_title_dr_med2():

    input_series = pd.Series(["Dr. med"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr."

def test_format_title_column_with_valid_title_dr_dr_med():

    input_series = pd.Series(["Dr. med. Dr. med"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr. Dr." 

def test_format_title_column_with_valid_title_pd():

    input_series = pd.Series(["PD"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "PD Dr."

def test_format_title_column_with_valid_title_pd_dr_dr():

    input_series = pd.Series(["PD Dr. med Dr. med."]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "PD Dr. Dr."

def test_format_title_column_with_valid_title_prof():

    input_series = pd.Series(["Professor"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Prof. Dr."

def test_format_title_column_with_valid_title_dipl():

    input_series = pd.Series(["Dipl. med"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] is None

def test_format_title_column_with_valid_title_empty():

    input_series = pd.Series([""]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] is None

def test_format_title_column_with_valid_title_live_example1():

    input_series = pd.Series(["Dr. med. MME (U)"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr."

def test_format_title_column_with_valid_title_live_example2():

    input_series = pd.Series(["Lic./Univ. Barcelona"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] is None

def test_format_title_column_with_valid_title_live_example3():

    input_series = pd.Series(["Medico-Cirujano (Univ. Central de Venezuela)"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr."

def test_format_title_column_with_valid_title_live_example4():

    input_series = pd.Series(["Priv.-Doz. Dr.med."]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "PD Dr."

def test_format_title_column_with_valid_title_live_example5():

    input_series = pd.Series(["M.D.(SYR)"]) 

    result_series = fam_formatter.validate_doctor_title_column(input_series)

    assert result_series[0] == "Dr."