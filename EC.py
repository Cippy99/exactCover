import argparse
import os
import time
from collections import Counter
from os.path import splitext
from fileGenerator import write_cardinalities


class ExactCover:
    def __init__(self, input_file):
        self.a = {}
        self.b = {}
        self.input_file = input_file
        self.covers = set()

        with open(input_file, 'r') as inf:
            for line in inf:
                # Ignore comments
                if line.startswith(';;;'):
                    continue
                else:
                    n = len(line.strip().replace('-', ''))
                    break

        self.m = {i for i in range(1, n + 1)}

    @staticmethod
    def to_set(line):
        i = 0
        result = set()
        for c in line:
            i += 1
            if c == '1':
                result.add(i)
        return result

    def write_set(self, file, to_write_set):
        self.covers.add(frozenset(to_write_set))
        file.write(str(to_write_set) + '\n')
        print(f"Exact Cover found: {str(to_write_set)}")

    @staticmethod
    def write_input_cards(file):
        pass

    def write_stats(self, file, exec_time, user_stop=False):
        if user_stop:
            file.write(';;;Process terminated by user\n')
            file.write(f';;;Analyzed {len(self.a) - 1} sets\n')
        else:
            file.write(';;;Execution complete\n')
            file.write(f';;;Analyzed all {len(self.a) - 1} sets\n')

        file.write(f';;;Found {len(self.covers)} cover{"" if len(self.covers) == 1 else "s"}\n')
        write_cardinalities(file, Counter([len(x) for x in self.covers]), ';;;Cardinality of covers:\n')
        self.write_input_cards(file)
        file.write(f';;;Execution time:{exec_time:.2f}\n')

    @staticmethod
    def print_report(exec_time, n_sets):
        print(f"{time.strftime('%M:%S', time.gmtime(exec_time))} - Analyzed {n_sets} sets")

    def store_card(self, card, index):
        pass

    def generate_u(self, set1, set2):
        return set1.union(set2)

    def generate_u_explore(self, set1, set2):
        return set1.union(set2)

    def check_cover(self, to_check):
        return to_check == self.m

    def explore(self, ind, u_set, intersect, outf):
        for k in sorted(intersect):
            itemp = ind.union({k})
            utemp = self.generate_u_explore(u_set, self.a[k])

            if self.check_cover(utemp):
                self.write_set(outf, itemp)
            else:
                intertemp = intersect.intersection(self.b[k])
                if len(intertemp) != 0:
                    self.explore(itemp, utemp, intertemp, outf)

    def ec(self, output_file, quiet=False):

        start_time = time.time()
        i = 0
        each = 25  # Frequency of reports

        name, ext = splitext(self.input_file)

        input_file_wiht_id = f"{name}_commented{ext}"
        if os.path.exists(input_file_wiht_id):
            os.remove(input_file_wiht_id)
        if os.path.exists(output_file):
            os.remove(output_file)

        with open(self.input_file, 'r') as inf, open(output_file, 'a') as outf, open(input_file_wiht_id, 'a') as infid:
            try:
                for line in inf:
                    # Ignore comments, just copy in the other file
                    if line.startswith(';;;'):
                        infid.write(line)
                        continue

                    i += 1

                    # Copy line to new file and prepend set number
                    infid.write(f";;;Set {i}\n")
                    infid.write(line)

                    self.b[i] = set()

                    # Remove trailing '\n' and row separator
                    line = line.strip().replace('-', '')

                    # Read line and add to A
                    self.a[i] = self.to_set(line)

                    # Start of Algorithm
                    if len(self.a[i]) == 0:
                        break

                    if self.a[i] == self.m:
                        self.write_set(outf, {i})
                        break

                    self.store_card(len(self.a[i]), i)

                    for j in range(1, i):
                        if len(self.a[i].intersection(self.a[j])) == 0:
                            i_set = {i, j}  # i_set is I of pseudocode
                            # u contains a[i] union a[j] (or |A[i]| + |A[j]| for EC+)
                            u = self.generate_u(self.a[i], self.a[j])
                            if self.check_cover(u):
                                self.write_set(outf, i_set)
                            else:
                                self.b[i].add(j)
                                inter = self.b[i].intersection(self.b[j])
                                if len(inter) != 0:
                                    self.explore(i_set, u, inter, outf)

                    # Write report every 'each' sets analyzed
                    if (i % each == 0) and not quiet:
                        self.print_report(time.time() - start_time, i)

                end_time = time.time()
                self.write_stats(outf, end_time - start_time)

            except KeyboardInterrupt:
                end_time = time.time()
                self.write_stats(outf, end_time - start_time, user_stop=True)


class ExactCoverPlus(ExactCover):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.card = {}

    def store_card(self, card, index):
        self.card[index] = card

    def generate_u(self, set1, set2):
        return len(set1) + len(set2)

    def generate_u_explore(self, card1, set2):
        return card1 + len(set2)

    def check_cover(self, to_check):
        return to_check == len(self.m)

    def write_input_cards(self, file):
        write_cardinalities(file, Counter(list(self.card.values())), ';;;Cardinality of input sets:\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exact Cover problem solver')
    parser.add_argument('-i', '--input', required=True, metavar='', help='Input file containing matrix A')
    parser.add_argument('-o', '--output', metavar='', help='Output file (without extension)')
    parser.add_argument('-q', '--quiet', action='store_true', help='If present, no reports will be printed')
    parser.add_argument('-p', '--plus', action='store_true', help='Plus version of the algorithm')

    args = parser.parse_args()

    name_f, ext_f = splitext(args.input)
    out_file = f"{name_f}_out{'_p' if args.plus else ''}{ext_f}" if args.output is None else f"{args.output}.txt"

    ec = ExactCoverPlus(args.input) if args.plus is True else ExactCover(args.input)
    ec.ec(out_file, args.quiet)
