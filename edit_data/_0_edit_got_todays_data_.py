"""
本日分のデータクリーニングやスプリットを行います
TODO edit_data_from_analyse_result を実装
"""
import _0_edit_got_data
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import utils
import VALUES
from sklearn.model_selection import train_test_split
import pandas as pd

if __name__ == "__main__":
    df = utils.read_csv('got_data/concated_companies/todays_concated_us_list_.csv')
    df = _0_edit_got_data.edit_data_from_analyse_result(df)
    # データを標準化
    df = _0_edit_got_data.standardize_data(df,[VALUES.VOLUME,
                              VALUES.SLOPE_OF_LAST_5_DAYS,
                              VALUES.SLOPE_OF_LAST_10_DAYS,
                              VALUES.SLOPE_OF_LAST_15_DAYS,
                              VALUES.SLOPE_OF_LAST_20_DAYS,
                              VALUES.COEFFICIENT_OF_VARIATION,
                              VALUES.SLOPE5_DEVIDE_RHO,
                              VALUES.VOLUME_DEVIDE_RHO,
                              VALUES.SLOPE5_DEVIDE_CLOSE_PRICE,
                              VALUES.VOLUME_DEVIDE_CLOSE_PRICE,
                              VALUES.RHO_DEVIDE_CLOSE_PRICE
                              ])
    # 訓練用とテスト用でデータ分割
    # 訓練セットを保存
    utils.save_to_csv(df,'edited_data/todays.csv')
