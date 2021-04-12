## ml_stock_research
* 今後10日間で株価が10%あがるか分類します。 

## 性能
* 適合率 63%
* 再現率 14%

## 使用した特徴量
* 終値
* 出来高
* 時価総額
* 変動係数
* 1次近似の傾き
* 分散

## フォルダ,ファイルの説明
### /get_data
1. 米国株の上記特徴量を取得
2. /data/got_dataに格納

### /analayse/analyse_got_data.py
* 各特徴量同士および各特徴量を組み合わせた値と株価の上昇量との相関係数を調査
  * 高いものを優先的に学習で使用する特徴量にしていく

### /edit_data/edit_got_data.py
* 欠損値補完/標準化/次元削減(pca)を実施
* その後、訓練データや教師データに分割

### /common/utils.py
* 共通処理を置く

### /common/VALUES.py
* 共通定数一覧

### /fit_and_predict/make_model.py
* モデル学習 -> 性能評価 -> モデル保存 を実施
* モデルはSGD分類器とランダムフォレストの投票分類器

### /fit_and_predict/predict.py
* 保存したモデルを利用し予測，コンソールにその結果を表示する

#### (例)2021/4/12に予測した結果
* IDEX
* JKS
* MARA
* MIME
* MVIS
* QTT
* RMNI
* TTD
