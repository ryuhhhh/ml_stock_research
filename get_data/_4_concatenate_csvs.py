"""
4. 取得したcsvを列方向に連結し1つのcsvにします。
"""
import os,sys
import glob
import pandas as pd

ENCODING_TYPE = 'utf-8-sig'

def concat_csvs(sourth_dir,dest_path):
    """
    指定したパスのcsvを全て連結し1つのcsvにします
    """
    pass

if __name__ == "__main__":
    sourth_dir = os.path.join(os.path.dirname(__file__) + '/../got_data/companies')
    dest_dir = os.path.join(os.path.dirname(__file__) + '/../got_data/concated_us_info_list.csv')
    paths = glob.glob(sourth_dir+'/*')
    result_df = pd.DataFrame(index=[], columns=[])
    for path in paths:
        read_df = pd.read_csv(path,encoding='utf-8')
        result_df = pd.concat([result_df, read_df])
        print(f'{path}を連結')
    result_df.to_csv(dest_dir,encoding=ENCODING_TYPE)
    print(f'{dest_dir}に保存しました')
