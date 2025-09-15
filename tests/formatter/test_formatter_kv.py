from pathlib import Path
import pandas as pd
from app.core.KVResolver import KVResolver 

#-- test -- kv formatter -- #
def test_kv_formatter():
    current_file = Path(__file__)
    
    project_root = current_file.parent.parent.parent

    asset_file_path = project_root / "assets" / "plz_kv_mapping.xlsx"

    kv_resolver = KVResolver(asset_path=asset_file_path)

    input_data = {
        'arzt_postcode': ['10115', '80331', '99999', '44135','06618'],
        'kv_district':   ['Berlin', 'Oberpfalz', 'Invalid Name', None, 'Sachsen-Anhalt']
    }
    main_df = pd.DataFrame(input_data)

    result_series = kv_resolver.resolve_kv_column(
        arzt_postcode_column=main_df['arzt_postcode'], kv_district_column=main_df['kv_district']
    )
    main_df['kv_code_cleaned'] = result_series

    assert main_df.loc[0, 'kv_code_cleaned'] == '16'

    assert main_df.loc[1, 'kv_code_cleaned'] == '6'

    assert pd.isna(main_df.loc[2, 'kv_code_cleaned'])

    assert main_df.loc[3, 'kv_code_cleaned'] == '2'

    assert main_df.loc[4, 'kv_code_cleaned'] == '3'
