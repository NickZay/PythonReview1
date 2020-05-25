from collections import defaultdict
import pickle
import string


def get_material(filename, encoding=None):
    words = []
    with open(filename, 'r', encoding=encoding) as book:
        for line in book:
            words += line.split()
    return words


def return_emptiness():
    return defaultdict(int)


def calculate(args):
    try:
        words = get_material(args.input_file, 'utf-8')
    except Exception:
        words = get_material(args.input_file)

    probabilities = [args.depth]

    for index in range(args.depth):
        result = defaultdict(return_emptiness)
        for i in range(index, len(words)):
            if words[i] not in string.punctuation:
                result[tuple(words[i - index: i])][words[i]] += 1
        for substring in result.keys():
            amount = sum(result[substring].values())
            for new_word in result[substring].keys():
                result[substring][new_word] /= amount
        probabilities.append(result)

    with open(args.probabilities_file, "wb") as write_file:
        pickle.dump(probabilities, write_file)
