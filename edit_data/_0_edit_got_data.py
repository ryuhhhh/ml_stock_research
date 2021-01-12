"""
データクリーニングやスプリットを行います
"""
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import utils
import VALUES
from sklearn.model_selection import train_test_split

def impute_missing_value(df):
    """
    欠損値を補完します
    ※今回は取得出来なかった値を0においているため何もしない
    """

def delete_outliers():
    """
    外れ値を四分位数を元に削除します
    """

def standardize_data(df,columns):
    """
    データを標準化します
    """
    for column in columns:
        print(column)
        column_series = df[column]
        column_series = (column_series - column_series.mean()) / column_series.std()
        # print(column_series)
        print(f'平均が{column_series.mean()},標準偏差が{column_series.std()}になりました')
        df[column] = column_series
    print(df)
    return df


def split_data(df):
    """
    データを訓練用とテスト用に分割します
    """
    df_train, df_test = train_test_split(df, random_state=42)
    return df_train, df_test

if __name__ == "__main__":
    df = utils.read_csv('got_data/concated_companies/concated_us_info_list.csv')
    # データを標準化
    df = standardize_data(df,[VALUES.VOLUME,
                              VALUES.SLOPE_OF_LAST_5_DAYS,
                              VALUES.SLOPE_OF_LAST_10_DAYS,
                              VALUES.SLOPE_OF_LAST_15_DAYS,
                              VALUES.SLOPE_OF_LAST_20_DAYS,
                              VALUES.COEFFICIENT_OF_VARIATION,
                              ])
    # 訓練用とテスト用でデータ分割
    df_train, df_test = split_data(df)
    # print(len(df))
    # print(len(df_train),len(df_test))
    # 訓練セットを保存
    utils.save_to_csv(df_train,'edited_data/train.csv')
    utils.save_to_csv(df_test,'edited_data/test.csv')