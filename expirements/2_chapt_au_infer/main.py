import pandas as pd
import draw_fig
import gen_eval_res_tabl
import explanation

from os.path import join
from os import listdir

'''
Game Code:
    0 -> SR
    1 -> GI
'''
sr_chapt_lookup = {
    0: '序章',
    1: '第一章',
    2: '第二章',
    3: '第三章'
}

gi_chapt_lookup = {
    0: '序章',
    1: '第一章',
    2: '第二章',
    3: '第三章',
    4: '第四章',
    90: '间章 风起鹤归',
    91: '间章 危途疑踪',
    92: '间章 倾落伽蓝'
}

save_root = 'expirements\\2_chapt_au_infer\\figs_tbls'

# draw_fig.draw_lda_fig('concat.xlsx', f'{save_root}\\SR_chapt.png', 0, sr_chapt_lookup)
# print('Done drawing fig of HSR.')

# draw_fig.draw_lda_fig('concat.xlsx', f'{save_root}\\GI_chapt.png', 1, gi_chapt_lookup)
# print('Done drawing fig of GI.')


draw_fig.draw_fig('concat.xlsx', f'{save_root}\\SR_chapt_PCA.png', 0, sr_chapt_lookup, kind='pca')
print('Done drawing fig of HSR.')

draw_fig.draw_fig('concat.xlsx', f'{save_root}\\GI_chapt_PCA.png', 1, gi_chapt_lookup, kind='pca')
print('Done drawing fig of GI.')


# gi_dir_root = 'expirements\\2_chapt_au_infer\\model_eval_res\\GI'
# gen_eval_res_tabl.gen_tabl(gi_dir_root).T \
#                  .to_excel(join(save_root, 'GI.xlsx'))

# sr_dir_root = 'expirements\\2_chapt_au_infer\\model_eval_res\\SR'
# gen_eval_res_tabl.gen_tabl(sr_dir_root).T \
#                  .to_excel(join(save_root, 'SR.xlsx'))


# name = ['LDA']

# gi_dir_root = 'expirements\\2_chapt_au_infer\\model_eval_res\\GI_LDA'
# gen_eval_res_tabl.gen_tabl(gi_dir_root, models_names=name).T \
#                  .to_excel(join(save_root, 'GI_LDA.xlsx'))

# sr_dir_root = 'expirements\\2_chapt_au_infer\\model_eval_res\\SR_LDA'
# gen_eval_res_tabl.gen_tabl(sr_dir_root, models_names=name).T \
#                  .to_excel(join(save_root, 'SR_LDA.xlsx'))


# explanation.gen_exp_figs('concat.xlsx', 0, join(save_root, 'shap\\SR.png'), sr_chapt_lookup)
# explanation.gen_exp_figs('concat.xlsx', 1, join(save_root, 'shap\\GI.png'), gi_chapt_lookup)
