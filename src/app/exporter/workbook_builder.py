import pandas as pd
from typing import Dict, Any, List

def _build_notes_df(notes: Dict[str, Any]) -> pd.DataFrame:
    """Creates the DataFrame for the Notes sheet."""
    return pd.DataFrame(list(notes.items()), columns=['Check', 'Result'])

def _build_rejection_df(rejected_data: Dict[str, pd.DataFrame], sheet_name: str) -> pd.DataFrame:
    """Creates a single DataFrame for the rejection report."""
    all_rejected_list = []
    for reason, df in rejected_data.items():

        header_text = f'Folgende Zeilen wurden aus dem Sheet "{sheet_name}" herausgeschnitten, da {reason}:'

        all_rejected_list.append(pd.DataFrame([header_text]))

        all_rejected_list.append(pd.DataFrame([df.columns.tolist()]))

        all_rejected_list.append(df)
        
        all_rejected_list.append(pd.DataFrame([""]))

    if not all_rejected_list:
        return pd.DataFrame()
        
    return pd.concat(all_rejected_list, ignore_index=True)

def export_to_single_workbook(
    output_path: str,
    active_fam_df: pd.DataFrame,
    active_tm_df: pd.DataFrame,
    analysis_notes: Dict[str, Any],
    rejected_fam_data: Dict[str, pd.DataFrame],
    rejected_tm_data: Dict[str, pd.DataFrame]
):
    """
    Exports all results (cleaned data, notes, rejected rows)
    into a single Excel workbook with multiple sheets.

    Args:
        output_path: The path for the final Excel file.
        active_fam_df: The DataFrame with the cleaned FAM data.
        active_tm_df: The DataFrame with the cleaned TM data.
        analysis_notes: The dictionary with the analysis results.
        rejected_fam_data: The dictionary with the rejected FAM rows.
        rejected_tm_data: The dictionary with the rejected TM rows.
    """
    print(f"Starting export to single workbook: {output_path}")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

        active_fam_df.to_excel(writer, sheet_name="FAM_processed", index=False)
        print("Sheet 'FAM_processed' written.")

        active_tm_df.to_excel(writer, sheet_name="TM_processed", index=False)
        print("Sheet 'TM_processed' written.")

        notes_df = _build_notes_df(analysis_notes)
        notes_df.to_excel(writer, sheet_name="Analysis_Notes", index=False, header=False)
        print("Sheet 'Analysis_Notes' written.")

        rejected_fam_df = _build_rejection_df(rejected_fam_data, "FAM ihpE aufbereitet")
        if not rejected_fam_df.empty:
            rejected_fam_df.to_excel(writer, sheet_name="Rejections_FAM", index=False, header=False)
            print("Sheet 'Rejections_FAM' written.")

        rejected_tm_df = _build_rejection_df(rejected_tm_data, "TM aufbereitet")
        if not rejected_tm_df.empty:
            rejected_tm_df.to_excel(writer, sheet_name="Rejections_TM", index=False, header=False)
            print("Sheet 'Rejections_TM' written.")

