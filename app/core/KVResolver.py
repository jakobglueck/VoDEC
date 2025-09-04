# in app/core/resolvers.py (or a similar utility file)
import pandas as pd
from typing import Dict

class KVResolver:
    """
    A performant resolver for KV districts that loads lookup data only once.
    """

    KV_NAME_TO_CODE_MAP: Dict[str, str] = {
        "Baden-Württemberg": "1",
        "Westfalen-Lippe": "2",
        "Sachsen-Anhalt": "3",
        "Rheinland-Pfalz": "4",
        "Niedersachsen": "5",
        "Bayern": "6",
        "Bremen": "7",
        "Hessen": "8",
        "Mecklenburg-Vorpommern": "9",
        "Sachsen": "10",
        "Brandenburg": "11",
        "Saarland": "12",
        "Schleswig-Holstein": "13",
        "Thüringen": "14",
        "Hamburg": "15",
        "Berlin": "16",
        "Nordrhein": "17"
    }

    def __init__(self, asset_path: str):
            """
            Initializes the resolver by loading the PLZ-to-KV mapping from an Excel file.
            """
            try:

                df_lookup = pd.read_excel(asset_path, header=0)

                df_lookup = df_lookup.iloc[:, [0, 3]]
                df_lookup.columns = ["plz", "kv_code"] 

                df_lookup['plz'] = df_lookup['plz'].astype(str)

                df_lookup.drop_duplicates(subset='plz', keep='first', inplace=True)

                self.plz_to_kv_code_map = pd.Series(
                    df_lookup.kv_code.values, 
                    index=df_lookup.plz
                ).to_dict()
                
            except FileNotFoundError:
                raise FileNotFoundError(f"KV lookup file not found at: {asset_path}")
            except IndexError:
                raise ValueError("The Excel file needs at least 4 columns (PLZ in A, KV-Code in D).")

    def resolve_kv_column(self, kv_district_column: pd.Series, arzt_postcode_column: pd.Series) -> pd.Series:
        """
        Resolves the KV district using the two-step fallback logic.
        """

        resolved_series = kv_district_column.map(self.KV_NAME_TO_CODE_MAP)

        fallback_series = arzt_postcode_column.map(self.plz_to_kv_code_map)

        resolved_series.fillna(fallback_series, inplace=True)
        
        return resolved_series
