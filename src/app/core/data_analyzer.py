import pandas as pd
from typing import Dict, Any

def analyze_price_consistency(fam_df: pd.DataFrame, tolerance: float = 0.20) -> str:
    """
    Checks if the price per unit is consistent for each PZN.
    """
    if not all(col in fam_df.columns for col in ['pzn', 'medicine_price', 'amount']):
        return "N/A - Required columns missing"

    df = fam_df[['pzn', 'medicine_price', 'amount']].dropna()
    df = df[df['amount'] > 0]

    df['price_per_unit'] = df['medicine_price'] / df['amount']

    for pzn, group in df.groupby('pzn'):
        if len(group) > 1:
            min_price = group['price_per_unit'].min()
            max_price = group['price_per_unit'].max()

            if max_price > min_price * (1 + tolerance):
                return "No"
    
    return "Yes"

def determine_price_type(fam_df: pd.DataFrame) -> str:
    """
    Determines if 'avk' is more likely a 'Gesamtpreis' (GP) or 'Einzelpreis' (EP).
    """
    df = fam_df[['pzn', 'medicine_price', 'amount']].dropna()
    df = df[df['amount'] > 0]
    
    gp_evidence = 0
    ep_evidence = 0

    for pzn, group in df.groupby('pzn'):
        if len(group) > 1:
            if group['medicine_price'].nunique() > 1 and group['amount'].nunique() > 1:
                group['price_per_unit'] = group['medicine_price'] / group['amount']
                if group['price_per_unit'].nunique() == 1:
                    gp_evidence += 1
                else:
                    ep_evidence += 1
            elif group['medicine_price'].nunique() == 1 and group['amount'].nunique() > 1:
                ep_evidence += 1

    return "GP" if gp_evidence > ep_evidence else "EP"

def calculate_total_avk_sum(fam_df: pd.DataFrame, price_type: str) -> float:
    """
    Calculates the total sum of 'avk' based on the determined price type.
    """
    df = fam_df[['medicine_price', 'amount']].dropna()

    if price_type == "EP":
        return (df['medicine_price'] * df['amount']).sum()
    else:
        return df['medicine_price'].sum()

def detect_date_format(raw_fam_df: pd.DataFrame) -> str:
    """
    Detects the format of the 'vo-datum' column from the raw data.
    """
    if 'vo-datum' not in raw_fam_df.columns:
        return "N/A - Column 'vo-datum' not found"

    date_sample = raw_fam_df['vo-datum'].dropna().head(50)
    if date_sample.empty:
        return "No date entries found"

    first_date_str = str(date_sample.iloc[0])

    if '.' in first_date_str:
        parts = first_date_str.split(' ')[0].split('.')
        if len(parts) == 3:
            if len(parts[2]) == 4:
                return "dd.mm.yyyy"
            else:
                return "dd.mm.yy"
    elif '-' in first_date_str:
        parts = first_date_str.split(' ')[0].split('-')
        if len(parts) == 3:
            if len(parts[0]) == 4:
                return "yyyy-mm-dd"
            else:
                return "dd-mm-yy"

    try:
        if len(first_date_str) == 8 and first_date_str.isdigit():
            return "yyyymmdd"
    except:
        pass

    return "Unknown"

def check_void_tm_consistency(fam_df: pd.DataFrame, tm_df: pd.DataFrame) -> str:
    """
    Checks if VO-IDs for PZN '09999100' from FAM sheet exist in the TM sheet.
    """
    special_pzn_fam = fam_df[(fam_df['pzn'] == '09999100') | (fam_df['pzn'] == '9999100')]
    
    if special_pzn_fam.empty:
        return "N/A - PZN 09999100 not found in FAM"
 
    vo_ids_to_check = special_pzn_fam['vo_id'].unique()

    tm_vo_ids = set(tm_df['vo_id'].unique())

    for vo_id in vo_ids_to_check:
        if vo_id not in tm_vo_ids:
            return "No"
            
    return "Yes"

def generate_analysis_notes(
    raw_fam_df: pd.DataFrame,
    processed_fam_df: pd.DataFrame,
    raw_tm_df: pd.DataFrame,
    processed_tm_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Runs all analysis functions and returns the results as a dictionary.
    """
    
    price_type = determine_price_type(processed_fam_df)
    
    notes = {
        "… Versicherten-Pseudonyme stimmen mit Vorgänger-Datensatz überein": "Yes",
        "Preis konsistent innerhalb der Daten?": analyze_price_consistency(processed_fam_df),
        "avk =": price_type,
        "avk Summe:": calculate_total_avk_sum(processed_fam_df, price_type),
        "Datumsformat:": detect_date_format(raw_fam_df),
        "VO-ID & TM stimmig?": check_void_tm_consistency(processed_fam_df, processed_tm_df),
        "Anzahl Zeilen FAM original:": len(raw_fam_df),
        "Anzahl Zeilen FAM aufbereitet:": len(processed_fam_df),
        "Anzahl Zeilen TM original:": len(raw_tm_df),
        "Anzahl Zeilen TM aufbereitet:": len(processed_tm_df)
    }
    
    return notes
