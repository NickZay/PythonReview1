from texteditor import text_improver
import random
import pickle


def choose_and_add_word(data, previous_tokens, result, editor, verbosity):
    rand = random.random()
    sum_of_prob = 0.0
    for word, prob in data[len(previous_tokens) + 1][tuple(previous_tokens)].items():
        sum_of_prob += prob
        if sum_of_prob > rand:
            previous_tokens.append(word)
            if verbosity == 1:
                print(word, end=' ')
            word = editor(word)
            result.append(word)
            break


def cut_previous_tokens(data, previous_tokens, depth):
    while previous_tokens and (len(previous_tokens) >= depth - 1) or \
            (not (tuple(previous_tokens) in data[len(previous_tokens) + 1])):
        previous_tokens = previous_tokens[1:]
    return previous_tokens


def generate(args):
    with open(args.probabilities_file, "rb") as read_file:
        data = pickle.load(read_file)
    assert data[0] >= args.depth, f'You only have {data[0]} depth'

    previous_tokens = []
    result = []
    editor = text_improver(args.count)

    if args.verbosity == 1:
        print("Текст курильщика:")

    for _ in range(args.count):
        previous_tokens = cut_previous_tokens(data, previous_tokens, args.depth)
        choose_and_add_word(data, previous_tokens, result, editor, args.verbosity)

    if args.verbosity == 1:
        print("\n\nТекст здорового человека:")
        if args.output_file:
            print("(In your file)")

    answer = ' '.join(word for word in result if word)
    if not args.output_file:
        print(answer)
    else:
        with open(args.output_file, 'w') as output:
            print(answer, file=output)
