import pandas as pd
from typing import Dict, Tuple

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
