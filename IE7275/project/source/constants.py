from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


PARAMS = {
    'estimator': [
        GaussianNB,
        KNeighborsClassifier,
        # LogisticRegression,
        LinearDiscriminantAnalysis,
        SVC,
        DecisionTreeClassifier
    ],
    'dropna': [True, False],
    'numerify': [True, False],
    'numerify_by': ['codes', 'one-hot'],
    'normalize': [True, False],
    'normalize_by': ['std', 'max-min'],
    'pca': [True, False]
}
