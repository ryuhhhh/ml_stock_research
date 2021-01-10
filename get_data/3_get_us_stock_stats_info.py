"""
データ取得3: 変動係数,1次近似,株価が十分に上昇するか を取得します
TODO check_stock_price_skyrocketed,get_slope_list_4_quarter
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import traceback
import matplotlib.pyplot as pltimport
import math
import datetime
from scipy import stats
import numpy as np

# 過去さかのぼる日数
DATE_NUM_LENGTH = 40

def get_stock_info(close_price_series,base_date):
    """
    以下の値を取得する
      - 変動係数
      - 1次近似の傾き1(last 5 days)
      - 1次近似の傾き2(last 10 days)
      - 1次近似の傾き3(last 15 days)
      - 1次近似の傾き4(last 20 days)
      - 次の10営業日後に直近の終値より10%以上高くなったかどうか
    """
    # 基準日から前20日-後10日分のデータを取得する
    # 基準日の終値を取得する
    # 基準日から前20日分の変動係数を取得する
    # 基準日から前5,10,15,20日分の1次近似を取得する
    # 基準日から後10日に10%以上高くなったか取得する
    pass

def get_coefficient_of_variation(close_series):
    """
    終値のシリーズを受け取り過去1か月と過去ヵ月の変動係数(有効桁数2桁)を求めます
    """
    coefficient_of_variation = round(stats.variation(close_series),2)
    return coefficient_of_variation

def check_stock_price_skyrocketed(close_series,start):
    """
    10営業日までに直近の終値より15%以上高くなったかどうか確認する
    """
    pass

def get_slope_list_4_quarter(close_price_series,base_date):
    """
    日付降順の終値リストに指定されている期間で株価を取得し1時近似を取得する
    """
    QUARTER_NUM = 4
    close_price_series_length = len(close_price_series)
    # ループ用変数
    close_price_series_length_quarter = int(close_price_series_length/QUARTER_NUM)
    loop_length = close_price_series_length_quarter
    slope_list = []
    # データが少なすぎる場合はスキップ
    if close_price_series_length < QUARTER_NUM:
        print('データが少ないためスキップします')
        return slope_list
    # 指定期間の4等分の上昇量を取得する
    while loop_length < close_price_series_length:
        try:
            # 日付で区切りながら昇順にしていく
            slope = get_slope(close_price_series[:loop_length].iloc[::-1])
            # print(f'{loop_length}日前からの上昇量は{slope}です')
            loop_length += close_price_series_length_quarter
            slope_list.append(slope)
        except Exception:
            print(f'1次近似取得時にエラー発生。スキップします。')
            continue
    return slope_list

def get_slope(close_price_list):
    """
    終値のリストより1次近似を求めます
    ※series型でも扱える
    """
    close_price_list_num = len(close_price_list)
    try:
        slope,intercept = np.polyfit(list(range(close_price_list_num)), close_price_list, 1)
        slope = round(slope,2)
    except:
        print('1次近似を求めるのに失敗しました。スキップします。')
        return 0
    return slope


if __name__ == "__main__":
    pass
