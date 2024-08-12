from glob import glob
from os import makedirs
from os.path import exists, join


paths = [
    'data_for_exp_4\\gi_indiv_lines_seg',
    'data_for_exp_4\\sr_indiv_lines_seg'
]

for path in paths:
    root = path.split('\\')[-1]
    for file in glob(join(path, '*')):
        filename = file.split('\\')[-1]

        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        dst_dir = f'data_for_exp_4\\data_for_readability_calc\\{root}_txt'
        if not exists(dst_dir):
            makedirs(dst_dir)

        with open(join(dst_dir, f'{filename}.txt'), 'w', encoding='utf-8') as f:
            f.write(content)
