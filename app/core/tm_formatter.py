
import pandas as pd

from model.tm import TMModel

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



