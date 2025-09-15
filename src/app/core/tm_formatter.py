import pandas as pd

from app.model.tm import TMModel

TM_HEADER_MAPPING = {
    "VO-ID": "vo_id",
    "Chargen-Nr.": "charge_nr",
    "Position/laufende Nr.": "position",
    "PZN": "pzn",
    "Bezeichnung": "am_name",
    "Faktorenkennzeichen": "factor_indicator",
    "Mengenfaktor": "quantity_factor",
    "Preiskennzeichen": "price_indicator",
    "Teilmengenpreis": "partial_quantity_price",
    "Packungsgröße": "package_size",
    "Mengeneinheit": "unit_of_measurement",
    "Darreichungsform": "presentation_form",
    "ATC-Code": "atc_code",
    "ATC-Bezeichnung": "atc_name"
}

def format_tm_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and formats the raw TM DataFrame.
    - Renames headers based on the mapping.
    - Selects ONLY the columns defined in the mapping.
    - Performs basic data type conversions and cleaning.
    """
    formatted_df = raw_df.rename(columns=TM_HEADER_MAPPING)

    final_columns_to_keep = list(TM_HEADER_MAPPING.values())

    final_df = formatted_df[final_columns_to_keep]

    return final_df

def validate_tm_medicine_name_column(am_name: pd.Series) -> pd.Series:
    """Formats medicine names to proper case."""
    def validate_single_medicine_name(am_name):
        if pd.isna(am_name) or not str(am_name).strip():
            return None
        
        return str(am_name).title()
    return am_name.apply(validate_single_medicine_name)

def validate_tm_charge_nr_column(charge_nr: pd.Series) -> pd.Series:
    """Formats charge numbers to proper case."""
    def validate_single_charge_nr(charge_nr):
        if pd.isna(charge_nr) or not str(charge_nr).strip():
            return None
        
        return str(charge_nr).title()
    return charge_nr.apply(validate_single_charge_nr)

def validate_tm_position_column(position: pd.Series) -> pd.Series:
    """Validates that the position is a valid integer."""
    def validate_single_position(pos):
        if pd.isna(pos):
            return None

        pos_str = str(pos).split('.')[0] 
        
        if pos_str.isdigit():
            return int(pos_str)
        return None
    return position.apply(validate_single_position)

def validate_tm_factor_indicator_column(factor_indicator: pd.Series) -> pd.Series:
    """Validates that the factor indicator is a valid integer."""

    def validate_single_factor_indicator(indicator):
        if pd.isna(indicator):
            return None
        
        indicator_str = str(indicator).split('.')[0]

        if indicator_str.isdigit():
            return int(indicator_str)
        return None
    return factor_indicator.apply(validate_single_factor_indicator)

def validate_tm_normalize_quantity_factor_column(quantity_factor_column: pd.Series, promille_threshold: int = 100) -> pd.Series:
    """Normalizes the quantity factor column (handles promille)."""
    numeric_column = pd.to_numeric(quantity_factor_column, errors='coerce')

    if numeric_column.notna().any() and numeric_column.max() > promille_threshold:
        converted_column = numeric_column / 1000
        return converted_column.round(4)
    return numeric_column.round(4)

def validate_tm_price_indicator_column(price_indicator: pd.Series) -> pd.Series:
    """Validates that the price indicator is a valid integer."""
    def validate_single_price_indicator(indicator):
        if pd.isna(indicator):
            return None
        
        indicator_str = str(indicator).split('.')[0]

        if indicator_str.isdigit():
            return int(indicator_str)
        return None
    return price_indicator.apply(validate_single_price_indicator)

def validate_tm_partial_quantity_price_column(partial_quantity_price: pd.Series) -> pd.Series:
    """Validates that the price is a valid number and rounds it."""
    def validate_single_partial_quantity_price(price):
        if pd.isna(price):
            return None

        try:
            price_float = float(price)
            return round(price_float, 2)
        except (ValueError, TypeError):
            return None
    return partial_quantity_price.apply(validate_single_partial_quantity_price)
