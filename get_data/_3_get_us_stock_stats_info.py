"""
データ取得3:
 - 変動係数
 - 1次近似
 - 株価が十分に上昇するか
 - 終値の±2σまでの距離
を取得します
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

def get_stock_info(close_price_series,base_date_close_price,base_index=None,base_date=None,is_today=False):
    """
    以下の値を取得する
      - 変動係数
      - 1次近似の傾き1(last 5 days)
      - 1次近似の傾き2(last 10 days)
      - 1次近似の傾き3(last 15 days)
      - 1次近似の傾き4(last 20 days)
      - 次の10営業日後に直近の終値より10%以上高くなったかどうか
    """
    # 基準日より前20日,後10日の長さ31日のseriesを取得
    if not is_today:
       close_price_series_batch = close_price_series[base_index-19:base_index+11]
    else :
        close_price_series_batch = close_price_series[-20:]
    # 基準日から前20日分の変動係数を取得する
    coefficient_of_variation = get_coefficient_of_variation(close_price_series_batch[:20])
    # 基準日から前5,10,15,20日分の1次近似を取得する
    slope_list = get_slope_list_4_quarter(close_price_series_batch[:20].iloc[::-1])
    # 標準偏差を取得する
    rho = get_rho(close_price_series_batch[:20])
    # 予測用に使用する場合はここで返す
    if is_today:
        return coefficient_of_variation,\
               slope_list,\
               rho
    # 基準日から後10日にratio倍高くなったか取得する
    RATIO = 1.1
    if_close_price_up,close_price_up_ratio = \
        check_stock_price_skyrocketed(close_price_series_batch[-10:],base_date_close_price,RATIO)
    return coefficient_of_variation,\
           slope_list,\
           if_close_price_up,\
           close_price_up_ratio,\
           rho


def get_coefficient_of_variation(close_series):
    """
    終値のシリーズを受け取り過去1か月と過去ヵ月の変動係数(有効桁数2桁)を求めます
    """
    coefficient_of_variation = round(stats.variation(close_series),2)
    return coefficient_of_variation

def get_slope_list_4_quarter(close_price_series):
    """
    日付降順の終値リストに指定されている期間で株価を取得し1時近似を取得する
    Returns:
        1次近似のリスト(list):5,10,15,20日前のリストを取得する
    """
    QUARTER_NUM = 4
    slope_list = []
    # 指定期間の4等分の上昇量を取得する
    for i in range(5,len(close_price_series)+1,int(len(close_price_series)/QUARTER_NUM)):
        try:
            # 日付で区切りながら昇順にしていく
            slope = get_slope(close_price_series[:i].iloc[::-1])
            # print(f'{loop_length}日前からの上昇量は{slope}です')
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

def check_stock_price_skyrocketed(close_price_series,close_price,ratio=1.1):
    """
    教師データ取得
    10営業日までに直近の終値よりratio%以上高くなったかどうか確認する
    Return:
        if_close_price_up(num):上がる->1,上がらない->0
    """
    # print(f'{close_price}に対して後10日で{ratio}倍になった日があるか検索します')
    target_price = close_price*ratio
    if_close_price_up = 0
    max_price = close_price_series.max()
    if max_price > target_price:
        if_close_price_up = 1
    close_price_up_ratio = round(max_price/close_price,2)
    return if_close_price_up,close_price_up_ratio

def get_rho(close_price_series):
    """
    標準偏差を取得します
    """
    # 標準偏差を取得
    return round(close_price_series.std(),2)

