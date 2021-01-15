"""
モデルを学習させ性能を測ります
    - SGDClassifier
    - ガウスRBFカーネルSVM
    - DecisionTree
    - RandomForest
    - VotingClassifierで上記をアンサンブル
    - RandomForestでバギング
"""
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
import utils
import VALUES
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.metrics import confusion_matrix,precision_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,VotingClassifier

def get_train_data():
    print('データ読み込み中...')
    df = utils.read_csv('edited_data/train.csv')
    print('データ読み込み完了')
    # 特徴量データ
    X_train = df.drop(VALUES.IF_10per_UP_NEXT_10_DAYS, axis=1)
    # 教師データ
    y_train = df[VALUES.IF_10per_UP_NEXT_10_DAYS]
    return X_train,y_train

def get_test_data():
    print('テストデータ読み込み中...')
    df = utils.read_csv('edited_data/test.csv')
    print('テストデータ読み込み完了')
    # 特徴量データ
    X_test = df.drop(VALUES.IF_10per_UP_NEXT_10_DAYS, axis=1)
    # 教師データ
    y_test = df[VALUES.IF_10per_UP_NEXT_10_DAYS]
    return X_test,y_test

def check_model_cross_val_score(model,X,y):
    """
    交差検証でモデルの性能を評価します
    """
    return cross_val_score(model,X,y,cv=3,scoring='accuracy')

def check_confusion_matrix_and_precision(model,X,y):
    """
    混同行列/適合率で分類器の性能を評価します。
    (分類はこちらの方が優位)
    """
    # 予測結果を返す
    y_pred = cross_val_predict(model,X,y,cv=3)
    return confusion_matrix(y,y_pred),precision_score(y,y_pred)

def check_all(model,X_train,y_train,X_test,y_test):
    """
    交差検証,混同行列,適合率 を評価します
    """
    val_score = check_model_cross_val_score(model,X_train,y_train)
    confusion_matrix_train,precision_score_train = check_confusion_matrix_and_precision(model,X_train,y_train)
    confusion_matrix_test,precision_score_test = check_confusion_matrix_and_precision(model,X_test,y_test)
    return val_score,confusion_matrix_train,precision_score_train,confusion_matrix_test,precision_score_test

def save_model(model,name='model.pickle'):
    """
    モデルを保存します
    """
    with open(name, mode='wb') as fp:
        pickle.dump(model, fp)

if __name__ == "__main__":
    X_train,y_train = get_train_data()
    X_test,y_test = get_test_data()
    target_columns = [
                        # VALUES.CLOSING_PRICE,
                        VALUES.COEFFICIENT_OF_VARIATION,
                        VALUES.SLOPE_OF_LAST_5_DAYS,
                        # VALUES.SLOPE_OF_LAST_10_DAYS,
                        # VALUES.SLOPE_OF_LAST_15_DAYS,
                        # VALUES.SLOPE_OF_LAST_20_DAYS,
                        # VALUES.RHO,
                        VALUES.SLOPE5_DEVIDE_RHO,
                        # VALUES.VOLUME_DEVIDE_RHO,
                        # VALUES.SLOPE5_DEVIDE_CLOSE_PRICE,
                        # VALUES.VOLUME_DEVIDE_CLOSE_PRICE,
                        # VALUES.RHO_DEVIDE_CLOSE_PRICE
                    ]
    X_train = X_train[target_columns]
    X_test = X_test[target_columns]

    # SGDClassifier
    sgd_clf = SGDClassifier(random_state=42)
    # ガウスRBFカーネル => 要グリッドサーチ
    svm_clf = SVC(kernel='rbf',gamma=5,C=5)
    # 決定木
    tree_clf = DecisionTreeClassifier(max_depth=3)
    # ランダムフォレスト
    rnd_clf = RandomForestClassifier(n_estimators=500,max_leaf_nodes=32,n_jobs=-1)
    # 投票分類器
    voting_clf = VotingClassifier(
        estimators=[('sgd_clf',sgd_clf),('tree_clf',tree_clf),('rnd_clf',rnd_clf)]
    )

    voting_clf.fit(X_train,y_train)
    save_model(voting_clf)
    # val_score,confusion_matrix_train,precision_score_train,confusion_matrix_test,precision_score_test =\
    #      check_all(voting_clf,X_train,y_train,X_test,y_test)
    # print(confusion_matrix_train)
    # print(precision_score_train)
    # print(confusion_matrix_test)
    # print(precision_score_test)

    # SGDClassifierで0.52を出力
    # # target_columns = [
                        # # VALUES.CLOSING_PRICE,
                        # VALUES.COEFFICIENT_OF_VARIATION,
                        # VALUES.SLOPE_OF_LAST_5_DAYS,
                        # # VALUES.SLOPE_OF_LAST_10_DAYS,
                        # # VALUES.SLOPE_OF_LAST_15_DAYS,
                        # # VALUES.SLOPE_OF_LAST_20_DAYS,
                        # # VALUES.RHO,
                        # VALUES.SLOPE5_DEVIDE_RHO,
                        # # VALUES.VOLUME_DEVIDE_RHO,
                        # # VALUES.SLOPE5_DEVIDE_CLOSE_PRICE,
                        # # VALUES.VOLUME_DEVIDE_CLOSE_PRICE,
                        # # VALUES.RHO_DEVIDE_CLOSE_PRICE
    # #                 ]

    # テストセットで0.79
    # # SGDClassifier
    # sgd_clf = SGDClassifier(random_state=42)
    # # ランダムフォレスト
    # rnd_clf = RandomForestClassifier(n_estimators=500,max_leaf_nodes=32,n_jobs=-1)
    # # 投票分類器
    # voting_clf = VotingClassifier(
    #     estimators=[('sgd_clf',sgd_clf),('rnd_clf',rnd_clf)]
    # )