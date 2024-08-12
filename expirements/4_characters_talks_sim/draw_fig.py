import radialtree
import pandas as pd
import scipy.cluster.hierarchy as sch
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt


def draw(data_xlsx_path:str, output_name:str):
    font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')
    
    df = pd.read_excel(data_xlsx_path)
    df = df.drop(columns=['Unnamed: 0'])

    labels_ = [i.split('_')[0] for i in df.pop('file_name').to_list()]


    fig, ax = plt.subplots(1, 1, figsize=(15, 15), dpi=1000)
    Y = sch.linkage(df, method="average")
    Z2 = sch.dendrogram(
        Y,
        no_plot=True,
        labels=labels_,
    )
    radialtree.radialTreee(Z2, ax=ax, fontsize=10, fontproperties=font, sample_classes={'name': labels_})
    fig.savefig(output_name)
