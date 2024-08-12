import pandas as pd
import numpy as np
import imblearn

from copy import deepcopy
from os.path import join
from math import floor
from typing import Literal

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


class EvalModels:
    def __init__(self, 
                 models_names:list[str],
                 models_instances:list) -> None:
        self.models_names = models_names
        self.models_instances = models_instances

    def __sample(self, X, y):
        # balance dataset
        sm = imblearn.over_sampling.SMOTE()
        x_res, y_res = sm.fit_resample(X, y)
        x_res.index = y_res
        
        proportion_in_whole_data_set = 0.3
        
        dataset_classified = [x_res.loc[i] for i in set(x_res.index)]
        n_test_samples = floor(dataset_classified[0].shape[0] * proportion_in_whole_data_set)
        # Due to the balanced dataset, one sub-dataset shape represents all.

        idx_for_test = [np.random.choice(range(0, i.shape[0]), (n_test_samples,), replace=False) for i in dataset_classified]
        test_x = pd.concat([dataset_classified[i].take(idx_for_test[i]) for i in range(len(dataset_classified))])
        test_y = test_x.index
        
        idx_for_train = [list(set(range(dataset_classified[sub].shape[0])).difference(idx_for_test[sub]))
                        for sub in range(len(dataset_classified))]
        train_x = pd.concat([dataset_classified[i].take(idx_for_train[i]) for i in range(len(dataset_classified))])
        train_y = train_x.index
        
        return train_x, train_y, test_x, test_y

    def __eval(self, X, y, *, 
               is_gi: bool,
               is_multi_class:bool,
               epoches:int=100, 
               hint:str='', 
               average: Literal['micro', 'macro', 'samples', 'weighted', 'binary'] | None = "binary"):
        if is_gi:
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
            y = [mapper[i] for i in y]
        
        clf_auc = {}
        clf_acc = {}
        clf_pre = {}
        clf_rec = {}
        clf_f1s = {}

        X_copied = deepcopy(X)
        y_copied = deepcopy(y)

        for i in range(epoches):
            x, y, t_x, t_y = self.__sample(X_copied, y_copied)

            for name, clf in zip(self.models_names, self.models_instances):
                print(hint, f'Session {i+1} of {epoches}: Evaluating {name}...')

                clf.fit(x, y)

                if name not in clf_auc:
                    clf_auc[name] = []
                if name not in clf_acc:
                    clf_acc[name] = []
                if name not in clf_pre:
                    clf_pre[name] = []
                if name not in clf_rec:
                    clf_rec[name] = []
                if name not in clf_f1s:
                    clf_f1s[name] = []
                
                if is_multi_class:
                    y_prep = clf.predict_proba(t_x)
                else:
                    y_prep = clf.predict(t_x)
                clf_auc[name].append(roc_auc_score(t_y, y_prep, multi_class='ovr'))
                pred = clf.predict(t_x)
                clf_acc[name].append(accuracy_score(t_y, pred))
                clf_pre[name].append(precision_score(t_y, pred, average=average))
                clf_rec[name].append(recall_score(t_y, pred, average=average))
                clf_f1s[name].append(f1_score(t_y, pred, average=average))

        df_auc = pd.DataFrame(clf_auc)
        df_acc = pd.DataFrame(clf_acc)
        df_pre = pd.DataFrame(clf_pre)
        df_rec = pd.DataFrame(clf_rec)
        df_f1s = pd.DataFrame(clf_f1s)

        return df_auc, df_acc, df_pre, df_rec, df_f1s

    def run_eval(self, 
                 X, 
                 y, 
                 save_path:str, 
                 *,
                 is_gi:bool, 
                 is_multi_class:bool,
                 average: Literal['micro', 'macro', 'samples', 'weighted', 'binary']):
        df_auc, df_acc, df_pre, df_rec, df_f1s = \
            self.__eval(X, y, 
                        is_gi=is_gi, 
                        is_multi_class=is_multi_class, 
                        average=average)
        
        df_auc.to_excel(join(save_path, 'auc.xlsx'), index=False)
        df_acc.to_excel(join(save_path, 'acc.xlsx'), index=False)
        df_pre.to_excel(join(save_path, 'pre.xlsx'), index=False)
        df_rec.to_excel(join(save_path, 'rec.xlsx'), index=False)
        df_f1s.to_excel(join(save_path, 'f1s.xlsx'), index=False)
