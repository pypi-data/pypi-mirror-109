import numpy as np
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

def preproc(X):
    '''module dockstring'''
    X = preprocessing.scale(X)
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X)
    X = imp.transform(X)
    return X

