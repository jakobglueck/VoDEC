import re
import pandas as pd
from datetime import datetime


def format_and_clean_name_column(name_column: pd.Series) -> pd.Series:
    """Cleans and formats a column of names (first names, last names)."""
    def clean_single_name(name):
        if pd.isna(name) or not str(name).strip():
            return None
        
        if str(name).strip().isdigit(): 
            return None
        
        return str(name).title()
    return name_column.apply(clean_single_name)

def validate_plz_column(plz_column: pd.Series) -> pd.Series:
    """Validates and cleans a column of German postal codes (for doctors, pharmacies)."""
    def validate_single_plz(plz):
        if pd.isna(plz):
            return None
        plz_str = str(plz).split('.')[0].strip()

        if len(plz_str) == 4 and plz_str.isdigit():
            plz_str = "0" + plz_str

        if len(plz_str) == 5 and plz_str.isdigit():
            return plz_str
        
        else:
            return None
    return plz_column.apply(validate_single_plz)

def validate_id_number_column(id_column: pd.Series, required_length: int) -> pd.Series:
    """
    Validates a column of numeric ID numbers based on a specified length
    and a rule against repeating digits.
    - Must be a pure number.
    - Must have the exact required_length.
    - Must not contain the same digit repeated four or more times.
    - Invalid or empty entries are converted to None.
    """
    
    def validate_single_id(id_value):

        if pd.isna(id_value):
            return None

        id_str = str(id_value).split('.')[0].strip()
        
        if not id_str.isdigit():
            return None

        if len(id_str) != required_length:
            return None

        if re.search(r'(\d)\1{3,}', id_str):
            return None

        return id_str
            
    return id_column.apply(validate_single_id)

def validate_street_column(street_column: pd.Series) -> pd.Series:
    """Validates and cleans a column of street names (for doctors, pharmacies)."""
    def validate_single_plz(street):
        if pd.isna(street) or not str(street).strip():
            return None

        street_str = str(street).strip()
        
        if street_str.isdigit():
            return None
        
        street_str = re.sub(r'\b(strasse|straße|trasse)\b', 'str.', street_str, flags=re.IGNORECASE)
        
        return street_str
    return street_column.apply(validate_single_plz)

def validate_city_column(city_column: pd.Series) -> pd.Series:
    """Validates and cleans a column of city names (for doctors, pharmacies)."""
    def validate_single_plz(city):
        if pd.isna(city) or not str(city).strip():
            return None

        city_str = str(city).strip()

        if city_str.isdigit():
            return None

        return city_str.title()
    return city_column.apply(validate_single_plz)

def remove_keywords_from_column(name_column: pd.Series, keywords: list[str]) -> pd.Series:
    """
    Generic utility to remove a list of specified keywords from a Series of strings.
    """

    pattern = r'\b(' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'

    def clean_single_entry(name):
        if pd.isna(name):
            return None

        cleaned_name = re.sub(pattern, '', str(name), flags=re.IGNORECASE)
      
        cleaned_name = " ".join(cleaned_name.split()) 
        cleaned_name = cleaned_name.strip(' ,-')
        
        return cleaned_name
            
    return name_column.apply(clean_single_entry)