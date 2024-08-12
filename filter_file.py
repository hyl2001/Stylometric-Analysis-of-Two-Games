import regex

import config

from json import dump
from glob import glob
from os.path import join

# https://zhuanlan.zhihu.com/p/106946176
def count_char(text):
    punctuation = r'\s\/!:\._\?,：()《》（）……~“”*""；，。！？、&=>\<」「…\n•'
    text = regex.sub(r'[{}]+'.format(punctuation), '', text)
    return len(text)

def filter_file(folder_path:str, save_path:str, min_file_len:int):
    files_included = []

    n_included = 0
    n_excluded = 0
    
    for file in glob(join(folder_path, '*')):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        n_chars = count_char(content)
        if n_chars >= min_file_len:
            files_included.append(file.split('\\')[-1])

            n_included += 1
        else:
            n_excluded += 1
    
    print(f'{n_included} file(s) included; {n_excluded} file(s) excluded.')
    
    with open(save_path, 'w', encoding='utf-8') as f:
        dump(files_included, f, ensure_ascii=False, indent=4)
