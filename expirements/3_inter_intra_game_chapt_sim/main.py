import dist
import pandas as pd
import matplotlib.font_manager as fm

from matplotlib import pyplot as plt


font = fm.FontProperties(fname='c:\\windows\\fonts\\simsun.ttc')

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
    5: '间章 风起鹤归', # 90
    6: '间章 危途疑踪', # 91
    7: '间章 倾落伽蓝'  # 92
}

df = pd.read_excel('concat.xlsx')

df_sr = df[df['game']==0]
df_gi = df[df['game']==1]

cols_to_drop = [
    'Unnamed: 0',
    'file_name',
    'game',
]
df_sr_cln = df_sr.drop(cols_to_drop, axis='columns')
df_gi_cln = df_gi.drop(cols_to_drop, axis='columns')

# Inter
# sim_arr, sim_std_arr, exp_var_ratio = dist.compare(df_gi_cln, 'GI', df_sr_cln, 'SR', 10)

# dist.draw(sim_arr, 
#           'expirements\\3_inter_intra_game_chapt_sim\\inter\\sim.png', 
#           sr_chapt_lookup, 
#           gi_chapt_lookup)

# plt.figure()
# plt.boxplot(exp_var_ratio.values(), showmeans=True)
# plt.xticks([1, 2], ['原神', '崩坏：星穹铁道'], fontproperties=font)
# plt.savefig('expirements\\3_inter_intra_game_chapt_sim\\inter\\explained_variance.png')

# Intra
# GI
sim_arr, sim_std_arr, exp_var_ratio = dist.compare(df_gi_cln, 'GI', df_gi_cln, 'GI')
dist.draw(sim_arr, 
          'expirements\\3_inter_intra_game_chapt_sim\\intra\\GI\\sim.png',
          x_lookup=gi_chapt_lookup,
          y_lookup=gi_chapt_lookup,
          xlable='原神',
          ylable='原神',
          x_ticks_rotation=45,
          x_ha='right')

plt.figure()
plt.boxplot(exp_var_ratio.values(), showmeans=True)
plt.xticks([1], ['原神'], fontproperties=font)
plt.savefig('expirements\\3_inter_intra_game_chapt_sim\\intra\\GI\\explained_variance.png')


# SR
# sim_arr, sim_std_arr, exp_var_ratio = dist.compare(df_sr_cln, 'SR', df_sr_cln, 'SR')
# dist.draw(sim_arr, 
#           'expirements\\3_inter_intra_game_chapt_sim\\intra\\SR\\sim.png',
#           x_lookup=sr_chapt_lookup,
#           y_lookup=sr_chapt_lookup,
#           xlable='崩坏：星穹铁道',
#           ylable='崩坏：星穹铁道')

# plt.figure()
# plt.boxplot(exp_var_ratio.values(), showmeans=True)
# plt.xticks([1], ['崩坏：星穹铁道'], fontproperties=font)
# plt.savefig('expirements\\3_inter_intra_game_chapt_sim\\intra\\SR\\explained_variance.png')
