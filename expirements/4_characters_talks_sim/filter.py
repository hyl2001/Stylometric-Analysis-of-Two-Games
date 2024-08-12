# This experiment is under the guidance of [1] to take the quantitative language features 
# as a passage which indicates personal idiosyncrasies of different characters in game.
# 
# Reference:
# [1]俞东明.戏剧文体与戏剧文体学[J].浙江大学学报(社会科学版),1996(01):100-103.

import pandas as pd

from collections import Counter

MIN_N_OCCURANCE = 4

df = pd.read_excel('data_for_exp_4\\concat.xlsx')
df = df.drop('Unnamed: 0', axis='columns')

df['name'] = [name.split('_')[0] for name in df['file_name']]
chars_interested = [name for name, occurance in Counter(df['name']).items() 
                    if occurance >= MIN_N_OCCURANCE and name != '？？？']

df_selected = [pd.DataFrame(row) for row in df.itertuples()
               if row.name in chars_interested]
df_selected = pd.concat(df_selected, axis='columns').T
df_selected = df_selected.drop(columns=[0])
df_selected.columns = df.columns

df_selected[df_selected['game'] == 0]\
    .drop(columns=['game', 'name'])\
    .to_excel('expirements\\4_characters_talks_sim\\SR_selected.xlsx')
df_selected[df_selected['game'] == 1]\
    .drop(columns=['game', 'name'])\
    .to_excel('expirements\\4_characters_talks_sim\\GI_selected.xlsx')


chars_interested = [name for name, occurance in Counter(df['name']).items() 
                    if occurance >= MIN_N_OCCURANCE and name != '？？？' 
                    and name not in ['旅行者', '派蒙', '开拓者', '三月七']]

df_selected = [pd.DataFrame(row) for row in df.itertuples()
               if row.name in chars_interested]
df_selected = pd.concat(df_selected, axis='columns').T
df_selected = df_selected.drop(columns=[0])
df_selected.columns = df.columns

df_selected[df_selected['game'] == 0]\
    .drop(columns=['game', 'name'])\
    .to_excel('expirements\\4_characters_talks_sim\\SR_selected_filtered.xlsx')
df_selected[df_selected['game'] == 1]\
    .drop(columns=['game', 'name'])\
    .to_excel('expirements\\4_characters_talks_sim\\GI_selected_filtered.xlsx')
