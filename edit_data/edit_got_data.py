"""
データクリーニングやスプリットを行います
TODO edit_data_from_analyse_result を実装
"""
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import utils
import VALUES
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.decomposition import PCA

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
    # print(df)
    return df


def split_data(df):
    """
    データを訓練用とテスト用に分割します
    """
    df_train, df_test = train_test_split(df, random_state=42)
    return df_train, df_test

def edit_data_from_analyse_result(df):
    """
    analyseで得た知見をもとにここで反映します
    現在:新たに以下の値を追加します
        - 傾き5_割る_標準偏差
        - 出来高_割る_1σ
        - 傾き5_割る_終値
        - 出来高_割る_終値
        - 標準偏差_割る_終値
        - 出来高_割る_傾き15
    """
    # 傾き5/標準偏差
    series1 = round(df[VALUES.SLOPE_OF_LAST_5_DAYS] / df[VALUES.RHO],2)
    series1.name = VALUES.SLOPE5_DEVIDE_RHO

    # 出来高/標準偏差
    series2 = round(df[VALUES.VOLUME] / df[VALUES.RHO],2)
    series2.name = VALUES.VOLUME_DEVIDE_RHO

    # 傾き5/終値
    series3 = round(df[VALUES.SLOPE_OF_LAST_5_DAYS] / df[VALUES.CLOSING_PRICE],2)
    series3.name = VALUES.SLOPE5_DEVIDE_CLOSE_PRICE

    # 出来高/終値
    series4 = round(df[VALUES.VOLUME] / df[VALUES.CLOSING_PRICE],2)
    series4.name = VALUES.VOLUME_DEVIDE_CLOSE_PRICE


    # 標準偏差/終値
    series5 = round(df[VALUES.RHO] / df[VALUES.CLOSING_PRICE],2)
    series5.name = VALUES.RHO_DEVIDE_CLOSE_PRICE

    # 出来高/傾き15
    series6 = round(df[VALUES.VOLUME] / df[VALUES.SLOPE_OF_LAST_15_DAYS],2)
    series6.name = VALUES.VOLUME_DEVIDE_SLOPE15

    df = pd.concat([df,series1,series2,series3,series4,series5,series6], axis=1)
    print(df.columns)
    return df

def pca(df):
    """
    主成分分析を行い次元削減後の特徴量をdfに付け加えます
    ※寄与率が等分されたため今回は未使用
    (写像先の分散を最大化します)
    """
    pca = PCA(n_components=4)
    pca.fit(df[VALUES.TARGET_COLS])
    print(pca.explained_variance_ratio_)


def main(is_fit=True):
    """
    main関数
    データを加工
    """
    source_path = 'data/got_data/concated_companies/'
    if is_fit:
        source_path = source_path + 'concated_us_info_list.csv'
    else:
        source_path = source_path + 'todays_concated_us_list_.csv'
    df = utils.read_csv(source_path)
    df = edit_data_from_analyse_result(df)
    # データを標準化
    df = standardize_data(df,VALUES.TARGET_COLS)
    # 訓練用とテスト用でデータ分割
    df_train, df_test = split_data(df)

    if is_fit:
        # 訓練セットを保存
        utils.save_to_csv(df_train,'data/edited_data/train.csv')
        utils.save_to_csv(df_test,'data/edited_data/test.csv')
    else:
        # 特徴量を保存
        utils.save_to_csv(df,'data/edited_data/todays.csv')

if __name__ == "__main__":
    """
    特徴量を加工します
    args:
       is_fit: 学習かどうか判断
    """
    # 引数がある場合取得
    args = sys.argv
    if len(args) > 1:
        is_fit = args[1]
        main(is_fit)
    else:
        main()