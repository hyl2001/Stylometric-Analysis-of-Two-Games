import hanlp
import torch

from json import dump


class SDP:
    def __init__(self) -> None:
        print('Initializing model...')
        self.__mtl = hanlp.load('CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH')

        tasks = list(self.__mtl.tasks.keys())
        for task in tasks:
            if task not in ('tok/fine', 'sdp'):
                del self.__mtl[task]

    def run_and_save(self, text:str, save_path:str):
        sentences = list(hanlp.hanlp.utils.rules.split_sentence(text))

        blks = self.__mtl(sentences)

        with open(save_path, 'w', encoding='utf-8') as f:
            dump(blks, f, ensure_ascii=False, indent=2)
        
        torch.cuda.empty_cache()
