import re
import numpy as np
import pandas as pd
from datetime import datetime


def format_and_clean_name_column(name_column: pd.Series) -> pd.Series:
    """Cleans and formats a column of names (first names, last names)."""
    def clean_single_name(name):
        if pd.isna(name):
            return None

        name_str = str(name).strip()

        name_str = " ".join(name_str.split())

        if not name_str:
            return None
        if name_str.isdigit():
            return None
            
        return name_str.title()
        
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

        if len(id_str) < required_length:
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

        street_str = " ".join(str(street).split())
        
        if street_str.isdigit():
            return None
        
        street_str = re.sub(r'(strasse|straße|trasse)\b', 'str.', street_str, flags=re.IGNORECASE)
        
        titled_street = street_str.title()
        
        # function to ensure that street ads like 1b and 25a are not missleading converted (It stays 1b and not 1B)
        corrected_street = re.sub(r'(\d)([A-Z])', 
            lambda m: m.group(1) + m.group(2).lower(), 
            titled_street
        )
        
        return corrected_street

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
    pattern = '|'.join(re.escape(kw) for kw in keywords)

    def clean_single_entry(name):
        if pd.isna(name):
            return None

        if str(name).strip().isdigit(): 
           return None

        cleaned_name = re.sub(pattern, '', str(name), flags=re.IGNORECASE)

        cleaned_name = " ".join(cleaned_name.split())
        cleaned_name = cleaned_name.strip(' ,-')
        
        return cleaned_name
            
    return name_column.apply(clean_single_entry)

def process_charges_and_positions(tm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates chargen and position numbers using the correct
    order of operations to handle both patterns and duplicates.
    """
    def _calculate_charges_for_group(group: pd.DataFrame) -> pd.DataFrame:
        """Helper function to determine chargen numbers for a single vo_id group."""
        pzn_list = group['pzn'].tolist()
        block_length = 0

        if len(pzn_list) < 2:
            block_length = 1
        else:
            first_pzn = pzn_list[0]
            try:

                next_occurrence_index = pzn_list[1:].index(first_pzn)
                block_length = next_occurrence_index + 1
            except ValueError:

                block_length = len(pzn_list)

        indices = np.arange(len(group))
        group['charge_nr'] = (indices // block_length) + 1
        return group

    df = tm_df.copy()

    processed_groups = []
    for name, group in df.groupby('vo_id'):
        processed_group = _calculate_charges_for_group(group.copy())
        processed_groups.append(processed_group)

    if not processed_groups:
        return pd.DataFrame(columns=df.columns)
        
    df = pd.concat(processed_groups)

    df.drop_duplicates(subset=['vo_id', 'charge_nr', 'pzn'], keep='first', inplace=True)

    df['position'] = df.groupby(['vo_id', 'charge_nr']).cumcount() + 1
    
    return df