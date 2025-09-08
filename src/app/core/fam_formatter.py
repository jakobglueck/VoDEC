
from datetime import datetime
import re
import pandas as pd
from nameparser import HumanName

from app.model.fam import FAMModel
from app.core import utils 

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

def validate_medicine_name_column(medicine_name: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are in the right format like a Grosse2 excel function.
    """

    def validate_single_medicine_name(medicine_name):
        if pd.isna(medicine_name) or not str(medicine_name).strip():
            return None
        
        return str(medicine_name).title()
    return medicine_name.apply(validate_single_medicine_name)

def validate_prescription_date_column(date_column: pd.Series) -> pd.Series:
    """
    Parses, validates, and formats a column of dates.
    """

    parsed_dates = pd.to_datetime(date_column, format='%d.%m.%Y', errors='coerce')

    failed_mask = parsed_dates.isna()
    if failed_mask.any():
        parsed_dates.loc[failed_mask] = pd.to_datetime(
            date_column[failed_mask], errors='coerce', dayfirst=True
        )

    today = pd.Timestamp.now()
    two_years_ago = today - pd.DateOffset(years=2)
    parsed_dates.loc[(parsed_dates < two_years_ago) | (parsed_dates > today)] = pd.NaT

    formatted_dates = parsed_dates.dt.strftime('%d.%m.%Y')
    
    return formatted_dates.where(pd.notna(formatted_dates), None)

def validate_medicine_price_column(medicine_price: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are real prices with greater than 0.
    """

    def validate_medicine_price(medicine_price):
        if pd.isna(medicine_price):
                    return None

        price_str = str(medicine_price).replace('€', '').strip()
        price_str = price_str.replace('.', '').replace(',', '.')
        
        try:
            price_float = float(price_str)

            if price_float > 0:
                return price_float
            else:
                return None
        except (ValueError, TypeError):
            return None    
    return medicine_price.apply(validate_medicine_price)

def validate_amount_column(amount: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are in greater 0.
    """

    def validate_single_amount(amount):
        if pd.isna(amount):
            return None
        try:
            amount_int = int(float(amount))
        except (ValueError, TypeError):
            return None

        if amount_int >= 1:
            return amount_int
        else:
            return None
    return amount.apply(validate_single_amount)

def validate_doctor_title_column(doctor_title: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are are valid doctor titles.
    """

    def validate_single_doctor_title(doctor_title):

        if pd.isna(doctor_title) or not str(doctor_title).strip():
            return None 

        check_str = str(doctor_title).lower().replace('.', '').replace(' ', '')

        dr_keywords = ['dr', 'doctor', 'mudr', 'md', 'mbbs', 'dott', 'doktor', 'dr ', 'medico']
        prof_keywords = ('prof', 'professor')
        pd_keywords = ('pd', 'privatdozent', 'priv')

        has_prof = any(kw in check_str for kw in prof_keywords)
        has_pd = any(kw in check_str for kw in pd_keywords)

        dr_pattern = '|'.join(dr_keywords)
        dr_count = len(re.findall(dr_pattern, check_str, flags=re.IGNORECASE))

        if has_prof:
            if dr_count >= 2: return "Prof. Dr. Dr."
            if dr_count == 1: return "Prof. Dr."
            return "Prof. Dr."
        elif has_pd:
            if dr_count >= 2: return "PD Dr. Dr."
            if dr_count == 1: return "PD Dr."
            return "PD Dr."
        elif dr_count >= 2:
            return "Dr. Dr."
        elif dr_count == 1:
            return "Dr."
        return None
    return doctor_title.apply(validate_single_doctor_title)

def format_pharmacy_name_column(name_column: pd.Series) -> pd.Series:
    """Cleans the pharmacy name column by removing business suffixes."""
    PHARMACY_NAME_KEYWORDS = [
    "e.K.", "e. K.", "e.K ", "e. K", "B.V.", "PE", "Filiale", "e.Kfm",
    "e. Kfm", "e.Kfr.", "Zytostatika", "eK", "OHG", "oHG", "gGmbH", 
    "GmbH", "Inh.", "Inhaber"
    ]

    return utils.remove_keywords_from_column(name_column, keywords=PHARMACY_NAME_KEYWORDS)

def format_bs_name_column(name_column: pd.Series) -> pd.Series:
    """Cleans the bs_name column by removing various attachments."""

    BS_NAME_KEYWORDS = [
    "gGmbH", "GmbH", "e.V.", "e. V.", "e V", "e.V", "eV", "B.V.", "OHG",
    "e.Kfm", "SAPV-Team", "e. G.", "gKAöR", "§117 SGBV", "eG", "&Co.KG",
    "& Co.KG", "mbH", "+ Co.KG", "GbR", "(Entlassungsmanagement 750200598)",
    "G:", ",Entlassungsmanagement", "Entlassungsmanagement", "UG", "NULL", "#",
    "N/A", "Pseudo Pseudo-Arzt", "Pseudoarzt KH-Entlassungsmanagement", "#NV",
    "ungültiger Wert", "et. al."
    ]
    
    return utils.remove_keywords_from_column(name_column, keywords=BS_NAME_KEYWORDS)

def format_doctor_specialization_column(doctor_specialization_column: pd.Series) -> pd.Series:
    """Cleans the medical specialty column by removing boilerplate and junk values."""

    DOCTOR_SPECIALIZATION_KEYWORDS = [
    "(Facharzt)", "(Hausarzt)", "Hausarzt", "Facharzt",
    "Praktischer Arzt / Hausarzt", "F: ", "0", "unbekannt", "keine Angaben",
    "Zur freien Verfügung für die KVen (Notfallärzte etc.)",
    "Zur freien Verfügung für die KVen (Notfallärzte etc)",
    "Zur freien Verfügung für die KVen", "Sonstige Ärzte", "00", "k.A.",
    "XXX", "NULL", "nicht referenziert",
    "KV-interne Kennzeichnung, z.B. Notfallärzte",
    "Nicht zugeordnet", "ungültiger Wert", "zur freien Verfügung",
    "ungültige Facharztgruppe", "(SP)", "KV-interne Vergabe", " / "
    ]
    
    cleaned_column = utils.remove_keywords_from_column(
        doctor_specialization_column, 
        keywords=DOCTOR_SPECIALIZATION_KEYWORDS
    )

    return cleaned_column.str.title()

def sync_receipt_and_vo_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Synchronizes 'receipt_id' and 'vo_id' for each row.
    If one is missing, it's filled with the value of the other.
    """
    def sync_ids_for_single_row(row):
        receipt_id = row['receipt_id']
        vo_id = row['vo_id']

        receipt_is_missing = pd.isna(receipt_id)
        vo_is_missing = pd.isna(vo_id)

        if receipt_is_missing and not vo_is_missing:
            row['receipt_id'] = vo_id
        elif not receipt_is_missing and vo_is_missing:
            row['vo_id'] = receipt_id

        return row

    return df.apply(sync_ids_for_single_row, axis=1)

def format_pharmacy_owner_column(pharmacy_owner_column: pd.Series) -> pd.Series:
    """Cleans the pharmacy owner column by removing boilerplate and junk values."""

    PHARMACY_OWNER_KEYWORDS = [
    "gGmbH", "GmbH", "e.V.", "e. V.",
    "e V", "e.V", "eV","B.V.", "OHG", "oHG","e.Kfm",
    "e. Kfm","e.Kfr.", "#","e.K.","e. K.","e.K",
    "Inh.","Inhaber"
    ]
    
    cleaned_column = utils.remove_keywords_from_column(
        pharmacy_owner_column, 
        keywords=PHARMACY_OWNER_KEYWORDS
    )

    return cleaned_column

def validate_ihpe_units_column(ihpe_units: pd.Series) -> pd.Series:
    """
    Validates a column to ensure that entries are None or whole number.
    """

    def validate_single_ihpe_units(ihpe_units):
        if pd.isna(ihpe_units):
            return None
        try:
           ihpe_units_int = int(ihpe_units)
        except (ValueError, TypeError):
            return None

        if ihpe_units_int >= 0:
            return ihpe_units_int
        else:
            return None
    return ihpe_units.apply(validate_single_ihpe_units)

def validate_kv_district_column(kv_district: pd.Series) -> pd.Series:
    """
    Validates a kv_district column to ensure that entries are None or whole number and max 17.
    """

    def validate_single_kv_district(kv_district):
        if pd.isna(kv_district):
            return None
        try:
           kv_district_int = int(kv_district)
        except (ValueError, TypeError):
            return None

        if kv_district_int >= 0 and kv_district_int <= 17:
            return kv_district_int
        else:
            return None
    return kv_district.apply(validate_single_kv_district)

def split_full_name(full_name: str) -> dict:
    """
    Intelligently splits a full name string into its components using the nameparser library.
    """
    if pd.isna(full_name) or not str(full_name).strip():
        return {"title": "", "first_name": "", "last_name": ""}

    name = HumanName(str(full_name))

    return {
        "title": name.title,
        "first_name": name.first,
        "last_name": name.last
    }
