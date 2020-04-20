import pickle
import argparse
import random
import string
from sys import stdout, stderr


def is_last_sign(a):
    if a == "." or a == "!" or a == "?":
        return True
    else:
        return False


parser = argparse.ArgumentParser()
# positional
parser.add_argument('mode', type=str, help='calculate or generate')
# optional required=True
parser.add_argument('-i', '--input_file', type=str,
                    help='file to calculate from', default='AliceInWonderland.txt')
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
    has_quote = False
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

                word = word.replace("--", "")
                word = word.replace("(", "")
                word = word.replace(")", "")
                word = word.replace("'", '"')
                if 'n"t' in word:
                    word = word.replace('n"t', "n't")
                if '"s' in word:
                    word = word.replace('"s', "'s")
                    word = word.replace('"S', "'S")
                if '"ve' in word:
                    word = word.replace('"ve', "'ve")
                if '"ll' in word:
                    word = word.replace('"ll', "'ll")

                if word[0] == '"':
                    if has_quote:
                        word = word[1:]
                    has_quote = True
                if word[-1] == '"':
                    if not has_quote:
                        word = word[:-1]
                    has_quote = False
                if is_last_sign(word[-1]) and has_quote:
                    word = word[:-1] + '"' + word[-1]
                    has_quote = False
                if len(word) > 1 and is_last_sign(word[-1]):
                    if not has_quote and word[-2] == '"':
                        word = word.replace('"', "")

                if len(result) == 0 or is_last_sign(result[-1][-1]):
                    index = 0
                    while index < len(word) - 1 and word[index] \
                            in string.punctuation:
                        index += 1
                    else:
                        word = word[:index] + word[index].capitalize() \
                               + word[index + 1:]

                if len(word) > 1 and word[-2] == '.' and word[-1] == '"':
                    word = word[:-2] + '".'
                result.append(word)
                length += 1
                break

        while length >= args.depth - 1:
            combination = combination[1:]
            length -= 1

    index = -1
    while index > -len(result[-1]) and result[-1][index] \
            in string.punctuation:
        index -= 1
    else:
        if index != -1:
            result[-1] = result[-1][:index + 1]

    if has_quote:
        result[-1] = result[-1] + '"'
    result[-1] = result[-1] + '.'

    if args.output_file == '':
        for word in result:
            print(word, end=' ')
    else:
        with open(args.output_file, 'w') as output:
            for word in result:
                print(word, end=' ', file=output)
