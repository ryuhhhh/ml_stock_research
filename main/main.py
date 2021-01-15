"""
データの取得~学習までを実行します
"""
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../get_data'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../edit_data'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../fit_and_predict/fit'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../fit_and_predict/predict'))
import _0_get_us_stock_info
import _4_concatenate_csvs
import _todays_get_data_for_predict
import edit_got_data
import make_model
import argparse
import predict

if __name__ == "__main__":
    """
    args:
        -b:
           0: データ変換までをスキップ
           1: データ取得までをスキップ
           2: 全てを実行
        -t:
           fit: 学習を行います
           predict: 予測を行います
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--behavior',type=int,help="振る舞いを指定",default=2)
    parser.add_argument('-t','--type',type=str,help="振る舞いを指定",default='fit')
    args = parser.parse_args()
    FIT  = 'fit'
    PREDICT = 'predict'

    # 学習の場合
    if args.type == FIT:
        # データ取得
        if args.behavior >= 2:
            _0_get_us_stock_info.main()
            _4_concatenate_csvs.main()
        # データ変換
        if args.behavior >= 1:
            edit_got_data.main()
        # モデル作成
        make_model.main()
    # 予測の場合
    elif args.type == PREDICT:
        # データ取得
        if args.behavior >= 2:
            _todays_get_data_for_predict.main()
        # データ変換
        if args.behavior >= 1:
            edit_got_data.main(is_fit=False)
        # モデル作成
        predict.main()