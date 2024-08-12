import regex

from copy import deepcopy

SEG_SIZE = 1000

# https://zhuanlan.zhihu.com/p/106946176
def count_char(text):
    punctuation = r'\s\t\/!:\._\?,：()《》（）……~“”*""；，。！？、&=>\<」「…\n•'
    text = regex.sub(rf'[{punctuation}]+', '', text)
    return len(text)

def sub_string(text:str):
    matched = regex.finditer(r'[。！？\n…+]+', text)
    
    split_string = []
    prev_split_pos = 0
    if matched:
        for delimiter_pos in matched:
            split_pos = delimiter_pos.span()[-1]
            
            # Check if a left '）' or '」' follows the split position, if true, shift the position right by 1.
            if split_pos + 1 <= len(text) and text[split_pos] in ['）', '」']:
                split_pos += 1

            split_string.append(deepcopy(text)[prev_split_pos:split_pos].strip())
            prev_split_pos = split_pos
    else:
        return []

    return [i for i in split_string if i != '']

def slice_file(content, size:int=1000):
    sub_string_list = sub_string(content)

    temp = []
    res = []
    counter = 0
    for curr_string in sub_string_list:
        counter += count_char(curr_string)

        if counter < size:
            temp.append(curr_string)
        elif counter >= size:
            res.append('\n'.join(temp))

            counter = 0
            temp.clear()

    return res
