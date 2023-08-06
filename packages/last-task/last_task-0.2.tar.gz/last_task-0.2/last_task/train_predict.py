from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

def train_predict(X, y, penalty, C, solver):
    '''module dockstring'''
    # Linear model
    clf = LogisticRegression(penalty=penalty, C=C, solver=solver)
    yhat = cross_val_predict(clf, X, y, cv=10)
    return yhat, clf
