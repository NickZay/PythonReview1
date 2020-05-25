import argparse
import calculation
import generation


parser = argparse.ArgumentParser(description='Program which can make text itself')
subparsers = parser.add_subparsers()

calculate_parser = subparsers.add_parser('calculate', help='calculate probabilities')
calculate_parser.add_argument('-i', '--input_file', help='file to calculate from', default='Alice.txt')
calculate_parser.add_argument('-p', '--probabilities_file', help='file to write to', default='probabilities.txt')
calculate_parser.add_argument('-d', '--depth', type=int, help='depth of calculation', default=3)
calculate_parser.set_defaults(func=calculation.calculate)

generate_parser = subparsers.add_parser('generate', help='generate text from database')
generate_parser.add_argument('-p', '--probabilities_file', help='file to learn info from', default='probabilities.txt')
generate_parser.add_argument('-o', '--output_file', help='file to generate to')
generate_parser.add_argument('-d', '--depth', type=int, help='depth of finding words', default=3)
generate_parser.add_argument('-c', '--count', type=int, help='number of words to generate', default=100)
generate_parser.add_argument('-v', '--verbosity', type=int, help='0 is just text, and 1 is with original', default=0)
generate_parser.set_defaults(func=generation.generate)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
