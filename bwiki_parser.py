import regex


class Parse:
    def __init__(self) -> None:
        self.__rich_text_func_str_matcher = regex.compile(r'\{{2,}.+?\}{2,}')
        self.__quotation_mark_matcher = regex.compile(r'：|:')
        self.__noise_remover = regex.compile(r'<(\s*?)[^>]*>.*?|<.*? />')
        self.__line_matcher = regex.compile(r'(?<=[选项|剧情]\d=).+|(?<=^\*).+|{{角色对话\|[左右]\|.+', regex.MULTILINE)
        self.__starter_matcher = regex.compile(r'[\u4e00-\u9fa5]+\=\=')
        self.__msg_trailing_chars_matcher = regex.compile(r'\|*是*}+')
        self.__msg_sender_name_matcher = regex.compile(r'(?<=角色对话\|[左右]\|).+?(?=\|)')

        self.__game = ''

    def __remove_brackets(self, string:str):
        return string.replace('}', '').replace('{', '')
    
    def __get_char_needed_in_tag(self, tag):
        tag_no_brackets = self.__remove_brackets(tag)
        tag_string_char_list = tag_no_brackets.split('|')
        
        if tag_no_brackets.find('注音') != -1:
            # 注音 functions as ruby; we just need characters at middle with index of 1.
            return tag_string_char_list[1]
        elif tag_no_brackets.find('颜色') != -1 or tag_no_brackets.find('文本') != -1:
            # Sentence at the end of 颜色 or 角色对话 function is what we need.
            # These two functions will be matched by regex when they are in a talk sentence.
            return tag_string_char_list[-1]
        elif tag_no_brackets.find('图标') != -1 or \
             tag_no_brackets.find('黑幕') != -1 or \
             tag_no_brackets.find('图片放大') != -1 or \
            tag_no_brackets.find('图片'):
            # Skip to replace it with returning an empty string.
            return ''
        else:
            raise ValueError(f'Uncatched tag ({tag}) found.')

    def __replace_tags(self, string:str):
        tag_match_res = \
            list(self.__rich_text_func_str_matcher.finditer(string))
        
        if tag_match_res:
            left, right = tag_match_res.pop().span()
            lstring, tag, rstring = string[:left], string[left:right], string[right:]

            tag_new = self.__get_char_needed_in_tag(tag)

            return self.__replace_tags(''.join([lstring, tag_new, rstring]))
        else:        
            return string

    def __remove_html_tags(self, string:str):
        return self.__noise_remover.sub('', string)
    
    def __truncate(self, text:str):
        '''
        Two situations should be considered:
        1. if a file contains the starter, then truncate this file from the starter;
        2. if a file does not contain the starter, deem the file has clipped already.
        
        `Starter` refers to the first `==`
        '''
        
        matched = list(self.__starter_matcher.finditer(text))
        if matched:
            # The matched[0] we just need the fisrt occurance of the string matched by given regex.
            text = text[matched[0].span()[1]:]
        
        return text
    
    def __handle_msg_text(self, string:str):
        if string.find('|文本|') == -1:
            # If '|文本|' not found, return the input string.
            # Because this is not a piece of massage.
            return string

        spkr_name = self.__msg_sender_name_matcher.findall(string)
        if spkr_name:
            spkr_name = spkr_name[0]
        else:
            raise ValueError('No speaker name found.')
        
        str_pieces = string.split('|文本|')
        talk_sent = str_pieces[-1]
        talk_sent_cleaned = self.__msg_trailing_chars_matcher.sub('', talk_sent)

        return '：'.join([spkr_name, talk_sent_cleaned])

    def parse(self, file_path):
        if file_path.find('sr') != -1:
            self.__game = 'SR'
        elif file_path.find('gi') != -1:
            self.__game = 'GI'
        else:
            raise ValueError('Game type cannot be recognized.')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = self.__truncate(content)
        out = [self.__replace_tags(self.__handle_msg_text(m)) 
               for m in self.__line_matcher.findall(content)]
        
        return out

    def clean_text(self, strings:list[str]):
        out = []

        for s in strings:
            if not len(s.strip()):
                continue

            matched = [i for i in self.__quotation_mark_matcher.finditer(s)]
            if matched:
                # matched[0] means that we just need the quotation mark behind speak's name.
                sent = s[matched[0].span()[1]:]
            else:
                sent = s
            
            sent = self.__remove_html_tags(sent)
            out.append(self.__remove_brackets(sent) + '\n')
        
        # # Remove redundant strings and keep order.
        # string_redundance_removed = []
        # for o in out:
        #     if o.strip() in string_redundance_removed:
        #         continue
        #     else:
        #         string_redundance_removed.append(self.__remove_html_tags(o))
        
        return out
    
    def __replace_char(self, string:str):
        string = self.__remove_html_tags(string)
        # Some string may contain HTML tags. 

        # Both "「" and "」" will incur error of ARC, so they must be replaced.
        string = string.replace('「', '').replace('」', '')
        string = string.replace('⌈', '').replace('⌋', '')

        if self.__game == 'GI':
            string = string.replace('*', '')\
                    .replace('荧/空', '旅行者')\
                    .replace('荧\空', '旅行者')\
                    .replace('荧', '旅行者')\
                    .replace('空', '旅行者')
        else:
            string = string.replace('*', '')

        return string.strip()

    def get_invidual_lines(self, strings:list[str]):
        '''
        Travler or Trailblazer will be tagged those sentences without 
        name at the beginning of sentences.
        '''
        char_lines_dict = {}

        for s in strings:
            if not len(s.strip()):
                continue

            matched = [i for i in self.__quotation_mark_matcher.finditer(s)]
            if matched:
                name = s[:matched[0].span()[0]]
                line = self.__remove_brackets(s[matched[0].span()[1]:])
            else:
                name = '旅行者' if self.__game == 'GI' else '开拓者'
                line = self.__remove_brackets(s)
            
            name = self.__replace_char(name)

            if name.find('短信') == -1:
                if name not in char_lines_dict:
                    char_lines_dict[name] = []
                
                char_lines_dict[name].append(line + '\n')
            else:
                print(s)
            
        return char_lines_dict
