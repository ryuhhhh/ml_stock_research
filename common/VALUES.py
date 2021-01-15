CODE_AND_DATE_ID = 'ID'
BASE_DATE = '基準日'
CODE = 'コード'
NAME = '名称'
CLOSING_PRICE = '終値'
INDUSTRY = '業種'
VOLUME = '出来高'
COEFFICIENT_OF_VARIATION = '変動係数'
IF_10per_UP_NEXT_10_DAYS = '次の10日で株価が10%以上上がったか'
CLOSE_PRICE_UP_RATIO = '10日間の株価上昇率'
RHO = '標準偏差'

SLOPE_OF_LAST_5_DAYS = '直近5日の1次近似の傾き'
SLOPE_OF_LAST_10_DAYS = '直近10日の1次近似の傾き'
SLOPE_OF_LAST_15_DAYS = '直近15日の1次近似の傾き'
SLOPE_OF_LAST_20_DAYS = '直近20日の1次近似の傾き'

# 追加特徴量
SLOPE5_DEVIDE_RHO = '傾き5_割る_標準偏差'
VOLUME_DEVIDE_RHO = '出来高_割る_標準偏差'
SLOPE5_DEVIDE_CLOSE_PRICE = '傾き5_割る_終値'
VOLUME_DEVIDE_CLOSE_PRICE = '出来高_割る_終値'
RHO_DEVIDE_CLOSE_PRICE = '標準偏差_割る_終値'
VOLUME_DEVIDE_SLOPE15 = '出来高_割る_傾き15'

# 訓練データ用カラム
TRAIN_COLS = [CODE_AND_DATE_ID,
              BASE_DATE,
              CLOSING_PRICE,
              VOLUME,
              SLOPE_OF_LAST_5_DAYS,
              SLOPE_OF_LAST_10_DAYS,
              SLOPE_OF_LAST_15_DAYS,
              SLOPE_OF_LAST_20_DAYS,
              COEFFICIENT_OF_VARIATION,
              IF_10per_UP_NEXT_10_DAYS,
              CLOSE_PRICE_UP_RATIO,
              RHO]

# 標準化処理対象カラム
STANDARDIZE_TARGET_COLS = [VOLUME,
                           SLOPE_OF_LAST_5_DAYS,
                           SLOPE_OF_LAST_10_DAYS,
                           SLOPE_OF_LAST_15_DAYS,
                           SLOPE_OF_LAST_20_DAYS,
                           COEFFICIENT_OF_VARIATION,
                           SLOPE5_DEVIDE_RHO,
                           VOLUME_DEVIDE_RHO,
                           SLOPE5_DEVIDE_CLOSE_PRICE,
                           VOLUME_DEVIDE_CLOSE_PRICE,
                           RHO_DEVIDE_CLOSE_PRICE,
                           VOLUME_DEVIDE_SLOPE15
                           ]

# 予測用カラム
PREDICT_COLS = [CODE_AND_DATE_ID,
                BASE_DATE,
                CLOSING_PRICE,
                VOLUME,
                SLOPE_OF_LAST_5_DAYS,
                SLOPE_OF_LAST_10_DAYS,
                SLOPE_OF_LAST_15_DAYS,
                SLOPE_OF_LAST_20_DAYS,
                COEFFICIENT_OF_VARIATION,
                RHO]

CSV_ROOT_PATH = 'got_data'
US_STOCK_LIST_CSV_NAME = 'us_stocks_list.csv'

# セクター
IT_INDUSTRY = '情報技術'
