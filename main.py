import pickle
import argparse
import random
import string
from collections import defaultdict
from sys import stdout, stderr


class MakeTextGreatAgain:
    TOP_SIGNS = ('(', '[', '{', '“', '"', '«', '‘', '')
    END_SIGNS = (')', ']', '}', '”', '"', '»', '’', '')
    SIGNS = ('.', '?', '!')

    def __init__(self, number_of_words):
        self.has_quote = False
        self.counter = 0
        self.num_of_words = number_of_words
        self.is_start_sentence = True
        self.what_quote = 0
        self.last_dot = False
        self.last_comma = False
        self.stack = []

    def remove_bad_signs(self, word):
        # word = word.replace("--", "–")
        word = word.replace("_", "")
        return word

    def fflush(self, new_word, symbol=''):
        symbol_index_in_end = MakeTextGreatAgain.END_SIGNS.index(symbol)
        symbol_top_sign = MakeTextGreatAgain.TOP_SIGNS[symbol_index_in_end]
        if symbol == '' or symbol_top_sign in self.stack:
            while len(self.stack) > 0 and symbol_top_sign != self.stack[-1]:
                current_top_sign = self.stack[-1]
                current_index_in_top = MakeTextGreatAgain.TOP_SIGNS.index(current_top_sign)
                current_end_sign = MakeTextGreatAgain.END_SIGNS[current_index_in_top]
                new_word += current_end_sign
                self.stack.pop(-1)
            else:
                if len(self.stack) > 0:
                    self.stack.pop(-1)
                    new_word += symbol
        return new_word

    def end_on_bad(self, word):
        bad = ["’s", "’t", "’ve", "’re", "’m"]
        is_it_honest = False
        for item in bad:
            if word.endswith(item):
                is_it_honest = True
        return is_it_honest

    def change_stack(self, word):
        new_word = ''
        for letter in word:
            if letter in MakeTextGreatAgain.TOP_SIGNS and \
                    not (letter == '"' and letter in self.stack):
                self.stack.append(letter)
                new_word += letter
            elif letter in MakeTextGreatAgain.SIGNS:
                if '...' not in word:
                    new_word += letter
                    new_word = self.fflush(new_word)
                self.is_start_sentence = True
            elif letter in MakeTextGreatAgain.END_SIGNS and \
                    not (letter == '’' and self.end_on_bad(word)):
                    new_word = self.fflush(new_word, letter)
            else:
                new_word += letter
        return new_word

    def make_capital(self, word):
        k = 0
        while k < len(word) - 1 and word[k] not in string.ascii_letters:
            k += 1
        else:
            word = word[:k] + word[k].capitalize() + word[k + 1:]
        return word

    def remove_double_dots_and_commas(self, word):
        new_word = ''
        for i in range(len(word)):
            need_to_add = True
            if word[i] != ',':
                self.last_comma = False
            else:
                if self.last_comma or self.last_dot:
                    need_to_add = False
                else:
                    self.last_comma = True

            if word[i] != '.':
                self.last_dot = False
            elif '...' not in word:
                if self.last_dot or self.last_comma:
                    need_to_add = False
                else:
                    self.last_dot = True

            if need_to_add:
                new_word += word[i]

        return new_word


    def __call__(self, word):
        self.counter += 1

        if self.is_start_sentence:
            word = self.make_capital(word)
            self.is_start_sentence = False

        word = self.remove_bad_signs(word)

        if self.counter == self.num_of_words:
            has_sign = False
            for sign in self.SIGNS:
                if sign in word:
                    has_sign = True
            if not has_sign:
                k = -1
                while k > -len(word) and word[k] not in string.ascii_letters:
                    k -= 1
                else:
                    if k != -1:
                        word = word[:k + 1] + '.'
                    else:
                        word += '.'

        word = self.change_stack(word)
        word = self.remove_double_dots_and_commas(word)
        return word


def return_zero():
    return 0


def return_emptiness():
    return defaultdict(return_zero)


def get_material(filename, encoding = None):
    words = []
    if encoding:
        with open(filename, 'r', encoding=encoding) as book:
            for line in book:
                words += line.split()
    else:
        with open(args.input_file, 'r') as book:
            for line in book:
                words += line.split()
    return words

parser = argparse.ArgumentParser()
# positional
parser.add_argument('mode', type=str, help='calculate or generate',
                    choices=['calculate', 'generate'])
# optional required=True
parser.add_argument('-i', '--input_file',
                    help='file to calculate from', default='LondonJack.WhiteFang.txt')
parser.add_argument('-p', '--probabilities_file',
                    help='file to write to', default='probabilities.txt')
parser.add_argument('-d', '--depth', type=int,
                    help='depth of calculation', default=3)
parser.add_argument('-c', '--count', type=int,
                    help='number of words to generate', default=30)
parser.add_argument('-o', '--output_file',
                    help='file to generate to')
args = parser.parse_args()

if args.mode == "calculate":

    try:
        words = get_material(args.input_file, 'utf-8')
    except Exception:
        words = get_material(args.input_file)

    probabilities = [args.depth]

    for level in range(args.depth):
        result = defaultdict(return_emptiness)
        for i in range(level, len(words)):
            if words[i] not in string.punctuation:
                result[tuple(words[i - level: i])][words[i]] += 1
        for substring in result.keys():
            amount = sum(result[substring].values())
            for new_word in result[substring].keys():
                result[substring][new_word] /= amount
        probabilities.append(result)

    with open(args.probabilities_file, "wb") as write_file:
        pickle.dump(probabilities, write_file)

elif args.mode == 'generate':

    def choose_and_add_word(big_dict):
        sum_of_prob = float()
        for word, value in data[len(previous_tokens) + 1][tuple(previous_tokens)].items():
            sum_of_prob += value
            if sum_of_prob > rand:
                previous_tokens.append(word)
                word = editor(word)
                result.append(word)
                break


    with open(args.probabilities_file, "rb") as read_file:
        data = pickle.load(read_file)
    assert data[0] >= args.depth, f'You only have {data[0]} depth'

    previous_tokens = []
    result = []
    editor = MakeTextGreatAgain(args.count)
    for _ in range(args.count):
        rand = random.random()
        while len(previous_tokens) > 0 and \
                not (tuple(previous_tokens) in data[len(previous_tokens) + 1]) \
                or (len(previous_tokens) >= args.depth - 1):
            previous_tokens = previous_tokens[1:]
        choose_and_add_word(data)

    if not args.output_file:
        print(' '.join(word for word in result if word))
    else:
        with open(args.output_file, 'w') as output:
            print(' '.join(word for word in result if word), file=output)

