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
import todays_get_data_for_predict
import edit_got_data
import make_model
import argparse
import predict

if __name__ == "__main__":
    """
    args:
        -b:
           no_skip: 全てを実行
           skip_get: データ取得をスキップ
           skip_get_transform: データ取得,データ変換までをスキップ
        -t:
           fit: 学習を行います
           predict: 予測を行います
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--behavior',type=str,help="振る舞いを指定",default='no_skip')
    parser.add_argument('-t','--type',type=str,help="学習か予測かを指定",default='fit')
    args = parser.parse_args()

    FIT  = 'fit'
    PREDICT = 'predict'

    NO_SKIP = 'no_skip'
    SKIP_GET = 'skip_get'
    SKIP_GET_TRANSFORM = 'skip_get_transform'

    if args.type not in [FIT,PREDICT]:
        print('typeの引数が正しくないため終了します')
        sys.exit()

    if args.behavior not in [NO_SKIP,SKIP_GET,SKIP_GET_TRANSFORM]:
        print('--behaviorの引数が正しくないため終了します')
        sys.exit()

    # 学習の場合
    if args.type == FIT:
        # データ取得
        if args.behavior == NO_SKIP:
            _0_get_us_stock_info.main()
            _4_concatenate_csvs.main()
        # データ変換
        if args.behavior != SKIP_GET_TRANSFORM:
            edit_got_data.main()
        # モデル作成
        make_model.main()
    # 予測の場合
    elif args.type == PREDICT:
        # データ取得
        if args.behavior == NO_SKIP:
            todays_get_data_for_predict.main()
        # データ変換
        if args.behavior != SKIP_GET_TRANSFORM:
            edit_got_data.main(is_fit=False)
        # 予測
        predict.main()
