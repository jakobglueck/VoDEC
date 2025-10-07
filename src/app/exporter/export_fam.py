from typing import Dict, List
import pandas as pd

from app.model.fam import FAMModel

REVERSE_FAM_HEADER_MAPPING: Dict[str, str] = {
    "health_insurance_company": "kasse",
    "patient_nr": "patnr",
    "pzn": "pzn",
    "medicine_name": "am-name",
    "medicine_price": "avk",
    "prescription_date": "vo-datum",
    "amount": "anzahl",
    "lanr": "lanr",
    "doctor_title": "arzt-titel",
    "doctor_first_name": "arzt-vorname",
    "doctor_last_name": "arzt-nachname",
    "doctor_phone": "arzt-tel",
    "kv_district": "kv-bezirk",
    "doctor_specialization": "FA-Bezeichnung",
    "role": "rolle",
    "billing_date": "abrdatum",
    "temp_lanr": "lanrtmp",
    "receipt_id": "belegnr",
    "doctor_id": "arzt-id",
    "pharmacy_name": "apo-name",
    "pharmacy_owner": "apo-inhaber",
    "bs_nr": "bsnr",
    "bs_name": "betriebsbez.",
    "ihpe_units": "applikationsfertige Einheiten",
    "vo_id": "vo-id"
}

FINAL_COLUMN_ORDER: List[str] = [
    "kasse", "patnr", "pzn", "am-name", "avk", "vo-datum", "anzahl", "lanr",
    "arzt-titel", "arzt-vorname", "arzt-nachname", "arzt-str", "arzt-plz",
    "arzt-ort", "apo-name", "apo-plz", "apo-ort", "bsnr", "betriebsbez.",
    "apo-str", "arzt-tel", "kv-bezirk", "FA-Bezeichnung", "rolle", "abrdatum",
    "lanrtmp", "belegnr", "arzt-id", "apo-inhaber",
    "applikationsfertige Einheiten", "vo-id"
]

def build_fam_exporter(data: List[FAMModel], output_path: str) -> pd.DataFrame:
    if not data:
        print("No FAM-Data to export.")
        return

    data_as_dicts = [model.model_dump() for model in data]

    df = pd.DataFrame(data_as_dicts)

    if 'doctor_address' in df.columns:
        doctor_address_df = pd.json_normalize(df['doctor_address'])
        doctor_address_df = doctor_address_df.rename(columns={
            "street": "arzt-str",
            "postcode": "arzt-plz",
            "city": "arzt-ort"
        })
        df = pd.concat([df.drop('doctor_address', axis=1), doctor_address_df], axis=1)

    if 'pharmacy_address' in df.columns:
        pharmacy_address_df = pd.json_normalize(df['pharmacy_address'])
        pharmacy_address_df = pharmacy_address_df.rename(columns={
            "street": "apo-str",
            "postcode": "apo-plz",
            "city": "apo-ort"
        })
        df = pd.concat([df.drop('pharmacy_address', axis=1), pharmacy_address_df], axis=1)

    df.rename(columns=REVERSE_FAM_HEADER_MAPPING, inplace=True)

    for col in FINAL_COLUMN_ORDER:
        if col not in df.columns:
            df[col] = None

    final_df = df[FINAL_COLUMN_ORDER]

    final_df.to_excel(output_path, index=False)
