import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
import seaborn as sns
import torch
import ddks

from matplotlib import pyplot as plt
from copy import deepcopy
from sklearn.decomposition import PCA


def draw(a:np.array, 
         savepath:str, 
         x_lookup:dict,
         y_lookup:dict,
         xlable:str='崩坏：星穹铁道', 
         ylable:str='原神',
         *,
         x_ticks_rotation = 0,
         y_ticks_rotation = 0,
         x_ha = 'center',
         y_ha = 'right'):
    font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')
     
    ax = sns.heatmap(a, annot=True, fmt='.2f')
     
    ax.set_xticklabels(
        [x_lookup[int(i.get_text())] for i in ax.axes.get_xticklabels()],
        fontproperties=font,
        rotation = x_ticks_rotation,
        ha=x_ha
    )
    ax.set_yticklabels(
        [y_lookup[int(i.get_text())] for i in ax.axes.get_yticklabels()],
        fontproperties=font,
        rotation = y_ticks_rotation,
        ha=y_ha
    )
    ax.set_xlabel(xlable, fontproperties=font)
    ax.set_ylabel(ylable, fontproperties=font)

    plt.savefig(savepath)


def compare(a:pd.DataFrame, name_of_a:str, b:pd.DataFrame, name_of_b:str, n_components:int=10):
    sim_list = []
    sim_std_list = []
    a_chapt = set(a['chapt_major'])
    b_chapt = set(b['chapt_major'])
    pca_a = PCA(n_components)
    pca_b = PCA(n_components)
    exp_var_ratio = {name_of_a: [], name_of_b: []}

    for a_chapt_num in a_chapt:
        print(f'Chapter number of {name_of_a}:', a_chapt_num)

        vec_a = a[a['chapt_major'] == a_chapt_num]
        vec_a = vec_a.drop('chapt_major', axis='columns')
        vec_a = vec_a.to_numpy()

        # Reduce dimension of a
        fitted_a = pca_a.fit(vec_a)
        exp_var_ratio_a = fitted_a.explained_variance_ratio_.sum()
        print(f'Explained variance ratio ({name_of_a}):', exp_var_ratio_a)
        exp_var_ratio[name_of_a].append(exp_var_ratio_a)

        vec_a = fitted_a.transform(vec_a)
        vec_a = torch.from_numpy(vec_a).to('cuda:0')
     
        temp_sim_list = []
        temp_sim_std_list = []

        for b_chapt_num in b_chapt:
            print(f'Chapter number of {name_of_b}:', b_chapt_num)

            vec_b = b[b['chapt_major'] == b_chapt_num]
            vec_b = vec_b.drop('chapt_major', axis='columns')
            vec_b = vec_b.to_numpy()

            fitted_b = pca_b.fit(vec_b)
            exp_var_ratio_b = fitted_b.explained_variance_ratio_.sum()
            print(f'Explained variance ratio ({name_of_b}):', exp_var_ratio_b)
            exp_var_ratio[name_of_b].append(exp_var_ratio_b)

            vec_b = fitted_b.transform(vec_b)
            vec_b = torch.from_numpy(vec_b).to('cuda:0')
     

            calculation = ddks.methods.ddKS()
            temp_sim_list.append(1 - calculation(vec_a, vec_b).cpu())
     
        sim_list.append(deepcopy(temp_sim_list))
        sim_std_list.append(deepcopy(temp_sim_std_list))
        temp_sim_list.clear()
        temp_sim_std_list.clear()
    
    return np.array(sim_list), np.array(sim_std_list), exp_var_ratio
