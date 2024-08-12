import eval_models
import pandas as pd

# NOTE
# Unblock imports below when using. Toggle them for saving time.

from random import randint
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from xgboost import XGBClassifier

names = [
    "Nearest Neighbors",
    "Linear SVM",
    "RBF SVM",
    "Decision Tree",
    "Random Forest",
    "Neural Net",
    "AdaBoost",
    "Naive Bayes",
    "XGBoost"
]

SEED = randint(0, 4294967295)

dec_tree = DecisionTreeClassifier()
    
classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", probability=True, C=0.025, max_iter=10_0000, random_state=SEED),
    SVC(gamma=2, probability=True, C=1, max_iter=10_0000, random_state=SEED),
    DecisionTreeClassifier(max_depth=5, random_state=SEED),
    RandomForestClassifier(
        max_depth=5, n_estimators=100, max_features=1, random_state=SEED
    ),
    MLPClassifier(alpha=1, max_iter=1000, random_state=SEED),
    AdaBoostClassifier(estimator=dec_tree, algorithm="SAMME", random_state=SEED),
    GaussianNB(),
    XGBClassifier()
]
e = eval_models.EvalModels(names, classifiers)

#### game_infer #######################################################

# col_to_drop = [
#     'Unnamed: 0', 
#     'chapt_major', 
#     'file_name'
# ]

# df = pd.read_excel('concat.xlsx').drop(col_to_drop, axis='columns')
# game = df.pop('game')

# e.run_eval(df, game.tolist(), 'expirements\\1_game_infer\\model_eval_res',
#            is_gi=False,
#            is_multi_class=False,
#            average='binary')

#### game_infer #######################################################


#### chapt_infer (GI) #################################################

# col_to_drop = [
#     'Unnamed: 0', 
#     'file_name',
# ]

# df = pd.read_excel('concat.xlsx').drop(col_to_drop, axis='columns')
# df = df[df['game'] == 1].drop('game', axis='columns')
# chapt = df.pop('chapt_major')

# e.run_eval(df, chapt.to_list(), 'expirements\\2_chapt_au_infer\\model_eval_res\\GI',
#            is_gi=True,
#            is_multi_class=True,
#            average='macro')

#### chapt_infer (GI) #################################################

#### chapt_infer (SR) #################################################

# col_to_drop = [
#     'Unnamed: 0', 
#     'file_name',
# ]

# df = pd.read_excel('concat.xlsx').drop(col_to_drop, axis='columns')
# df = df[df['game'] == 0].drop('game', axis='columns')
# chapt = df.pop('chapt_major')

# e.run_eval(df, chapt.to_list(), 'expirements\\2_chapt_au_infer\\model_eval_res\\SR',
#            is_gi=False,
#            is_multi_class=True,
#            average='macro')

#### chapt_infer (SR) #################################################


#### chapt_infer (GI LDA) #############################################

# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# col_to_drop = [
#     'Unnamed: 0', 
#     'file_name',
# ]

# df = pd.read_excel('concat.xlsx').drop(col_to_drop, axis='columns')
# df = df[df['game'] == 1].drop('game', axis='columns')
# chapt = df.pop('chapt_major')

# names = ['LDA']
# classifiers = [LinearDiscriminantAnalysis(n_components=2)]

# e = eval_models.EvalModels(names, classifiers)
# e.run_eval(df, chapt.to_list(), 'expirements\\2_chapt_au_infer\\model_eval_res\\GI_LDA',
#            is_gi=True,
#            is_multi_class=True,
#            average='macro')

#### chapt_infer (GI LDA) #############################################

#### chapt_infer (SR LDA) #############################################

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

col_to_drop = [
    'Unnamed: 0', 
    'file_name',
]

df = pd.read_excel('concat.xlsx').drop(col_to_drop, axis='columns')
df = df[df['game'] == 0].drop('game', axis='columns')
chapt = df.pop('chapt_major')

names = ['LDA']
classifiers = [LinearDiscriminantAnalysis(n_components=2)]

e = eval_models.EvalModels(names, classifiers)
e.run_eval(df, chapt.to_list(), 'expirements\\2_chapt_au_infer\\model_eval_res\\SR_LDA',
           is_gi=False,
           is_multi_class=True,
           average='macro')

#### chapt_infer (SR LDA) #############################################
