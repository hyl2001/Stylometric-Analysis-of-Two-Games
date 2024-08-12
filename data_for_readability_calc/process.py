from glob import glob
from os import replace, makedirs
from os.path import exists, join

paths = [
    'data_for_readability_calc\\gi_seg',
    'data_for_readability_calc\\sr_seg'
]

for path in paths:
    root = path.split('\\')[-1]
    for file in glob(join(path, '*')):
        filename = file.split('\\')[-1]

        dst_dir = f'data_for_readability_calc\\{root}_txt'
        if not exists(dst_dir):
            makedirs(dst_dir)

        replace(file, join(dst_dir, f'{filename}.txt'))
