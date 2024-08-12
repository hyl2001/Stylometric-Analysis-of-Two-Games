import pandas as pd
import seaborn as sns
import matplotlib.font_manager as fm

from matplotlib import pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
from typing import Literal

font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')

def draw_lda_fig(stylo_path:str, 
                 save_name:str, 
                 game_type:int, 
                 chapt_num_lookup_tbl:dict|None=None,
                 *,
                 kind:Literal['lda', 'pca']='lda'):
    df = pd.read_excel(stylo_path)
    df = df[df['game'] == game_type]
    y = df['chapt_major']
    x = df.drop([
        'Unnamed: 0',
        'file_name',
        'game',
        'chapt_major'
        ], axis='columns')
    
    if kind == 'lda':
        lda = LinearDiscriminantAnalysis(n_components=2)

        lda = lda.set_output(transform='pandas')
        fitted = lda.fit(x, y)
        
        res = fitted.transform(x)
        df_decomp = pd.concat([res, y], axis='columns')
        
        centroi = fitted.transform(pd.DataFrame(lda.means_, columns=lda.feature_names_in_))
        df_centroi = pd.concat([centroi, pd.DataFrame(set(y), columns=['chapt_major'])], axis='columns')
    elif kind == 'pca':
        pca = PCA(n_components=2)

        pca = pca.set_output(transform='pandas')
        fitted = pca.fit(x, y)

        res = fitted.transform(x)
        df_decomp = pd.concat([res, y], axis='columns')

    ax = plt.figure(figsize=(8, 6), dpi=1000).subplots(1, 1)

    # https://github.com/suqingdong/sci_palettes/blob/ca80b01e9424e191329a3da465d83a85fcde0bec/sci_palettes/palettes.py#L240C1-L250C7
    palette = [
        "#800000",
        "#767676",
        "#FFA319",
        "#8A9045",
        "#155F83", 
        "#C16622",
        "#8F3931",
        "#58593F",
        "#350E20"
    ]
     
    for idx, chapt_num in enumerate(set(df_decomp['chapt_major'].to_list())):
        chapt = df_decomp[df_decomp['chapt_major'] == chapt_num]

        if chapt_num_lookup_tbl:
            chapt_label = chapt_num_lookup_tbl.get(chapt_num, chapt_num)
        else:
            chapt_label = chapt_num

        ax.scatter(chapt.iloc[:, 0], 
                   chapt.iloc[:, 1], 
                   c=palette[idx],
                   label=chapt_label,
                   alpha=.8)
     
        if kind == 'lda':
            centroi = df_centroi[df_centroi['chapt_major'] == chapt_num]
            ax.scatter(centroi.iloc[:, 0], 
                    centroi.iloc[:, 1], 
                    marker='*', 
                    c=palette[idx],
                    s=200, 
                    edgecolor="black")
            ax.text(centroi.iloc[:, 0]+.1,
                    centroi.iloc[:, 1]+.1,
                    s=f'{chapt_label}',
                    fontproperties=font)
    
    # https://stackoverflow.com/questions/21933187/how-to-change-legend-fontname-in-matplotlib
    L = ax.legend()
    plt.setp(L.texts, family='simsun')
    
    ax.set_xlabel(f'Function 1\n{fitted.explained_variance_ratio_[0] * 100:.2f}%')
    ax.set_ylabel(f'Function 2\n{fitted.explained_variance_ratio_[1] * 100:.2f}%')
    
    plt.tight_layout()
    plt.savefig(save_name)
