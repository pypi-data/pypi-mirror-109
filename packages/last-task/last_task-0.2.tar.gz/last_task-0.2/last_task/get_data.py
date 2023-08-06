import pandas as pd
import os


def get_data(path='last_task/rawdata_new.csv'):
    '''module dockstring'''
    print(os.getcwd())
    df = pd.read_csv(path)
    y = df[["cons_general"]]
    y[y < 4] = 0
    y[y >= 4] = 1
    X = df.drop(columns=["cons_general"])
    return X, y, df
