import pandas as pd
from app.core import fam_formatter
from app.core import utils

#-- test -- name splitter -- #
def test_splitter_with_simple_title():

    result = fam_formatter.split_full_name("Dr. Erika Mustermann")

    assert result["title"] == "Dr."
    assert result["first_name"] == "Erika"
    assert result["last_name"] == "Mustermann"

def test_splitter_with_complex_title():

    result = fam_formatter.split_full_name("Prof. Dr. Peter Pan")

    assert result["title"] == "Prof. Dr."
    assert result["first_name"] == "Peter"
    assert result["last_name"] == "Pan"

def test_splitter_with_name_prefix():

    result = fam_formatter.split_full_name("Jan de Vries")

    assert result["title"] == ""
    assert result["first_name"] == "Jan"
    assert result["last_name"] == "de Vries"

def test_splitter_with_comma_separated_name():

    result = fam_formatter.split_full_name("Mustermann, Max")

    assert result["title"] == ""
    assert result["first_name"] == "Max"
    assert result["last_name"] == "Mustermann"

def test_splitter_with_middle_name():

    result = fam_formatter.split_full_name("James Tiberius Kirk")
    assert result["first_name"] == "James Tiberius"
    assert result["last_name"] == "Kirk"

def test_splitter_with_empty_and_none_input():

    result_none = fam_formatter.split_full_name(None)

    result_empty = fam_formatter.split_full_name("   ")
    assert result_none["first_name"] == ""
    assert result_empty["first_name"] == ""

def test_full_name_processing_pipeline():
    data = {'full_name': ["PROF. DR. max von der LIPPE"]}
    df = pd.DataFrame(data)

    split_results = df['full_name'].apply(fam_formatter.split_full_name)

    name_df = split_results.apply(pd.Series)
    df = pd.concat([df, name_df], axis=1)

    df['title'] = fam_formatter.validate_doctor_title_column(df['title'])
    df['first_name'] = utils.format_and_clean_name_column(df['first_name'])
    df['last_name'] = utils.format_and_clean_name_column(df['last_name'])

    assert df.loc[0, 'title'] == "Prof. Dr."
    assert df.loc[0, 'first_name'] == "Max"
    assert df.loc[0, 'last_name'] == "Von Der Lippe"

def test_full_name_processing_pipeline_live_example():
    data = {'full_name': ["Priv.-Doz. Dr. med. Arndt Petermann"]}
    df = pd.DataFrame(data)

    split_results = df['full_name'].apply(fam_formatter.split_full_name)

    name_df = split_results.apply(pd.Series)
    df = pd.concat([df, name_df], axis=1)

    df['title'] = fam_formatter.validate_doctor_title_column(df['title'])
    df['first_name'] = utils.format_and_clean_name_column(df['first_name'])
    df['last_name'] = utils.format_and_clean_name_column(df['last_name'])
    print(   df['title'] )
    assert df.loc[0, 'title'] == "PD Dr."
    assert df.loc[0, 'first_name'] == "Arndt"
    assert df.loc[0, 'last_name'] == "Petermann"

def test_full_name_processing_pipeline_live_example2():
    data = {'full_name': ["Abdelrahim Dr. med. Omar"]}
    df = pd.DataFrame(data)

    split_results = df['full_name'].apply(fam_formatter.split_full_name)

    name_df = split_results.apply(pd.Series)
    df = pd.concat([df, name_df], axis=1)

    df['title'] = fam_formatter.validate_doctor_title_column(df['title'])
    df['first_name'] = utils.format_and_clean_name_column(df['first_name'])
    df['last_name'] = utils.format_and_clean_name_column(df['last_name'])
    print(   df['title'] )
    assert df.loc[0, 'title'] == "Dr."
    assert df.loc[0, 'first_name'] == "Omar"
    assert df.loc[0, 'last_name'] == "Abdelrahim"

def test_full_name_processing_pipeline_live_example2():
    data = {'full_name': ["Palliativnetz Ludwigslust-Parchim GmbH"]}
    df = pd.DataFrame(data)

    split_results = df['full_name'].apply(fam_formatter.split_full_name)

    name_df = split_results.apply(pd.Series)
    df = pd.concat([df, name_df], axis=1)

    df['title'] = fam_formatter.validate_doctor_title_column(df['title'])
    df['first_name'] = utils.format_and_clean_name_column(df['first_name'])
    df['last_name'] = utils.format_and_clean_name_column(df['last_name'])
    print(   df['title'] )
    assert df.loc[0, 'title'] is None
    assert df.loc[0, 'first_name'] is None
    assert df.loc[0, 'last_name'] is None

def test_full_name_processing_pipeline_live_example3():
    data = {'full_name': ["Zech Ulrike"]}
    df = pd.DataFrame(data)

    split_results = df['full_name'].apply(fam_formatter.split_full_name)

    name_df = split_results.apply(pd.Series)
    df = pd.concat([df, name_df], axis=1)

    df['title'] = fam_formatter.validate_doctor_title_column(df['title'])
    df['first_name'] = utils.format_and_clean_name_column(df['first_name'])
    df['last_name'] = utils.format_and_clean_name_column(df['last_name'])
    print(   df['title'] )
    assert df.loc[0, 'title'] is None
    assert df.loc[0, 'first_name'] == "Ulrike"
    assert df.loc[0, 'last_name'] == "Zech"
    