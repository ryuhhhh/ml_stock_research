"""
予測に使用する本日のデータを取得します
"""
import _1_get_us_stock_list as usl
import _2_get_close_prices_and_volume as pav
import _3_get_us_stock_stats_info as ussi
import VALUES
import utils
import pandas as pd
import os,sys
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))

# 時価総額の閾値(億ドル)
MARKET_CAP_THRESHHOLD = 5

def add_to_dataframe(result_df_per_company,data):
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
            data['rho']]
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
            VALUES.RHO]
    result_df_per_company = pd.DataFrame(index=[], columns=cols)
    result_df_per_company.set_index(VALUES.CODE_AND_DATE_ID,inplace=True)
    # 銘柄リストをループ
    for index, row in us_stock_df.iterrows():

        # 今は情報技術セクターのみ取得
        if row[VALUES.INDUSTRY] != VALUES.IT_INDUSTRY:
            continue
        code = row[VALUES.CODE]
        print(f'{index}番目 {code} {row[VALUES.NAME]}')

        # 2:終値と出来高のdfを取得
        end = datetime.date.today()
        start = end - datetime.timedelta(days=40)
        price_and_volume_df = pav.get_close_price_and_volume_df(code,start,end)

        # 取得できなかった場合スキップ
        if price_and_volume_df.empty:
            continue
        # 2:時価総額を取得(億ドル)
        market_cap = pav.get_market_cap(code)
        # 証券会社が扱っていない可能性があるため時価総額で区切る
        if market_cap < MARKET_CAP_THRESHHOLD:
          print(f'時価総額が{market_cap}億ドル < {MARKET_CAP_THRESHHOLD}億ドル のためためスキップします')
          continue

        price_series = price_and_volume_df.Close

        # 基準日を取得
        base_date = price_series.index[-1]

        # 基準日の終値を取得
        base_date_close_price = round(price_series[-1],2)
        volume = price_and_volume_df.at[base_date, 'Volume']
        # 3:変動係数,1次近似,株価が十分に上昇か を取得します
        coefficient_of_variation,slope_list,rho = \
          ussi.get_stock_info(price_series,base_date_close_price,-1,base_date,True)
        data = {
                 'code':code,
                 'base_date':base_date,
                 'base_date_close_price':base_date_close_price,
                 'volume':volume,
                 'coefficient_of_variation':coefficient_of_variation,
                 'slope_list':slope_list,
                 'rho':rho
                }
        result_df_per_company = add_to_dataframe(result_df_per_company,data)

    # CSV化し保存する
    utils.save_to_csv(result_df_per_company,'got_data/concated_companies/todays_concated_us_list_.csv')
    print('csvに保存しました\n')