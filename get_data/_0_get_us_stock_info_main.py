"""
TODO 5日にして縛りをきつくする
TODO csv保存後に0と1の割合を確認する
TODO 過去に株価が大きく変動した企業があるかチェック(発行済み株式総数が変化したか確認)
1ヵ月毎にcsvにセーブ
2020/01/12 ~ 2020/12/28 => 2.のget_close_price_and_volume_dfで変更可
"""
import _1_get_us_stock_list as usl
import _2_get_close_prices_and_volume as pav
import _3_get_us_stock_stats_info as ussi
import VALUES
import pandas as pd
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import utils

# 過去n日分ずつさかのぼるのを指定
SKIP_DATE = 10


# def save_to_dataframe(result_df_per_company,code,base_date,base_date_close_price,volume,coefficient_of_variation,slope_list,if_close_price_10_up,close_price_up_ratio):
def save_to_dataframe(result_df_per_company,data):
  """
  各企業ごとにdfに保存する処理
  """
  result_df_per_company.loc[data['code']+data['base_date'].strftime('%Y%m%d')]=[
            data['base_date'],
            data['base_date_close_price'],
            data['volume'],
            data['coefficient_of_variation'],
            data['slope_list'][0],
            data['slope_list'][1],
            data['slope_list'][2],
            data['slope_list'][3],
            data['if_close_price_up'],
            data['close_price_up_ratio'],
            data['sigma1'],
            data['sigma2']]
  return result_df_per_company

if __name__ == "__main__":
    pass
    # 1:米国株リストを取得
    us_stock_df = usl.quote_us_stock_lists()
    # 企業ごとの結果  用dfを宣言
    cols = [VALUES.CODE_AND_DATE_ID,
            VALUES.BASE_DATE,
            VALUES.CLOSING_PRICE,
            VALUES.VOLUME,
            VALUES.SLOPE_OF_LAST_5_DAYS,
            VALUES.SLOPE_OF_LAST_10_DAYS,
            VALUES.SLOPE_OF_LAST_15_DAYS,
            VALUES.SLOPE_OF_LAST_20_DAYS,
            VALUES.COEFFICIENT_OF_VARIATION,
            VALUES.IF_10per_UP_NEXT_10_DAYS,
            VALUES.CLOSE_PRICE_UP_RATIO,
            VALUES.SIGMA_1,
            VALUES.SIGMA_2]
    # 銘柄リストをループ
    for index, row in us_stock_df.iterrows():
      # if index < 426:
      #   continue
      result_df_per_company = pd.DataFrame(index=[], columns=cols)
      result_df_per_company.set_index(VALUES.CODE_AND_DATE_ID,inplace=True)
      # 今は情報技術セクターのみ取得
      if row[VALUES.INDUSTRY] != VALUES.IT_INDUSTRY:
          continue
      code = row[VALUES.CODE]
      print(f'{index}番目 {code} {row[VALUES.NAME]}')
      # 2:終値と出来高のdfを取得
      price_and_volume_df = pav.get_close_price_and_volume_df(code)
      # 取得できなかった場合スキップ
      if price_and_volume_df.empty:
        continue
      price_series = price_and_volume_df.Close
      # 2:時価総額を取得
      market_cap = pav.get_market_cap(code)
      # 10日分ずつずらしながらループしていく => dfの10番前を選択していき、その日付を取得、残り20未満になったら終了
      for i in range(20,len(price_series),SKIP_DATE):
        # 基準日を取得
        base_date = price_series.index[i]
        # 基準日の終値を取得
        base_date_close_price = round(price_series[i],2)
        volume = price_and_volume_df.at[base_date, 'Volume']
        # 3:変動係数,1次近似,株価が十分に上昇か を取得します
        coefficient_of_variation,slope_list,if_close_price_up,max_price,close_price_up_ratio,sigma1,sigma2 = \
          ussi.get_stock_info(price_series,base_date_close_price,i,base_date)
        data = {
                 'code':code,
                 'base_date':base_date,
                 'base_date_close_price':base_date_close_price,
                 'volume':volume,
                 'coefficient_of_variation':coefficient_of_variation,
                 'slope_list':slope_list,
                 'if_close_price_up':if_close_price_up,
                 'close_price_up_ratio':close_price_up_ratio,
                 'sigma1':sigma1,
                 'sigma2':sigma2
                }
        # 企業ごとの結果用dfに代入
        result_df_per_company = save_to_dataframe(result_df_per_company,data)
      # CSV化し保存する
      utils.save_to_csv(result_df_per_company,'got_data/companies/'+code+'.csv')
      print('csvに保存しました\n')

