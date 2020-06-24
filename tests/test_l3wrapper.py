import pytest
from l3wrapper.l3wrapper import L3Classifier
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import os
from joblib import dump, load
import pickle


@pytest.fixture
def dataset_X_y():
    X = np.loadtxt('tests/data/car.data', dtype=object, delimiter=',')
    y = X[:, -1]
    X = X[:, :-1]
    return X, y


def test_fit_predict(dataset_X_y):
    X, y = dataset_X_y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    clf = L3Classifier().fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    assert y_pred.shape[0] == X_test.shape[0]
    assert len(clf.labeled_transactions_) == X_test.shape[0]
    print(clf.labeled_transactions_[1].matched_rules,
            clf.labeled_transactions_[1].used_level)
    print(len([t for t in clf.labeled_transactions_ if t.used_level == -1]))


def test_save_human_readable(dataset_X_y):
    X, y = dataset_X_y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    clf = L3Classifier().fit(X_train, y_train, save_human_readable=True)
    files = [f for f in os.listdir() if f.startswith(f"{clf.current_token_}")]
    assert len(files) == 2 # level 1 and level 2


def test_training_files(dataset_X_y):
    X, y = dataset_X_y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    clf = L3Classifier().fit(X_train, y_train, remove_files=False)
    files = [f for f in os.listdir() if f.startswith(f"{clf.current_token_}")]
    assert len(files) == 7 # all the stuff left by L3 


def test_save_load(dataset_X_y):
    X, y = dataset_X_y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    clf = L3Classifier().fit(X_train, y_train)

    dump(clf, "clf_pre_predict.joblib")

    y_pred = clf.predict(X_test)
    assert y_pred.shape[0] == X_test.shape[0]
    assert len(clf.labeled_transactions_) == X_test.shape[0]

    dump(clf, "clf.joblib")
    clf_l = load("clf.joblib")
    assert len(clf.lvl1_rules_) == len(clf_l.lvl1_rules_)

    with open("clf.pickle", "wb") as fp:
        pickle.dump(clf, fp)
    with open("clf.pickle", "rb") as fp:
        clf_l = pickle.load(fp)
    assert len(clf.lvl2_rules_) == len(clf_l.lvl2_rules_)


# column_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
# 
# 
# X = np.loadtxt('car.data', dtype=object, delimiter=',')
# y = X[:, -1]
# X = X[:, :-1]
# 
# param_grid = {
#     'min_sup': [0.01, 0.005, 0.02, 0.1],
#     'min_conf': [0.5, 0.25, 0.75],
#     'max_matching': [1, 2, 5, 10, 20],
#     'specialistic_rules': [True, False],
#     'max_length': [0, 2, 4, 6]
# }
# 
# clf = GridSearchCV(L3Classifier(), param_grid, n_jobs=-1)
# clf.fit(X, y)
# 
# print(clf.best_estimator_)
# print(clf.best_score_)
