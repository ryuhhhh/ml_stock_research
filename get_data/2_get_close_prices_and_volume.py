"""
データ取得2: 終値・取引高・時価総額を取得します
"""
import pandas_datareader.data as pdr

ONE_HUNDRED_MILLION = 100000000

def get_close_price_and_volume_series(code):
    """
    終値・取引高・時価総額のシリーズを取得する
    args:
        code(str):銘柄コーtド
        data_num_length(int):何日前のモノを取得するか
    returns:
        close_price_series(series):終値のシリーズ
    """
    # 終値を取得する日付を指定する
    start = '2020-01-01'
    end = '2021-01-10'
    # 終値のシリーズを取得する
    close_price_series = pdr.DataReader(code, 'yahoo',start,end)
    print(close_price_series[['Close','Volume']])
    return close_price_series

def get_market_cap(code):
    """
    時価総額の取得
    単位は億ドル
    """
    # 時価総額の取得
    market_cap_series = pdr.get_quote_yahoo(code)['marketCap']
    market_cap = round(market_cap_series[code]/ONE_HUNDRED_MILLION,2)
    print(market_cap)
    return market_cap

if __name__ == "__main__":
    pass