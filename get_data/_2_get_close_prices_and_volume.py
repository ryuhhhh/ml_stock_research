"""
データ取得2: 終値・取引高・時価総額を取得します
"""
import pandas_datareader.data as pdr
import time
import traceback
import pandas as pd
ONE_HUNDRED_MILLION = 100000000

def get_close_price_and_volume_df(code):
    """
    終値・取引高のdfを取得する
    args:
        code(str):銘柄コーtド
        data_num_length(int):何日前のモノを取得するか
    returns:
        close_price_and_volume_df(series):終値と出来高のdf
    """
    close_price_and_volume_df = pd.DataFrame(index=[], columns=[])
    # 終値を取得する日付を指定する
    start = '2020-01-01'
    end = '2021-01-10'
    # 終値のシリーズを取得する
    try:
        close_price_and_volume_df = pdr.DataReader(code, 'yahoo',start,end)
    except Exception as ex:
        print(f'終値取得時にエラー')
        print(traceback.format_exc())
    time.sleep(1)

    # print(close_price_and_volume_df[['Close','Volume']])
    return close_price_and_volume_df

def get_market_cap(code):
    """
    時価総額の取得
    単位は億ドル
    """
    # 時価総額の取得
    try:
        market_cap_series = pdr.get_quote_yahoo(code)['marketCap']
        market_cap = round(market_cap_series[code]/ONE_HUNDRED_MILLION,2)
    except Exception as ex:
        print(f'時価総額取得時にエラー')
        print(traceback.format_exc())
        market_cap = None
    return market_cap

if __name__ == "__main__":
    pass