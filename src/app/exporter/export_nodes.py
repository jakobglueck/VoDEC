import pandas as pd
from typing import Dict, Any

def export_analysis_notes(notes: Dict[str, Any], output_path: str):
    """
    Exports the analysis notes to a simple Excel file.
    
    Args:
        notes: A dictionary with the analysis results.
        output_path: The path for the output Excel file.
    """

    df_notes = pd.DataFrame(list(notes.items()), columns=['Check', 'Result'])

    df_notes.to_excel(output_path, index=False, header=False)
