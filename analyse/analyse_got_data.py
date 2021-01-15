"""
相関係数を調査します
調査結果よりデータを修正する際はedit_dataで行います
"""
import sys,os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import VALUES
import seaborn as sns
import matplotlib.pyplot as plt

def make_grid_param(df,columns):
    """
    データフレームの値を組み合わせて新しい値を作成します。
    +-*/
    """
    for column_outer in columns:
        target_series = df[column_outer]
        for column_inner in columns:
            if column_inner == column_outer:
                continue
            target_series = round(target_series,2)
            column_inner_value = round(df[column_inner],2)
            series_plus = target_series + column_inner_value
            series_plus.name = column_outer + '_' + column_inner + '_plus'
            series_minus = target_series - column_inner_value
            series_minus.name = column_outer + '_' + column_inner + '_minus'
            series_divide = target_series / column_inner_value
            series_divide.name = column_outer + '_' + column_inner + '_devide'
            series_cross = target_series * column_inner_value
            series_cross.name = column_outer + '_' + column_inner + '_cross'
            df = pd.concat([df, series_plus,series_minus,series_divide,series_cross], axis=1)
    return df

def main():
    """
    メイン関数
    データを分析します
    """
    source_dir = os.path.join(os.path.dirname(__file__) + '/../data/got_data/concated_companies/concated_us_info_list.csv')
    df = pd.read_csv(source_dir,encoding='utf-8')
    df = df[[VALUES.CLOSING_PRICE,
            VALUES.VOLUME,
            VALUES.SLOPE_OF_LAST_5_DAYS,
            VALUES.SLOPE_OF_LAST_10_DAYS,
            VALUES.SLOPE_OF_LAST_15_DAYS,
            VALUES.SLOPE_OF_LAST_20_DAYS,
            VALUES.COEFFICIENT_OF_VARIATION,
            VALUES.CLOSE_PRICE_UP_RATIO,
            VALUES.RHO]]

    # 様々な値を組み合わせて新しいdfを作成
    df = make_grid_param(df,[
            VALUES.CLOSING_PRICE,
            VALUES.VOLUME,
            VALUES.SLOPE_OF_LAST_5_DAYS,
            VALUES.SLOPE_OF_LAST_10_DAYS,
            VALUES.SLOPE_OF_LAST_15_DAYS,
            VALUES.SLOPE_OF_LAST_20_DAYS,
            VALUES.COEFFICIENT_OF_VARIATION,
            VALUES.RHO])

    df_corr = df.corr()
    df_corr['10日間の株価上昇率'].to_csv('./corr.csv',encoding='utf-8-sig')
    # sns.heatmap(df_corr, vmax=1, vmin=-1, center=0)
    # plt.show()

# 直近5日の1次近似の傾き_1σ_devide	0.283256359
# 出来高_1σ_devide	0.20069086
# 直近5日の1次近似の傾き_終値_devide	0.179589064
# 出来高_終値_devide	0.169579892
# 1σ_終値_devide	0.135024254
# 出来高_直近15日の1次近似の傾き_devide	0.098294569



if __name__ == "__main__":
    main()