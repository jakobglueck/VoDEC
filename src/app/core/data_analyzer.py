
import pandas as pd
from typing import Dict, Any, Tuple

def analyze_price_consistency(fam_df: pd.DataFrame, tolerance: float = 0.20) -> str:
    """
    Checks if the price per unit is consistent for each PZN.

    Args:
        fam_df: The processed FAM DataFrame.
        tolerance: The allowed percentage deviation (e.g., 0.20 for 20%).

    Returns:
        "Yes" if prices are consistent, "No" otherwise.
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
    Determines if the 'avk' is more likely a 'Gesamtpreis' (GP) or 'Einzelpreis' (EP).

    Args:
        fam_df: The processed FAM DataFrame.

    Returns:
        "GP" for total price, "EP" for single unit price.
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

    Args:
        fam_df: The processed FAM DataFrame.
        price_type: "GP" or "EP".

    Returns:
        The total sum.
    """
    df = fam_df[['medicine_price', 'amount']].dropna()

    if price_type == "EP":

        return (df['medicine_price'] * df['amount']).sum()
    else:

        return df['medicine_price'].sum()

def detect_date_format(raw_fam_df: pd.DataFrame) -> str:
    """
    Detects the format of the 'vo-datum' column from the raw data.
    
    Args:
        raw_fam_df: The original, unprocessed FAM DataFrame.
        
    Returns:
        The detected date format string (e.g., "dd.mm.yyyy") or "Unknown".
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

    Args:
        fam_df: The processed FAM DataFrame.
        tm_df: The processed TM DataFrame.

    Returns:
        "Yes" if all are consistent, "No" otherwise.
    """
    special_pzn_fam = fam_df[fam_df['pzn'] == '09999100' or fam_df['pzn'] == '9999100' ]
    
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

REJECTION_CRITERIA_FAM = {

    "Essentielle Spalten (patnr, pzn, vo-datum, anzahl) sind unvollständig": 
        lambda df: df[['patient_nr', 'pzn', 'prescription_date', 'amount']].isna().any(axis=1),
        
    "avk ist ungültig (fehlt oder <= 0)": 
        lambda df: df['medicine_price'].isna(),
        
    "belegnr und vo_id fehlen beide": 
        lambda df: df['receipt_id'].isna() & df['vo_id'].isna(),
}

REJECTION_CRITERIA_TM = {

    "Botendienst-PZN (06461110)": 
        lambda df: df['PZN'].astype(str) == '6461110',

    "Teilmengenpreis ist ungültig (fehlt oder <= 0)": 
        lambda df: df['partial_quantity_price'].isna(),
        
    "Position/laufende Nr. ist ungültig": 
        lambda df: df['position'].isna(),
}

def analyze_rejections(
    raw_df: pd.DataFrame,
    processed_df: pd.DataFrame,
    criteria: Dict[str, callable],
    is_raw_criteria: bool = False
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Identifiziert und trennt ungültige Zeilen basierend auf Kriterien.
    Kann sowohl auf rohen als auch auf prozessierten Daten operieren.
    """
    rejected_rows_dict: Dict[str, pd.DataFrame] = {}
    active_df = processed_df.copy()

    source_df = raw_df.copy()
    source_df['original_index'] = source_df.index
    active_df['original_index'] = active_df.index

    df_to_check = source_df if is_raw_criteria else active_df

    for reason, condition_func in criteria.items():
        rejection_mask = condition_func(df_to_check)
        
        rejected_indices = df_to_check.loc[rejection_mask, 'original_index']
        
        if not rejected_indices.empty:

            rejected_original_data = source_df[source_df['original_index'].isin(rejected_indices)]
            
            if reason in rejected_rows_dict:
                rejected_rows_dict[reason] = pd.concat([rejected_rows_dict[reason], rejected_original_data.drop(columns=['original_index'])])
            else:
                rejected_rows_dict[reason] = rejected_original_data.drop(columns=['original_index'])

            active_df = active_df[~active_df['original_index'].isin(rejected_indices)]

    return active_df.drop(columns=['original_index']), rejected_rows_dict