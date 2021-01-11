"""
相関係数
"""
import sys,os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import VALUES
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    source_dir = os.path.join(os.path.dirname(__file__) + '/../got_data/concated_companies/concated_us_info_list.csv')
    df = pd.read_csv(source_dir,encoding='utf-8')
    df = df[[VALUES.VOLUME,
            VALUES.SLOPE_OF_LAST_5_DAYS,
            VALUES.SLOPE_OF_LAST_10_DAYS,
            VALUES.SLOPE_OF_LAST_15_DAYS,
            VALUES.SLOPE_OF_LAST_20_DAYS,
            VALUES.COEFFICIENT_OF_VARIATION,
            VALUES.CLOSE_PRICE_UP_RATIO]]
    df_corr = df.corr()
    print(df_corr)
    sns.heatmap(df_corr, vmax=1, vmin=-1, center=0)
    plt.show()

# TODO ↓10日間の株価上昇率にもっと寄与する値を探す今のところ「直近5日の1次近似の傾き」の0.15のみ
#                     出来高  直近5日の1次近似の傾き  直近10日の1次近似の傾き  直近15日の1次近似の傾き  直近20日の1次近似の傾き      変動係数  10日間の株価上
# 昇率
# 出来高            1.000000      0.086058       0.011283      -0.003092       0.001759 -0.000052    0.026190
# 直近5日の1次近似の傾き   0.086058      1.000000       0.045126       0.033490       0.012663 -0.032104    0.156027
# 直近10日の1次近似の傾き  0.011283      0.045126       1.000000       0.629455       0.426292  0.306844   -0.018029
# 直近15日の1次近似の傾き -0.003092      0.033490       0.629455       1.000000       0.837565  0.642929   -0.019810
# 直近20日の1次近似の傾き  0.001759      0.012663       0.426292       0.837565       1.000000  0.889325   -0.028258
# 変動係数          -0.000052     -0.032104       0.306844       0.642929       0.889325  1.000000   -0.023199
# 10日間の株価上昇率     0.026190      0.156027      -0.018029      -0.019810      -0.028258 -0.023199    1.000000