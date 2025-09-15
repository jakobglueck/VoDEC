import pandas as pd
from app.core import fam_formatter

#-- test -- void blgnr sync -- #
def test_sync_receipt_and_vo_ids():

    input_data = {
        'receipt_id': ['R100', None, 'R300', None],
        'vo_id':      ['V100', 'V200', None, None],
        'other_col':  [1, 2, 3, 4]
    }
    input_df = pd.DataFrame(input_data)

    result_df = fam_formatter.sync_receipt_and_vo_ids(input_df)

    assert result_df.loc[0, 'receipt_id'] == 'R100'
    assert result_df.loc[0, 'vo_id'] == 'V100'

    assert result_df.loc[1, 'receipt_id'] == 'V200'
    assert result_df.loc[1, 'vo_id'] == 'V200'

    assert result_df.loc[2, 'receipt_id'] == 'R300'
    assert result_df.loc[2, 'vo_id'] == 'R300'

    assert pd.isna(result_df.loc[3, 'receipt_id'])
    assert pd.isna(result_df.loc[3, 'vo_id'])

    assert result_df.loc[2, 'other_col'] == 3
