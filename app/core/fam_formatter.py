
from datetime import datetime
import re
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

def validate_plz_column(plz_column: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are valid German postal codes.
    A valid PLZ is a string containing exactly 5 digits.
    Invalid or empty entries are converted to None.
    """
    
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

def validate_medicine_name_column(medicine_name: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are in the right format like a Grosse2 excel function.
    """

    def validate_single_medicine_name(medicine_name):
        if pd.isna(medicine_name) or not str(medicine_name).strip():
            return None
        
        return str(medicine_name).title()
    return medicine_name.apply(validate_single_medicine_name)

def validate_prescription_date_column(prescription_date: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are in the right time period.
    """

    def validate_prescription_date(prescription_date):

        parsed_dates = pd.to_datetime(prescription_date, errors='coerce', dayfirst=True)

        today = pd.Timestamp.now()
        two_years_ago = today - pd.DateOffset(years=1)

        parsed_dates.loc[parsed_dates < two_years_ago] = pd.NaT
        parsed_dates.loc[parsed_dates > today] = pd.NaT

        formatted_dates = parsed_dates.dt.strftime('%d.%m.%Y')

        formatted_dates = formatted_dates.replace({pd.NaT: None})

        return formatted_dates
    return prescription_date.apply(validate_prescription_date)

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

def validate_lanr_column(lanr: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are are valid lanr(more than 5 digits and no consecutive identical digits).
    """

    def validate_single_lanr(lanr):
        if pd.isna(lanr):
            return None
        
        lanr_str = str(lanr).split('.')[0].strip()
        
        if not lanr_str.isdigit():
            return None

        if len(lanr_str) < 6:
            return None
        
        if re.search(r'(\d)\1{3,}', lanr_str):
            return None 

        return lanr_str
    return lanr.apply(validate_single_lanr)

def validate_doctor_title_column(doctor_title: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are are valid doctor titles.
    """

    def validate_single_doctor_title(doctor_title):

        if pd.isna(doctor_title) or not str(doctor_title).strip():
            return None 

        check_str = str(doctor_title).lower().replace('.', '').replace(' ', '')

        dr_keywords = ('dr', 'doctor', 'mudr', 'md', 'mbbs', 'dott', 'doktor')
        prof_keywords = ('prof', 'professor')
        pd_keywords = ('pd', 'privatdozent', 'priv')
        drdr_keywords = ('drdr', 'doktordoktor')

        has_dr = any(kw in check_str for kw in dr_keywords)
        has_prof = any(kw in check_str for kw in prof_keywords)
        has_pd = any(kw in check_str for kw in pd_keywords)
        has_drdr = any(kw in check_str for kw in drdr_keywords)

        if has_prof:
            if has_drdr:
                return "Prof. Dr. Dr."
            elif has_dr:
                return "Prof. Dr."
        elif has_pd:
            if has_drdr:
                return "PD Dr. Dr."
            elif has_dr:
                return "PD Dr."
        elif has_drdr:
            return "Dr. Dr."
        elif has_dr:
            return "Dr."
        return None
    return doctor_title.apply(validate_single_doctor_title)

def validate_doctor_first_name_column(doctor_first_name: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are are real names.
    """

    def validate_single_doctor_first_name(doctor_first_name):
        if pd.isna(doctor_first_name):
            return None
        
        cleaned_name = str(doctor_first_name).title()
        
        if str(doctor_first_name).strip().isdigit():
            return None
            
        return cleaned_name
    return doctor_first_name.apply(validate_single_doctor_first_name)

def validate_doctor_last_name_column(doctor_last_name: pd.Series) -> pd.Series:
    """
    Validates a column to ensure all entries are are real names.
    """

    def validate_single_doctor_last_name(doctor_last_name):
        if pd.isna(doctor_last_name):
            return None
        
        cleaned_name = str(doctor_last_name).title()
        
        if str(doctor_last_name).strip().isdigit():
            return None
            
        return cleaned_name
    return doctor_last_name.apply(validate_single_doctor_last_name)
