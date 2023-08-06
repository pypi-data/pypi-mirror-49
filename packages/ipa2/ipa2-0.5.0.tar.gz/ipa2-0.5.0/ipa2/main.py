import itertools
import json
import nlp2


def load_lang_to_list(lang):
    file_loc = 'data/' + lang + '.json'
    if nlp2.is_file_exist(file_loc):
        with open(file_loc, encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            return data[lang][0]
    else:
        assert FileNotFoundError


class IPAConverter:
    def __init__(self, lang='yue'):
        super().__init__()
        self.data = {}
        if isinstance(lang, str):
            self.data = load_lang_to_list(lang)
        elif isinstance(lang, list):
            for i in lang:
                self.data.update(load_lang_to_list(i))

    def convert_sent(self, input='測試的句子'):
        input = nlp2.spilt_sentence_to_array(input, True)
        result = []
        # maximum match
        senlen = len(input)
        start = 0
        while start < senlen:
            matched = False
            for i in range(senlen, 0, -1):
                string = "".join(input[start:start + i])
                if string in self.data:
                    result.append(string)
                    matched = True
                    break
            if not matched:
                i = 1
                result.append(input[start])
            start += i

        # get all combination
        ipa_result = []
        for i in result:
            if i in self.data:
                ipa_result.append(self.data[i].replace('/', '').split(", "))
        return [" ".join(x) for x in itertools.product(*ipa_result)]
