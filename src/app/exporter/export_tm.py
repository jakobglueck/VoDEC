import pandas as pd
from typing import List, Dict
from app.model.tm import TMModel

REVERSE_TM_HEADER_MAPPING: Dict[str, str] = {
    "vo_id": "VO-ID",
    "charge_nr": "Chargen-Nr.",
    "position": "Position/laufende Nr.",
    "pzn": "PZN",
    "am_name": "Bezeichnung",
    "factor_indicator": "Faktorenkennzeichen",
    "quantity_factor": "Mengenfaktor",
    "price_indicator": "Preiskennzeichen",
    "partial_quantity_price": "Teilmengenpreis",
    "package_size": "Packungsgröße",
    "unit_of_measurement": "Mengeneinheit",
    "presentation_form": "Darreichungsform",
    "atc_code": "ATC-Code",
    "atc_name": "ATC-Bezeichnung"
}

FINAL_TM_COLUMN_ORDER: List[str] = [
    "VO-ID", "Chargen-Nr.", "Position/laufende Nr.", "PZN", "Bezeichnung",
    "Faktorenkennzeichen", "Mengenfaktor", "Preiskennzeichen", "Teilmengenpreis",
    "Packungsgröße", "Mengeneinheit", "Darreichungsform", "ATC-Code", "ATC-Bezeichnung"
]

def export_tm_data(processed_data: List[TMModel], output_path: str):

    if not processed_data:
        print("No TM-Data to export.")
        return

    data_as_dicts = [model.model_dump() for model in processed_data]

    df = pd.DataFrame(data_as_dicts)

    df.rename(columns=REVERSE_TM_HEADER_MAPPING, inplace=True)

    for col in FINAL_TM_COLUMN_ORDER:
        if col not in df.columns:
            df[col] = None 

    final_df = df[FINAL_TM_COLUMN_ORDER]

    final_df.to_excel(output_path, index=False, sheet_name="TM aufbereitet")

