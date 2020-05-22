import string


def make_dict_of_signs():
    # CHECKED
    result = dict()
    for i in range(len(TextImprover.OPEN_SIGNS)):
        result[TextImprover.OPEN_SIGNS[i]] = TextImprover.CLOSE_SIGNS[i]
        result[TextImprover.CLOSE_SIGNS[i]] = TextImprover.OPEN_SIGNS[i]
    return result


def remove_bad_signs(word):
    # CHECKED
    word = word.replace('—', '-')
    word = word.replace("_", "")
    return word


def make_capital(word):
    # CHECKED
    index = 0
    for index, letter in enumerate(word):
        if letter in string.ascii_letters:
            break
    word = word[:index] + word[index].capitalize() + word[index + 1:]
    return word


def end_on_bad(word):
    # CHECKED
    bad = ["’s", "’t", "’ve", "’re", "’m", "’d"]
    is_word_bad = False
    for item in bad:
        if word.endswith(item):
            is_word_bad = True
    return is_word_bad


def add_one_more_point(word):
    # CHECKED
    k = -1
    while k > -len(word) and word[k] not in string.ascii_letters:
        k -= 1
    else:
        if k != -1:
            word = word[:k + 1] + '.'
        else:
            word += '.'
    return word


class TextImprover:
    OPEN_SIGNS = ('(', '[', '{', '“', '"', '«', '‘', '')
    CLOSE_SIGNS = (')', ']', '}', '”', '"', '»', '’', '')
    PUNCTUATION_SIGNS = ('.', '?', '!')

    def __init__(self, number_of_words):
        # CHECKED
        self.has_quote = False
        self.counter = 0
        self.num_of_words = number_of_words
        self.is_start_sentence = True
        self.what_quote = 0
        self.last_dot = False
        self.last_comma = False
        self.stack_of_signs = []
        self.pairs_of_signs = make_dict_of_signs()

    def fflush(self, new_word, symbol=''):
        # CHECKED
        opposite_symbol = self.pairs_of_signs[symbol]
        if symbol == '' or opposite_symbol in self.stack_of_signs:
            while self.stack_of_signs and opposite_symbol != self.stack_of_signs[-1]:
                new_word += self.pairs_of_signs[self.stack_of_signs[-1]]
                self.stack_of_signs.pop(-1)
            else:
                if symbol != '' and self.stack_of_signs:
                    self.stack_of_signs.pop(-1)
                    new_word += symbol
        return new_word

    def change_stack(self, word):
        # ПРОЧУВСТВОВАлВСюБОЛь
        new_word = ''
        for letter in word:
            if letter in TextImprover.OPEN_SIGNS and not (letter == '"' and letter in self.stack_of_signs):
                self.stack_of_signs.append(letter)
                new_word += letter
            elif letter in TextImprover.PUNCTUATION_SIGNS:
                new_word += letter
                if '...' not in word and 'www' not in word:
                    new_word = self.fflush(new_word)
                self.is_start_sentence = True
            elif letter in TextImprover.CLOSE_SIGNS and \
                    not (letter == '’' and end_on_bad(word)):
                new_word = self.fflush(new_word, letter)
            else:
                new_word += letter
        return new_word

    def remove_double_dots_and_commas(self, word):
        # CHECKED
        new_word = ''
        for i in range(len(word)):
            need_to_add = True
            if word[i] == ',':
                if self.last_comma or self.last_dot:
                    need_to_add = False
                else:
                    self.last_comma = True
                    self.last_dot = False
            else:
                self.last_comma = False

            if word[i] == '.' and '...' not in word:
                if self.last_dot or self.last_comma:
                    need_to_add = False
                else:
                    self.last_dot = True
            else:
                self.last_dot = False

            if need_to_add:
                new_word += word[i]

        return new_word

    def __call__(self, word):
        assert type(word) == str, 'Something went wrong'
        self.counter += 1

        if self.is_start_sentence:
            interesting_words = ('screamed', 'said', 'cried')
            if word not in interesting_words:
                word = make_capital(word)
            self.is_start_sentence = False

        word = remove_bad_signs(word)

        if self.counter == self.num_of_words:
            word = add_one_more_point(word)

        word = self.change_stack(word)
        word = self.remove_double_dots_and_commas(word)
        return word
