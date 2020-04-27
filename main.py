import pickle
import argparse
import random
import string
from sys import stdout, stderr


class MakeSentenceGreatAgain:
    def __init__(self, number_of_words):
        self.has_quote = False
        self.counter = 0
        self.num_of_words = number_of_words
        self.is_start_sentence = True
        self.what_quote = 0

    def __call__(self, arg):
        self.counter += 1
        arg = arg.replace("--", "–")
        arg = arg.replace("(", "")
        arg = arg.replace(")", "")
        arg = arg.replace("[", "")
        arg = arg.replace("]", "")
        arg = arg.replace("{", "")
        arg = arg.replace("}", "")
        arg = arg.replace("_", "")

        beg_quotes = ('“', '"', '«', '‘')
        end_quotes = ('”', '"', '»', '’')
        signs = ('.', '?', '!')

        if arg in string.punctuation:
            if self.counter == self.num_of_words:
                return '.'
            return None

        if arg[0] in beg_quotes:
            if self.has_quote:
                arg = arg[1:]
            else:
                self.what_quote = beg_quotes.index(arg[0])
            self.has_quote = True
        elif len(arg) > 1 and (arg[1] in beg_quotes):
            if self.has_quote:
                arg = arg[2:]
            else:
                self.what_quote = beg_quotes.index(arg[1])
            self.has_quote = True
        if arg[-1] in end_quotes:
            arg = arg[:-1]

        if arg[-1] in end_quotes:
            if not self.has_quote:
                arg = arg[:-1]
            if self.counter != self.num_of_words:
                self.has_quote = False
        elif len(arg) > 1 and arg[-2] in end_quotes:
            if not arg.endswith("’s") and not arg.endswith("’t"):
                if not self.has_quote:
                    arg = arg[:-2] + arg[-1]
                if self.counter != self.num_of_words:
                    self.has_quote = False

        if self.is_start_sentence:
            k = 0
            while k < len(arg) - 1 and arg[k] not in string.ascii_letters:
                k += 1
            else:
                arg = arg[:k] + arg[k].capitalize() + arg[k + 1:]
            self.is_start_sentence = False
        if arg[-1] in signs or (len(arg) > 1 and arg[-2] in signs):
            if self.has_quote and arg[-1] not in end_quotes:
                arg += end_quotes[self.what_quote]
                if self.counter != self.num_of_words:
                    self.has_quote = False
            self.is_start_sentence = True

        if self.counter == self.num_of_words:
            k = -1
            while k > -len(arg) and arg[k] not in string.ascii_letters:
                k -= 1
            else:
                if k != -1:
                    arg = arg[:k + 1]
            arg += '.'
            if self.has_quote:
                arg += end_quotes[self.what_quote]
        return arg


parser = argparse.ArgumentParser()
# positional
parser.add_argument('mode', type=str, help='calculate or generate')
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
                    help='file to generate to', default='')
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

    for deep in range(0, args.depth):
        result = dict()
        for i in range(deep, len(words)):
            current = tuple(words[i - deep: i])
            if current not in result.keys():
                result[current] = dict()
            if words[i] not in result[current].keys():
                result[current][words[i]] = 0
            result[current][words[i]] += 1
        for key in result.keys():
            amount = 0
            for inner_key in result[key].keys():
                amount += result[key][inner_key]
            for inner_key in result[key].keys():
                result[key][inner_key] /= amount
        probabilities.append(result)

    with open(args.probabilities_file, "wb") as write_file:
        pickle.dump(probabilities, write_file)

elif args.mode == 'generate':
    with open(args.probabilities_file, "rb") as read_file:
        data = pickle.load(read_file)
    if data[0] < args.depth:
        print(f'You only have {data[0]} depth', file=stderr)
        raise IndexError

    combination = []
    length = 0
    result = []
    fighter_for_justice = MakeSentenceGreatAgain(args.count)
    for j in range(args.count):
        rand = random.random()
        sum_of_prob = float()

        while length > 0 and not (tuple(combination) in
                                  data[length + 1].keys()):
            combination = combination[1:]
            length -= 1

        for word, value in data[length + 1][tuple(combination)].items():
            sum_of_prob += value
            if sum_of_prob > rand:
                combination.append(word)
                word = fighter_for_justice(word)
                result.append(word)
                length += 1
                break

        while length >= args.depth - 1:
            combination = combination[1:]
            length -= 1

    if args.output_file == '':
        for word in result:
            if word:
                print(word, end=' ')
    else:
        with open(args.output_file, 'w') as output:
            for word in result:
                if word:
                    print(word, end=' ', file=output)

