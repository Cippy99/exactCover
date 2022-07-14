import os
import random
import argparse

parser = argparse.ArgumentParser(description='Generate input files for exact cover problem')
parser.add_argument('-n', '--nsets', type=int, metavar='', required=True, help='Number of sets of the problem')
parser.add_argument('-t', '--total', type=int, metavar='', required=True,
                    help='Number of total different elements in all sets')
parser.add_argument('-f', '--file', metavar='', help='Name of the output file (without extension)')
args = parser.parse_args()


def generate_set(cardinality, total_elements):
    result = set()
    for _ in range(cardinality):
        result.add(random.randint(1, total_elements))
    return frozenset(result)


def generate_set_of_sets(n_sets, total_elements):
    result = set()
    for _ in range(n_sets):
        result.add(generate_set(random.randint(1, total_elements - 1), total_elements))

    return result


def generate_file(file, sets, total_elements):
    if os.path.exists(file):
        os.remove(file)

    line = ""
    with open(file, 'a') as f:
        f.write(';;;Number of sets: ' + str(len(sets)) + '\n')
        f.write(';;;Number of elements: ' + str(total_elements) + '\n')

        for s in sets:
            for i in range(1, total_elements + 1):
                if i in s:
                    f.write('1')
                else:
                    f.write('0')
            f.write('-\n')


if __name__ == '__main__':
    set_of_sets = generate_set_of_sets(args.nsets, args.total)

    file_name = 'out.txt' if args.file is None else args.file + '.txt'
    generate_file(file_name, set_of_sets, args.total)
