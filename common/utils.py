"""
utils
"""
import pandas as pd
def save_to_csv(df,path):
    """
    dataframeをcsvに保存します
    """
    ENCODING_TYPE = 'utf-8-sig'
    # print(df)
    df.to_csv(path,encoding=ENCODING_TYPE)
    print(f'{path}に保存しました')

def read_csv(path,encoding='utf-8'):
    """
    米国株の一覧をcsvより取得します
    """
    df = pd.read_csv(path,encoding=encoding)
    return df