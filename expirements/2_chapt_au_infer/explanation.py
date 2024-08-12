import pandas as pd
import shap
import imblearn
import matplotlib.font_manager as fm

from xgboost import XGBClassifier
from typing import Literal
from matplotlib import pyplot as plt


def gen_exp_figs(quant_sty_path:str, 
                 game_type:Literal[0, 1], 
                 save_path:str, 
                 lookup_tabl:dict):
    df = pd.read_excel(quant_sty_path)\
           .drop('file_name', axis='columns')\
           .drop('Unnamed: 0', axis='columns')
    df = df[df['game'] == game_type]
    chapt_num = df.pop('chapt_major')
    font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')
    clf = XGBClassifier()

    if game_type == 1: # The game is Genshin Impact.
        mapper = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            90: 5,
            91: 6,
            92: 7
        }
        chapt_num = [mapper[i] for i in chapt_num]
        reverse_mapper = dict(zip(list(mapper.values()), list(mapper.keys())))
    
    sm = imblearn.over_sampling.SMOTE()
    X, y = sm.fit_resample(df, chapt_num)

    clf.fit(X, y)
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X, y)

    if game_type == 1:
        y = [reverse_mapper[i] for i in y]

    # https://github.com/shap/shap/issues/3630#issuecomment-2232878093
    ensured_list_shap_values = [shap_values[:,:,i] for i in range(shap_values.shape[2])]
    class_names = list(set([lookup_tabl[i] for i in y]))
    shap.summary_plot(ensured_list_shap_values,
                      class_names=class_names,
                      feature_names=df.columns, 
                      plot_type='bar',
                      max_display=10, 
                      show=False)
     
    # Manually draw a legend with CJK font
    ax = plt.gca()
    plt.legend(*ax.get_legend_handles_labels(), prop=font)
    plt.savefig(save_path)

    plt.clf()
