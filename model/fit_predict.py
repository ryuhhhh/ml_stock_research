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
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
import utils
import VALUES
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.metrics import confusion_matrix,precision_score
from sklearn.svm import SVC

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

def extract_feature_value(X,columns):
    """
    訓練データから必要な特徴量を抜き出します
    """
    return  X[columns]

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
    confusion_matrix_test,precision_score_test = check_confusion_matrix_and_precision(model,X_train,y_train)
    return val_score,confusion_matrix_train,precision_score_train,confusion_matrix_test,precision_score_test


if __name__ == "__main__":
    X_train,y_train = get_train_data()
    X_test,y_test = get_test_data()
    # print(X_train.columns,y_train.name)
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
                        VALUES.VOLUME_DEVIDE_CLOSE_PRICE,
                        # VALUES.RHO_DEVIDE_CLOSE_PRICE
                    ]
    X_train = extract_feature_value(X_train,target_columns)
    X_test = extract_feature_value(X_test,target_columns)

    # SGDClassifier
    sgd_clf = SGDClassifier(random_state=42)
    # ガウスRBFカーネル => 要グリッドサーチ
    svm_clf = SVC(kernel='poly',degree=3,coef0=1,C=5)

    print(check_all(sgd_clf,X_train,y_train,X_test,y_test))
    print(check_all(svm_clf,X_train,y_train,X_test,y_test))