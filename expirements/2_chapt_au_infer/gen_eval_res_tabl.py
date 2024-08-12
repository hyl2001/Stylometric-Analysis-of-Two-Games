import pandas as pd

from os.path import join


def gen_tabl(store_root:str, *, models_names:list[str]|None=None):
    if not models_names:
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
    else:
        names = models_names
    
    df_auc = pd.read_excel(join(store_root, 'auc.xlsx'))
    df_acc = pd.read_excel(join(store_root, 'acc.xlsx'))
    df_pre = pd.read_excel(join(store_root, 'pre.xlsx'))
    df_rec = pd.read_excel(join(store_root, 'rec.xlsx'))
    df_f1s = pd.read_excel(join(store_root, 'f1s.xlsx'))


    df_list = []
    for name in names:
        ser_auc = df_auc[name]
        ser_acc = df_acc[name]
        ser_pre = df_pre[name]
        ser_rec = df_rec[name]
        ser_f1s = df_f1s[name]

        data = [
            [ser_auc.median(), ser_auc.std()], # AUC
            [ser_acc.median(), ser_acc.std()], # Accuracy
            [ser_pre.median(), ser_pre.std()], # Precision
            [ser_rec.median(), ser_rec.std()], # Recall
            [ser_f1s.median(), ser_f1s.std()], # F-1 Score
        ]

        idx_name = ['AUC', 'Acc', 'Pre', 'Rec', 'F1S']

        # https://stackoverflow.com/questions/37835508/how-to-do-multi-column-from-tuples
        midx = pd.MultiIndex.from_product([[name], ['Median', 'STD']])
        midy = pd.MultiIndex.from_product([idx_name])

        df_list.append(pd.DataFrame(data, index=midy, columns=midx))
    
    df = pd.concat(df_list, axis='columns').round(4)

    return df
