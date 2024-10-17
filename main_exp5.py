import config
import get_network

from glob import glob
from os.path import join


config = config.CongfiExpirementFive

#### Build Network ######################################################################################


# files_list = glob(join(config.GI_LINES_SAVE_PATH, '*'))
# n_files = len(files_list)

# mtl = get_network.SDP()

# for idx, file in enumerate(files_list, 1):
#     filename = file.split('\\')[-1]

#     print(f'Processing {filename} ({idx}\{n_files})...')

#     with open(file, 'r', encoding='utf-8') as f:
#         text = f.read()
#     mtl.run_and_save(text, join(config.GI_NETWORK_SAVE_FOLDER_PATH, f'{filename}.json'))


# files_list = glob(join(config.SR_LINES_SAVE_PATH, '*'))
# n_files = len(files_list)

# for idx, file in enumerate(files_list, 1):
#     filename = file.split('\\')[-1]

#     print(f'Processing {filename} ({idx}\{n_files})...')

#     with open(file, 'r', encoding='utf-8') as f:
#         text = f.read()
#     mtl.run_and_save(text, join(config.SR_NETWORK_SAVE_FOLDER_PATH, f'{filename}.json'))


#### Build Network ######################################################################################



