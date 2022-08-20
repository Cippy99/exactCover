import os
import random
import argparse
from scipy.stats import truncnorm
from collections import Counter


def generate_set(cardinality, total_elements):
    result = set()
    result = set(random.sample(range(1, total_elements + 1), cardinality))
    return frozenset(result)


def generate_random_set_of_sets(n_sets, total_elements):
    result = set()
    cardinalities = [random.randint(1, total_elements - 1) for _ in range(n_sets)]
    for c in cardinalities:
        result.add(generate_set(c, total_elements))

    cards = [len(x) for x in result]
    return result, Counter(cards)


def generate_normal_set_of_sets(n_sets, total_elements, around):
    result = set()
    scale = total_elements / 10
    cardinalities = truncnorm(a=(1 - around) / scale, b=(total_elements - around) / scale, loc=around, scale=scale) \
        .rvs(size=n_sets)
    cardinalities = cardinalities.round().astype(int)

    for c in cardinalities:
        result.add(generate_set(c, total_elements))

    # print(sorted(cardinalities))
    cards = [len(x) for x in result]
    # print(sorted(cards))
    return result, Counter(cards)


def write_cardinalities(open_file, cards, title=';;;Cardinality of sets:\n'):
    if len(cards) == 0:
        return
    m = max(cards.values())
    max_length = 25
    open_file.write(title)
    for k, v in sorted(cards.items()):
        open_file.write(';;;')
        for count in range(max_length):
            length = int(max_length * (v / m))
            open_file.write('*' if count <= length else ' ')

        open_file.write(f'\t{v:3} | c={k}\n')


def generate_file(file, sets, total_elements, cardinalities):
    if os.path.exists(file):
        os.remove(file)

    line = ""
    with open(file, 'a') as f:
        f.write(';;;Number of sets: ' + str(len(sets)) + '\n')
        f.write(';;;Number of elements: ' + str(total_elements) + '\n')

        write_cardinalities(f, cardinalities)

        for s in sets:
            for i in range(1, total_elements + 1):
                if i in s:
                    f.write('1')
                else:
                    f.write('0')
            f.write('-\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate input files for exact cover problem')
    parser.add_argument('-s', '--nsets', type=int, metavar='', required=True, help='Number of sets of the problem')
    parser.add_argument('-t', '--total', type=int, metavar='', required=True,
                        help='Number of total different elements in all sets')
    parser.add_argument('-a', '--around', type=int, metavar='',
                        help='If present, cardinality of sets is drawn from normal '
                             'distribution with this value as average')
    parser.add_argument('-f', '--file', metavar='', help='Name of the output file (without extension)')
    parser.add_argument('-nf', '--nfiles', type= int, metavar='', help='Number of files to generate')
    args = parser.parse_args()

    set_of_sets, stats = generate_random_set_of_sets(args.nsets, args.total) if args.around is None \
        else generate_normal_set_of_sets(args.nsets, args.total, args.around)

    if args.nfiles is None:
        file_name = 'out.txt' if args.file is None else args.file + '.txt'
        generate_file(file_name, set_of_sets, args.total, stats)

    else:
        for i in range(1, args.nfiles + 1):
            file_name = f'out_{i}.txt' if args.file is None else f'{args.file}_{i}' + '.txt'
            generate_file(file_name, set_of_sets, args.total, stats)
