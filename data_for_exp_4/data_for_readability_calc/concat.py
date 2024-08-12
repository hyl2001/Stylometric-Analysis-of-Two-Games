import pandas as pd


df_gi = pd.read_csv('data_for_exp_4\\data_for_readability_calc\\gi.csv')
df_sr = pd.read_csv('data_for_exp_4\\data_for_readability_calc\\sr.csv')

df = pd.concat([df_sr, df_gi], axis='index')
df.to_excel('data_for_exp_4\\readability.xlsx')


# sorting = {}

# for row in df.itertuples():
#     row_dict = row._asdict()
#     if row_dict['game'] == 1:
#         continue
    
#     name = '.'.join([k for i in row_dict['file_id'].split('_')[0::2] for k in i.split('.')])
#     row_dict.pop('Index')
#     row_dict.pop('file_id')
#     row_dict.pop('game')

#     sorting[name] = row_dict


# name = [list(map(int, i.split('.'))) for i in sorting.keys()]
# name.sort()
# name_sorted = ['.'.join(list(map(str, i))) for i in name]


# fig = plt.figure(figsize=(20, 5))
# ax = fig.add_subplot(1, 1, 1)

# lexical_richnes = []
# for idx, name in enumerate(name_sorted):
#     para = sorting[name]
#     lexical_richnes.append(para['lexical_richness'])

# ax.plot(lexical_richnes)
# ax.margins(x=0, y=0.1)

# plt.xticks(range(0, len(name_sorted)), name_sorted, rotation=90)
# plt.show()
