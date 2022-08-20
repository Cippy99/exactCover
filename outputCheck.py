import argparse
import csv


def line_to_set(line):
    line = line.strip('\n')
    line = line.strip('{}')
    return set(line.split(','))


def read_sets_from_file(f):
    sets = []
    with open(f, 'r')as f:
        for line in f:
            if line.startswith(';;;'):
                continue
            sets.append(line_to_set(line))

    return sets


def check(file1, file2):
    sets1 = read_sets_from_file(file1)
    sets2 = read_sets_from_file(file2)

    return sets1 == sets2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exact Cover output checker')
    parser.add_argument('file1', metavar='', help='Input file 1')
    parser.add_argument('file2', metavar='', help='Input file 2')

    args = parser.parse_args()

    result = check(args.file1, args.file2)

    print(f'Output files are {"" if result else "not "}equal')
