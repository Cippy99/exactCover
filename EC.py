class ExactCover:
    def __init__(self):
        pass

    @staticmethod
    def to_set(line):
        i = 0
        result = set()
        for c in line:
            i += 1
            if c == '1':
                result.add(i)
        return result

    @staticmethod
    def write_set(file, to_write_set):
        file.write(str(to_write_set) + '\n')

    def ec(self, input_file, output_file):
        a = {}
        b = {}
        i = 0
        # Initialize m
        with open(input_file, 'r') as inf:
            for line in inf:
                # Ignore comments
                if line.startswith(';;;'):
                    continue
                else:
                    n = len(line.strip().replace('-', ''))

        m = {i for i in range(1, n + 1)}

        def explore(ind, u_set, intersect):
            for k in sorted(intersect):
                itemp = ind.union({k})
                utemp = u_set.union(a[k])

                if utemp == m:
                    self.write_set(outf, itemp)
                else:
                    intertemp = intersect.intersection(b[k])
                    if len(intertemp) != 0:
                        explore(itemp, utemp, intertemp)

        with open(input_file, 'r') as inf, open(output_file, 'a') as outf:
            for line in inf:
                # Ignore comments
                if line.startswith(';;;'):
                    continue

                i += 1
                b[i] = set()

                # Remove trailing '\n' and row separator
                line = line.strip().replace('-', '')

                # Read line and add to A
                a[i] = self.to_set(line)

                # Start of Algorithm
                if len(a[i]) == 0:
                    break

                if a[i] == m:
                    self.write_set(outf, {i})
                    break

                for j in range(1, i):
                    if len(a[i].intersection(a[j])) == 0:
                        i_set = {i, j}
                        u = a[i].union(a[j])
                        if u == m:
                            self.write_set(outf, i_set)
                        else:
                            b[i].add(j)
                            inter = b[i].intersection(b[j])
                            if len(inter) != 0:
                                explore(i_set, u, inter)


if __name__ == '__main__':
    ec = ExactCover()
    # ec.ec('test/test2.txt', 'result2txt')
