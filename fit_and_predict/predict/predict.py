"""
本日分のデータを用いて予測を行います
"""
import pickle
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
import VALUES
import pandas as pd
import numpy as np

def load_model(name='fit_and_predict/models/model.pickle'):
    """
    モデルをロードします
    """
    with open(name, mode='rb') as fp:
        model = pickle.load(fp)
    return model

def load_todays_data(path='edited_data/todays.csv'):
    """
    本日分のデータをロードします
    """
    df = pd.read_csv(path,encoding='utf-8')
    return df

if __name__ == "__main__":
    target_columns = [
                        VALUES.COEFFICIENT_OF_VARIATION,
                        VALUES.SLOPE_OF_LAST_5_DAYS,
                        VALUES.SLOPE5_DEVIDE_RHO,
                     ]

    # 本日分のデータを取得
    df = load_todays_data()
    origin_df = df.copy()
    df = df[target_columns]

    # モデルを取得
    model = load_model()
    predictions = model.predict(df)

    for index, prediction in np.ndenumerate(predictions):
        if int(prediction) == 1:
            print(origin_df.iloc[index].ID)