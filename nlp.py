import hanlp, glob
import hanlp.pretrained
import hanlp.utils

from os.path import join
from copy import deepcopy
from json import loads, dump

def split_sent(txt_with_pos:list[str]):
    stop_marks = ['。', '！', '？', '……', '…']
    sent_split = []
    temp = []
    
    for char in txt_with_pos:
        char_, pos = char.strip().split('_')
        
        if pos == 'PU' and char_ in stop_marks:
            sent_split.append(deepcopy(temp))
            temp.clear()
        elif pos == 'PU' and char_ not in stop_marks:
            continue
        else:
            temp.append(char_)
    
    return sent_split

def process(path:str, pos_res_save_path:str, dep_res_save_path:str):
    tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
    dep = hanlp.load(hanlp.pretrained.dep.PMT1_DEP_ELECTRA_SMALL)
    pos = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)

    # https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/zh/tok_stl.ipynb
    tok_fine = hanlp.pipeline() \
        .append(hanlp.utils.rules.split_sentence) \
        .append(tok)
    tok_fine.append(lambda sents: sum(sents, []))

    for file in glob.glob(join(path, '*')):
        file_name = file.split('\\')[-1]
        print(f'[process()] Parsing: {file_name}')
        
        with open(file, 'r', encoding='utf-8') as op:
            print(f'  [process()] Running: tokenization...')
            toked = tok_fine(op.read())
            print(f'  [process()] Running: POS Tagging...')
            posed = pos(toked)
        
        txt_fmted = [f'{t}_{p}' + '\n' for t, p in zip(toked, posed)]

        dep_res = []
        print(f'  [process()] Running: Dependency Parse...')
        for s in split_sent(txt_fmted):
            if len(s) == 0 or len(s) == 1:
                pass
            else:
                dep_res.append(dep(s))
        
        print(f'  [Parser]: Saving...')
        with open(join(pos_res_save_path, file_name), 'w', encoding='utf-8') as f:
            f.writelines(txt_fmted)
        with open(join(dep_res_save_path, file_name+'.json'), 'w', encoding='utf-8') as f:
            dump(dep_res, f, ensure_ascii=False, indent=2)
