'''
This file saves the overall setting to the whole expirement.
Change in this file will affect the behavious of the program.
'''

class __BaseConfig:
    '''
    This class contains basic configurations shared by all expirements.
    '''
    SR_LINES_BWIKI_CODE_SAVE_PATH = 'data\\sr_bwiki_code'
    GI_LINES_BWIKI_CODE_SAVE_PATH = 'data\\gi_bwiki_code'

    EACH_FILE_SEG_LEN = 200 # This will effect the calculation of MSTTR (STTR).
    MINIMAL_FILE_LEN = 2 * EACH_FILE_SEG_LEN


class ConfigExpirementOneToThree(__BaseConfig):
    SR_LINES_SAVE_PATH = 'data\\sr'
    GI_LINES_SAVE_PATH = 'data\\gi'

    SR_LINES_FREG_FILE_SAVE_PATH = 'data\\sr_seg'
    GI_LINES_FREG_FILE_SAVE_PATH = 'data\\gi_seg'

    SR_NLP_RES_SAVE_PATH = 'data\\sr_nlp'
    GI_NLP_RES_SAVE_PATH = 'data\\gi_nlp'

    SR_DEP_RES_SAVE_PATH = 'data\\sr_dep'
    GI_DEP_RES_SAVE_PATH = 'data\\gi_dep'

    SR_FILES_INCLUDED_JSON_SAVE_PATH = 'data\\sr.json'
    GI_FILES_INCLUDED_JSON_SAVE_PATH = 'data\\gi.json'


class ConfigExpirementFour(__BaseConfig):
    SR_CHAR_LINES_SVAE_PATH = 'data_for_exp_4\\sr'
    GI_CHAR_LINES_SVAE_PATH = 'data_for_exp_4\\gi'

    SR_CHAR_LINES_FREG_FILE_SAVE_PATH = 'data_for_exp_4\\sr_indiv_lines_seg'
    GI_CHAR_LINES_FREG_FILE_SAVE_PATH = 'data_for_exp_4\\gi_indiv_lines_seg'

    SR_CHAR_LINES_NLP_RES_SAVE_PATH = 'data_for_exp_4\\sr_indiv_lines_nlp'
    GI_CHAR_LINES_NLP_RES_SAVE_PATH = 'data_for_exp_4\\gi_indiv_lines_nlp'

    SR_CHAR_LINES_DEP_RES_SAVE_PATH = 'data_for_exp_4\\sr_indiv_lines_dep'
    GI_CHAR_LINES_DEP_RES_SAVE_PATH = 'data_for_exp_4\\gi_indiv_lines_dep'

    SR_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH = 'data_for_exp_4\\sr.json'
    GI_CHAR_LINES_FILES_INCLUDED_JSON_SAVE_PATH = 'data_for_exp_4\\gi.json'
