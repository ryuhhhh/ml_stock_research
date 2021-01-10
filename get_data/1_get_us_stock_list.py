"""
データ取得1: 米国株のリストを取得します
"""
import pandas as pd
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import VALUES

def quote_us_stock_lists(url=f'{VALUES.CSV_ROOT_PATH}/{VALUES.US_STOCK_LIST_CSV_NAME}'):
    """
    米国株の一覧をcsvより取得します
    """
    df = pd.read_csv(url,encoding='utf-8')
    return df

if __name__ == "__main__":
    pass