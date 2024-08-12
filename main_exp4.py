import bwiki_parser
import slicer
import config
import nlp
import get_params
import get_quita_indicators
import filter_file

import pandas as pd

from glob import glob
from os.path import join
from os import remove
from json import dump

'''
This program is for extracting and analizing character individual lines. 
It is dedicated to expirement 4. Due to the compliexity of expirement 4,
all generated files will be saved in an independent folder.
'''

config = config.ConfigExpirementFour
excel_name = 'data_for_exp_4\\quantified_style.xlsx' 


#### Parse BWIKI code ######################################################################################

# for file_path in [config.SR_CHAR_LINES_SVAE_PATH, config.GI_CHAR_LINES_SVAE_PATH]:
#     for file in [file for file in glob(join(file_path, '*'))]:
#         remove(file)

# parser = bwiki_parser.Parse()
# for file_path in [config.SR_LINES_BWIKI_CODE_SAVE_PATH, config.GI_LINES_BWIKI_CODE_SAVE_PATH]:
#     files_list = [file for file in glob(join(file_path, '*.txt'))]
#     game_spkr_name_lst = []

#     for file in files_list:
#         file_name = file.split('\\')[-1].split('.txt')[0]
#         print(file_name)

#         save_path = \
#             config.SR_CHAR_LINES_SVAE_PATH if file_path.find('sr') != -1 \
#                 else config.GI_CHAR_LINES_SVAE_PATH
        
#         indiv_lines_dict = parser.get_invidual_lines([i for i in parser.parse(file)])
        
#         for name in indiv_lines_dict.keys():
#             indiv_lines = indiv_lines_dict[name]

#             if not name:
#                 name = 'NA'

#             if name not in game_spkr_name_lst:
#                 game_spkr_name_lst.append(name)

#                 with open(join(save_path, f'{name}'), 'w', encoding='utf-8') as f:
#                     f.writelines(indiv_lines)
#             else:
#                 with open(join(save_path, f'{name}'), 'a', encoding='utf-8') as f:
#                     f.writelines(indiv_lines)

#### Parse BWIKI code ######################################################################################
                    
#### Slice files ###########################################################################################

# for file_path in [config.SR_CHAR_LINES_SVAE_PATH, config.GI_CHAR_LINES_SVAE_PATH]:
#     for file in glob(join(file_path, '*')):
#         name = file.split('\\')[-1]
#         print(f'[Slicer]: {name}')

#         with open(file, 'r', encoding='utf-8') as f:
#             content = [sub for i in f.readlines() for sub in slicer.sub_string(i)]
        
#         save_path = \
#             config.SR_CHAR_LINES_FREG_FILE_SAVE_PATH if file_path.find('sr') != -1 \
#                 else config.GI_CHAR_LINES_FREG_FILE_SAVE_PATH
        
#         for idx, c in enumerate(slicer.slice_file(''.join(content), slicer.SEG_SIZE)):
#             with open(f'{save_path}\\{name}_{idx}', 'w', encoding='utf-8') as f:
#                 f.writelines([i for i in c])

#### Slice files ###########################################################################################

#### Running NLP ###########################################################################################

# for file_path in [config.SR_CHAR_LINES_FREG_FILE_SAVE_PATH, config.GI_CHAR_LINES_FREG_FILE_SAVE_PATH]:
#     if file_path.find('sr') != -1:
#         nlp_save_path = config.SR_CHAR_LINES_NLP_RES_SAVE_PATH
#         dep_save_path = config.SR_CHAR_LINES_DEP_RES_SAVE_PATH
#     else:
#         nlp_save_path = config.GI_CHAR_LINES_NLP_RES_SAVE_PATH
#         dep_save_path = config.GI_CHAR_LINES_DEP_RES_SAVE_PATH

#     nlp.process(file_path, nlp_save_path, dep_save_path)

#### Running NLP ###########################################################################################

#### Filtering files #######################################################################################

# filter_file.filter_file(config.GI_CHAR_LINES_FREG_FILE_SAVE_PATH,
#                         config.GI_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH,
#                         config.MINIMAL_FILE_LEN)
# filter_file.filter_file(config.SR_CHAR_LINES_FREG_FILE_SAVE_PATH,
#                         config.SR_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH,
#                         config.MINIMAL_FILE_LEN)

#### Filtering files #######################################################################################

#### Running QUITA #########################################################################################

# quita = get_quita_indicators.GetIndecators()

# df_sr_quita = quita.run_on_folder(config.SR_CHAR_LINES_NLP_RES_SAVE_PATH,
#                                   config.SR_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH)
# df_gi_quita = quita.run_on_folder(config.GI_CHAR_LINES_NLP_RES_SAVE_PATH,
#                                   config.GI_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH)
# df_quita = pd.concat([df_sr_quita, df_gi_quita])
# df_quita.to_excel('data_for_exp_4\\QUITA.xlsx')

#### Running QUITA #########################################################################################

#### Calculating quantified style ##########################################################################

# sr_quantifier = get_params.QuantifyStyle(
#     toked_files_path=config.SR_CHAR_LINES_NLP_RES_SAVE_PATH,
#     freg_files_path=config.SR_CHAR_LINES_FREG_FILE_SAVE_PATH,
#     dep_jsons_path=config.SR_CHAR_LINES_DEP_RES_SAVE_PATH,
#     files_included_json_path=config.SR_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH,
#     sub_array_len=config.EACH_FILE_SEG_LEN
# )
# gi_quantifier = get_params.QuantifyStyle(
#     toked_files_path=config.GI_CHAR_LINES_NLP_RES_SAVE_PATH,
#     freg_files_path=config.GI_CHAR_LINES_FREG_FILE_SAVE_PATH,
#     dep_jsons_path=config.GI_CHAR_LINES_DEP_RES_SAVE_PATH,
#     files_included_json_path=config.GI_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH,
#     sub_array_len=config.EACH_FILE_SEG_LEN
# )

# sr_quantifier.get_statistic()
# gi_quantifier.get_statistic()

# sr_quantified_style = sr_quantifier.stats
# gi_quantified_style = gi_quantifier.stats

# sr_marker = [0 for _ in range(sr_quantified_style.shape[0])]
# gi_marker = [1 for _ in range(gi_quantified_style.shape[0])]

# sr_quantified_style['game'] = sr_marker
# gi_quantified_style['game'] = gi_marker

# pd.concat([sr_quantified_style, gi_quantified_style], axis='index')\
#     .to_excel(excel_name)

#### Calculating quantified style ##########################################################################

#### Concatenate files #####################################################################################

df = pd.read_excel(excel_name)
file_name = df['Unnamed: 0']

df_readablity_concat = pd.read_excel('data_for_exp_4\\readability.xlsx')\
                         .drop('Unnamed: 0', axis='columns')\
                         .rename({'file_id': 'Unnamed: 0'}, axis='columns')
df_quita = pd.read_excel('data_for_exp_4\\QUITA.xlsx')

m1 = pd.merge(df, df_readablity_concat, on='Unnamed: 0')
m2 = pd.merge(m1, df_quita, on='Unnamed: 0')\
  .rename({'Unnamed: 0': 'file_name'}, axis='columns')\
  .to_excel('data_for_exp_4\\concat.xlsx')

#### Concatenate files #####################################################################################
