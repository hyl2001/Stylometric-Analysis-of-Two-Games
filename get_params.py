import regex
import numpy as np
import pandas as pd

from os.path import join
from math import floor
from glob import glob
from collections import Counter
from json import load


class QuantifyStyle:
    def __init__(self, 
                 toked_files_path:str, 
                 freg_files_path:str,
                 dep_jsons_path:str,
                 files_included_json_path:str,
                 *,
                 sub_array_len:int=200) -> None:
        self.toked_files_path = toked_files_path
        self.freg_files_path = freg_files_path
        self.dep_jsons_path = dep_jsons_path
        self.sub_array_len = sub_array_len

        self.toked_txt = {}

        with open(files_included_json_path, 'r', encoding='utf-8') as f:
            self.files_included = load(f)
        
        for file in glob(join(self.toked_files_path, '*')):
            name = file.split('\\')[-1]

            if name not in self.files_included:
                continue
            
            with open(file, 'r', encoding='utf-8') as f:
                self.toked_txt[name] = [i.strip() for i in f.readlines()]
            
        self.stats = None

    def __calc_dependency_dist(self, tree):
        dist = [np.abs(word['head'] - word['id']) 
                for word in tree 
                if word['deprel'] != 'PUN' and word['deprel'] != 'HED']
        
        return dist
    
    # https://zhuanlan.zhihu.com/p/106946176
    def __text_characters(self, text):
        punctuation = r'\s\/!:\._\?,：()《》（）……~“”*""；，。！？、&=>\<」「…\n'
        text = regex.sub(r'[{}]+'.format(punctuation), '', text)
        return len(text)

    def __get_subarrays(self, arr, size=100):
        if len(arr) % size == 0:
            split_pos = [i*size for i in range(1, int(len(arr)/size)+1)]
        else:
            split_pos = [i*size for i in range(1, floor(len(arr)/size)+1)] + [len(arr)]

        subarrays = []
        start_pos = 0
        for end_pos in split_pos:
            subarrays.append(arr[start_pos:end_pos])

            # Note that, according to the defination to STTR, this is not allowed.
            # For STTR, the segment which contains tokens less than the require 
            # tokens number of a segment will be dicarded. But, in some case, last 
            # segment will store tonkens whose count is near the required number,
            # so I think that segnment should be remained. And I set a threshold to
            # try to make sure the last piece holds most meaning for calculating
            # STTR.
            if end_pos - start_pos > 0.9 * size:
                start_pos = end_pos
            
        return subarrays

    def __simpson_diversity_coef(self,
                               word_list, 
                               *, 
                               trials:int = 10_0000, 
                               scale:int=1):
        # 胡显耀. 语料库文体统计学方法与应用[M]. 北京: 外语教学与研究出版社, 2020.12. 71.
        if scale == 0:
            raise ValueError('scale must not be equal to 0.')

        word_list_cap = len(word_list)
        word_one_idx_list = np.random.randint(low=0, high=word_list_cap, size=trials)
        word_two_idx_list = np.random.randint(low=0, high=word_list_cap, size=trials)
        rand_words_pairs = zip(word_one_idx_list, word_two_idx_list)

        two_words_diff_counter = \
            len([True for w1_idx, w2_idx in rand_words_pairs if word_list[w1_idx] != word_list[w2_idx]])
            
        return (two_words_diff_counter / trials) * scale

    def __safe_div(self, x, y):
        if y == 0:
            return 0
        else:
            return x / y
        
    def __get_mdd(self):
        print('[QuantifyStyle]: Calculating MDD...')

        dd = {}
        
        for file in glob(join(self.dep_jsons_path, '*.json')):
            name = file.split('\\')[-1].split('.json')[0]

            if name not in self.files_included:
                continue
        
            with open(file, 'r', encoding='utf-8') as f:
                # Each json file is called a discourse.
                disourse = load(f)
        
            dd_per_sent = []
            for sent in disourse:
                dd_per_sent.extend(self.__calc_dependency_dist(sent))
            
            dd[name] = {
                'MDD_mean': np.mean(dd_per_sent),
                'MDD_std': np.std(dd_per_sent)
            }
        
        return pd.DataFrame(dd)
    
    def __get_sttr(self):
        print('[QuantifyStyle]: Calculating STTR...')

        sttr = {}

        for name, txt in self.toked_txt.items():
            txt_no_tag = \
                self.__get_subarrays(
                    [i.split('_')[0] for i in txt if i.split('_')[-1] != 'PU'], self.sub_array_len
                )
            n_toks = [len(i) for i in txt_no_tag]
            n_typs = [len(set(i)) for i in txt_no_tag]

            sttr[name] = np.mean(np.divide(n_typs, n_toks))

        return pd.DataFrame(sttr, index = [f'sttr({self.sub_array_len})'])

    def __get_word_diversity(self):
        word_diversity = {}

        for name, txt in self.toked_txt.items():
            txt_no_tag = [i.split('_')[0] for i in txt if i.split('_')[-1] != 'PU']

            word_diversity[name] = self.__simpson_diversity_coef(txt_no_tag)

        return pd.DataFrame(word_diversity, index = ['word_div'])

    def __get_words_len_info(self):
        print('[QuantifyStyle]: Getting words length info...')

        words_len_info = {}

        for name, txt in self.toked_txt.items():
            txt_no_tag = [i.split('_')[0] for i in txt if i.split('_')[-1] != 'PU']
            word_len = [len(i) for i in txt_no_tag]

            words_len_info[name] = {
                'avg_word_len': np.mean(word_len),
                'std_word_len': np.std(word_len)
            }

        return pd.DataFrame(words_len_info)

    def __get_pos_info(self):
        # 名词(NN, NR, NT)、动词(VC, VE, VV)、形容词(VA, JJ)、副词(AD)、连词(CC, CS)、代词(PN)、介词(MSP, LC, P)、助词(AS)
        # Pos tags used when counting prepsitions are selected with https://baike.baidu.com/item/介词/2643774
        print('[QuantifyStyle]: Counting words of different pos...')

        pos = {}
        for name, txt in self.toked_txt.items():
            tags = [i.split('_')[-1] for i in txt]
            pos_counted = Counter(tags)
            pos[name] = {
                'nouns': pos_counted['NN'] +  pos_counted['NR'] + pos_counted['NT'],
                'verbs': pos_counted['VC'] +  pos_counted['VE'] + pos_counted['VV'],
                'adjs': pos_counted['VA'] +  pos_counted['JJ'],
                'advs': pos_counted['AD'] +  pos_counted[''],
                'conjs': pos_counted['CC'] +  pos_counted['CS'],
                'prons': pos_counted['PN'],
                'preps': pos_counted['MSP'] +  pos_counted['LC'] + pos_counted['P'],
                'auxs': pos_counted['AS'],
            }

        return pd.DataFrame(pos)

    def __get_spec_chars(self):
        print('[QuantifyStyle]: Counting specific characters ...')
        # 是、有、连、之
        spec_chars = {}

        for name, txt in self.toked_txt.items():
            txt_no_tag = [i.split('_')[0] for i in txt if i.split('_')[-1] != 'PU']
            counted = Counter(txt_no_tag)
            spec_chars[name] = {
                'shi': counted['是'],
                'you': counted['有'],
                'lian': counted['连'],
                'zhi': counted['之'],
            }

        return pd.DataFrame(spec_chars)

    def __get_sent_len_info(self):
        print('[QuantifyStyle]: Calculating MSL and SL STD ...')
        # 平均句长、句长标准差
        sent_len_info = {}

        for file in glob(join(self.freg_files_path, '*')):
            name = file.split('\\')[-1]

            if name not in self.files_included:
                continue

            with open(file, 'r', encoding='utf-8') as f:
                txt = [i.strip() for i in f.readlines()]
            
            sent_len = [self.__text_characters(i) for i in txt]
            sent_len_info[name] = {
                'avg_sent_len': np.mean(sent_len),
                'std_sent_len': np.std(sent_len)
            }

        return pd.DataFrame(sent_len_info)

    def __get_clause_info(self):
        print('[QuantifyStyle]: Getting clauses info ...')
        # Formulars about sentence rhythmic degree and average clauses length can be found in [1].
        # [1]仲文明,王靖涵.少年儿童翻译文学的译本风格计量研究——以Silent Spring三译本为例[J].
        #    外语与翻译,2023,30(01):20-27+98.DOI:10.19502/j.cnki.2095-9648.2023.01.010.

        pause_marks = ['。', '！', '？', '……', '…', '；', '，', '：', '、']
        stop_marks = ['。', '！', '？', '……', '…']

        sent_info = {}
        for name, txt in self.toked_txt.items():
            tokens = len([i.split('_')[0] for i in txt if i.split('_')[-1] != 'PU'])
            puncts = Counter([i.split('_')[0] for i in txt if i.split('_')[-1] == 'PU'])

            pauses = np.sum([puncts[i] for i in pause_marks])
            stops = np.sum([puncts[i] for i in stop_marks])
            # Here we treat stops as the number of sentences.

            sent_info[name] = {
                'avg_clauses_len': self.__safe_div(tokens, pauses),
                'sent_rhy_deg': self.__safe_div(pauses, stops)
            }

        return pd.DataFrame(sent_info)

    def __get_interested_sent(self):
        print('[QuantifyStyle]: Counting the number of interested sentences...')
        # 陈述句、疑问句
        declarative_sentence_makrs = ['。', '……', '…']
        interrogative_sentence_marks = ['？']

        # The number of periods and ellipses are seen as the amount of declarative sentences and
        # question marks interrogative sentences.

        interested_sent_types = {}
        for name, txt in self.toked_txt.items():
            puncts = Counter([i.split('_')[0] for i in txt if i.split('_')[-1] == 'PU'])

            n_declarative_sentence = np.sum([puncts[i] for i in declarative_sentence_makrs])
            n_interrogative_sentence = np.sum([puncts[i] for i in interrogative_sentence_marks])

            interested_sent_types[name] = {
                'decl_sent': n_declarative_sentence,
                'interr_sent': n_interrogative_sentence
            }

        return pd.DataFrame(interested_sent_types)

    def __get_puncts(self):
        print('[QuantifyStyle]: Counting punctuations ...')

        comma_matchers = regex.compile(r'，')
        pause_mark_matchers = regex.compile(r'、')
        bracket_matchers = regex.compile(r'（')
        dash_matchers = regex.compile(r'—+') # Dashs may have one '—' or two.

        puncts_info = {}
        for file in glob(join(self.freg_files_path, '*')):
            name = file.split('\\')[-1]

            if name not in self.files_included:
                continue

            with open(file, 'r', encoding='utf-8') as f:
                txt = ''.join([i.strip() for i in f.readlines()])

            puncts_info[name] = {
                'commas': len(comma_matchers.findall(txt)),
                'pause_marks': len(pause_mark_matchers.findall(txt)),
                'brackets': len(bracket_matchers.findall(txt)),
                'dashes': len(dash_matchers.findall(txt)),
            }

        return pd.DataFrame(puncts_info)

    def __get_spec_sents(self):
        print('[QuantifyStyle]: Counting specific sentences...')

        # 把字句(BA)、被字句(LB, SB)
        spec_sents = {}

        for name, txt in self.toked_txt.items():
            tag = Counter([i.split('_')[-1] for i in txt])
            spec_sents[name] = {
                'ba': tag['BA'],
                'bei': tag['LB'] + tag['SB']
            }

        return pd.DataFrame(spec_sents)

    def __get_four_char_words(self):
        print('[QuantifyStyle]: Counting four-character words ...')

        # 四字词语
        four_char_words = {}

        for name, txt in self.toked_txt.items():
            char_len = Counter([len(i.split('_')[0]) for i in txt if i.split('_')[-1] != 'PU'])
            four_char_words[name] = {
                'four_char_words': char_len[4]
            }

        return pd.DataFrame(four_char_words)

    def __get_simile(self):
        print('[QuantifyStyle]: Counting similes ...')

        simile_chars = ['如', '若', '似', '好像', '像', '如同', '好比', '犹如', '仿佛', '宛如']

        simile = {}
        for name, txt in self.toked_txt.items():
            chars_counted = Counter([i.split('_')[0] for i in txt if i.split('_')[-1] != 'PU'])

            simile[name] = {
                'similes': np.sum([chars_counted[i] for i in simile_chars])
            }

        return pd.DataFrame(simile)

    def get_statistic(self):
        self.stats = pd.concat([
            self.__get_mdd(),
            self.__get_sttr(),
            self.__get_word_diversity(),
            self.__get_words_len_info(),
            self.__get_pos_info(),
            self.__get_spec_chars(),
            self.__get_sent_len_info(),
            self.__get_clause_info(),
            self.__get_interested_sent(),
            self.__get_puncts(),
            self.__get_spec_sents(),
            self.__get_four_char_words(),
            self.__get_simile(),
        ]).T
    
    def save_as_excel(self, name:str='quantified_style.xlsx'):
        self.stats.to_excel(name)
