import pickle
import argparse
import random
import string
from collections import defaultdict
from sys import stdout, stderr


class MakeTextGreatAgain:
    BEGIN_QUOTES = ('“', '"', '«', '‘')
    END_QUOTES = ('”', '"', '»', '’')
    SIGNS = ('.', '?', '!')

    def __init__(self, number_of_words):
        self.has_quote = False
        self.counter = 0
        self.num_of_words = number_of_words
        self.is_start_sentence = True
        self.what_quote = 0
        self.last_dot = False
        self.last_comma = False

    def remove_brackets(self, word):
        word = word.replace("--", "–")
        brackets = ("(", ")", "[", "]", "{", "}", "_")
        for bracket in brackets:
            word = word.replace(bracket, "")
        return word

    def change_quotes(self, word):
        if word[0] in MakeTextGreatAgain.BEGIN_QUOTES:
            if self.has_quote:
                word = word[1:]
            else:
                self.what_quote = MakeTextGreatAgain.BEGIN_QUOTES.index(word[0])
            self.has_quote = True
        elif len(word) > 1 and (word[1] in MakeTextGreatAgain.BEGIN_QUOTES):
            if self.has_quote:
                word = word[2:]
            else:
                self.what_quote = MakeTextGreatAgain.BEGIN_QUOTES.index(word[1])
            self.has_quote = True

        if word[-1] in MakeTextGreatAgain.END_QUOTES:
            if not self.has_quote:
                word = word[:-1]
            if self.counter != self.num_of_words:
                self.has_quote = False
        elif len(word) > 1 and word[-2] in MakeTextGreatAgain.END_QUOTES:
            if not word.endswith("’s") and not word.endswith("’t"):
                if not self.has_quote:
                    word = word[:-2] + word[-1]
                if self.counter != self.num_of_words:
                    self.has_quote = False

        return word

    def __call__(self, word):
        self.counter += 1
        word = self.remove_brackets(word)

        if word in string.punctuation:
            if self.counter == self.num_of_words:
                if not self.last_dot and not self.last_comma:
                    return '.'
            return None

        word = self.change_quotes(word)

        if self.is_start_sentence:
            k = 0
            while k < len(word) - 1 and word[k] not in string.ascii_letters:
                k += 1
            else:
                word = word[:k] + word[k].capitalize() + word[k + 1:]
            self.is_start_sentence = False
        if word[-1] in MakeTextGreatAgain.SIGNS or \
                (len(word) > 1 and word[-2] in MakeTextGreatAgain.SIGNS):
            if self.has_quote and word[-1] not in MakeTextGreatAgain.END_QUOTES:
                word += MakeTextGreatAgain.END_QUOTES[self.what_quote]
                if self.counter != self.num_of_words:
                    self.has_quote = False
            self.is_start_sentence = True

        if self.counter == self.num_of_words:
            k = -1
            while k > -len(word) and word[k] not in string.ascii_letters:
                k -= 1
            else:
                if k != -1:
                    word = word[:k + 1]
            word += '.'
            if self.has_quote:
                word += MakeTextGreatAgain.END_QUOTES[self.what_quote]

        for l in range(len(word)):
            if word[l] != ',':
                self.last_comma = False
            else:
                if self.last_comma:
                    word = word[:l] + word[l+1:]
                else:
                    self.last_comma = True

            if word[l] != '.':
                self.last_dot = False
            else:
                if self.last_dot:
                    word = word[:l] + word[l+1:]
                else:
                    self.last_dot = True
        
        return word


def return_zero():
    return 0


def return_emptiness():
    return defaultdict(return_zero)


parser = argparse.ArgumentParser()
# positional
parser.add_argument('mode', type=str, help='calculate or generate',
                    choices=['calculate', 'generate'])
# optional required=True
parser.add_argument('-i', '--input_file', type=str,
                    help='file to calculate from', default='LondonJack.WhiteFang.txt')
parser.add_argument('-p', '--probabilities_file', type=str,
                    help='file to write to', default='probabilities.txt')
parser.add_argument('-d', '--depth', type=int,
                    help='depth of calculation', default=3)
parser.add_argument('-c', '--count', type=int,
                    help='number of words to generate', default=30)
parser.add_argument('-o', '--output_file', type=str,
                    help='file to generate to')
args = parser.parse_args()

if args.mode == "calculate":
    words = []
    try:
        with open(args.input_file, 'r', encoding='utf-8') as book:
            for line in book:
                words += line.split()
    except Exception:
        with open(args.input_file, 'r') as book:
            for line in book:
                words += line.split()

    probabilities = [args.depth]

    for level in range(args.depth):
        result = defaultdict(return_emptiness)
        for i in range(level, len(words)):
            result[tuple(words[i - level: i])][words[i]] += 1
        for substring in result.keys():
            amount = sum(result[substring].values())
            for new_word in result[substring].keys():
                result[substring][new_word] /= amount
        probabilities.append(result)

    with open(args.probabilities_file, "wb") as write_file:
        pickle.dump(probabilities, write_file)

elif args.mode == 'generate':
    with open(args.probabilities_file, "rb") as read_file:
        data = pickle.load(read_file)
    assert data[0] >= args.depth, f'You only have {data[0]} depth'

    previous_tokens = []
    result = []
    choose_your_word = MakeTextGreatAgain(args.count)
    for _ in range(args.count):
        rand = random.random()
        sum_of_prob = float()

        while len(previous_tokens) > 0 and not (tuple(previous_tokens) in
                                                data[len(previous_tokens) + 1]):
            previous_tokens = previous_tokens[1:]

        for word, value in data[len(previous_tokens) + 1][tuple(previous_tokens)].items():
            sum_of_prob += value
            if sum_of_prob > rand:
                previous_tokens.append(word)
                word = choose_your_word(word)
                result.append(word)
                break

        while len(previous_tokens) >= args.depth - 1:
            previous_tokens = previous_tokens[1:]

    if not args.output_file:
        print(' '.join(word for word in result))
    else:
        with open(args.output_file, 'w') as output:
            print(' '.join(word for word in result), file=output)



