import pandas as pd
from typing import Dict, Any

def _build_notes_df(notes: Dict[str, Any]) -> pd.DataFrame:
    """Creates the DataFrame for the Notes sheet."""
    return pd.DataFrame(list(notes.items()), columns=['Check', 'Result'])

def _write_rejection_sheet(writer: pd.ExcelWriter, rejected_data: Dict[str, pd.DataFrame], sheet_name: str, report_sheet_name: str):
    """Writes a detailed rejection report to a given sheet."""
    if not rejected_data:
        print(f"No rejected data for {sheet_name} to export.")
        return

    start_row = 0
    
    for reason, df in rejected_data.items():
        if df.empty:
            continue
            
        header_text = f'Folgende Zeilen wurden aus dem Sheet "{sheet_name}" herausgeschnitten, da {reason}:'
        header_df = pd.DataFrame([header_text])
        header_df.to_excel(writer, sheet_name=report_sheet_name, startrow=start_row, index=False, header=False)
        start_row += 2

        df.to_excel(writer, sheet_name=report_sheet_name, startrow=start_row, index=False)
        start_row += len(df) + 2

    print(f"Sheet '{report_sheet_name}' written.")

def export_to_single_workbook(
    output_path: str,
    active_fam_df: pd.DataFrame,
    active_tm_df: pd.DataFrame,
    analysis_notes: Dict[str, Any],
    rejected_fam_data: Dict[str, pd.DataFrame],
    rejected_tm_data: Dict[str, pd.DataFrame]
):
    """
    Exports all results into a single Excel workbook with multiple sheets.
    """
    print(f"Starting export to single workbook: {output_path}")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

        active_fam_df.to_excel(writer, sheet_name="FAM_aufbereitet", index=False)
        print("Sheet 'FAM_aufbereitet' written.")

        active_tm_df.to_excel(writer, sheet_name="TM_aufbereitet", index=False)
        print("Sheet 'TM_aufbereitet' written.")

        notes_df = _build_notes_df(analysis_notes)
        notes_df.to_excel(writer, sheet_name="Analyse_Hinweise", index=False, header=False)
        print("Sheet 'Analyse_Hinweise' written.")
        
        _write_rejection_sheet(writer, rejected_fam_data, "FAM ihpE aufbereitet", "Ausschuss_FAM")

        _write_rejection_sheet(writer, rejected_tm_data, "TM aufbereitet", "Ausschuss_TM")

    print(f"Excel workbook '{output_path}' created successfully.")