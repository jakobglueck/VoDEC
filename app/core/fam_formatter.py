
import pandas as pd

from model.fam import FAMModel

FAM_HEADER_MAPPING = {
    "kasse": "health_insurance_company",
    "patnr": "patient_nr",
    "pzn": "pzn",
    "am-name": "medicine_name",
    "avk": "medicine_price",
    "vo-datum": "prescription_date",
    "anzahl": "amount",
    "lanr": "lanr",
    "arzt-titel": "doctor_title",
    "arzt-vorname": "doctor_first_name",
    "arzt-nachname": "doctor_last_name",
    "arzt-str": "street",
    "arzt-plz": "postcode",
    "arzt-ort": "city",
    "apo-name": "pharmacy_name",
    "apo-plz": "postcode",
    "apo-ort": "city",
    "bsnr": "bs_nr",
    "betriebsbez.": "bs_name",
    "apo-str": "street",
    "arzt-tel": "doctor_phone",
    "kv-bezirk": "kv_district",
    "FA-Bezeichnung": "doctor_specialization",
    "rolle": "role",
    "abrdatum": "billing_date",
    "lanrtmp": "temp_lanr",
    "belegnr": "receipt_id",
    "arzt-id": "doctor_id",
    "apo-inhaber": "pharmacy_owner",
    "applikationsfertige Einheiten": "ihpe_units",
    "vo-id": "vo_id"
}

def format_fam_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and formats the raw FAM DataFrame.
    - Renames headers based on the mapping.
    - Selects ONLY the columns defined in the mapping.
    - Performs basic data type conversions and cleaning.
    """
    formatted_df = raw_df.rename(columns=FAM_HEADER_MAPPING)

    final_columns_to_keep = list(FAM_HEADER_MAPPING.values())

    final_df = formatted_df[final_columns_to_keep]
    
    return final_df
