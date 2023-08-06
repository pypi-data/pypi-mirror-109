# Packaging
last task in ml eng course
# to install
!pip install last_task
# to use 
import last_task\
path=f'{last_task.__path__[0]}/rawdata_new.csv'\
X, y, df = last_task.get_data(path)\
X = last_task.preproc(X)\
y_pred, clf = last_task.train_predict(X, y.to_numpy().ravel(), 'l2', 1, 'lbfgs')
