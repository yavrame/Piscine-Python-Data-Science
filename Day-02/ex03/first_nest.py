import sys

class Research:
    def __init__(self, file_name):
        self.file_name = file_name

    def file_reader(self, has_header = True):
        with open(self.file_name, 'r') as file:
            line = file.readlines()
            if line[0] == '0,1\n' or line[0] == '1,0\n':
                self.has_header = False
            start = 0
            if has_header == True:
                start = 1
            list_lists = []
            for i in range(start, len(line)):
                list_i = [int(line[i][0])]
                list_i.append(int(line[i][2]))
                list_lists.append(list_i)
            return(list_lists)

    class Calculations:
        def counts(list_lists):
            heads = 0
            tails = 0
            for i in range(len(list_lists)):
                if list_lists[i][0] == 1:
                    heads += 1
                else:
                    tails += 1
            return(heads, tails)

        def fractions(list_counts):
            sum_counts = list_counts[0] + list_counts[1]
            return(list_counts[0] / sum_counts, list_counts[1] / sum_counts)


def check_arg(file_name):
    with open(file_name, 'r') as file:
        line = file.readlines()
        if len(line) == 0 or (len(line) == 1 and (line[0] != '0,1\n' and line[0] != '1,0\n')):
            raise Exception("Error argument")
        if len(line) > 1:
            for i in range(1, len(line) - 1):
                if line[i] != '0,1\n' and line[i] != '1,0\n':
                    raise Exception("Error argument")

if __name__ == '__main__':
    if len (sys.argv) != 2 or check_arg(sys.argv[1]):
        raise Exception("Error argument")
    list_lists = Research(sys.argv[1]).file_reader()
    print(list_lists)
    list_counts = Research.Calculations.counts(list_lists)
    print(list_counts[0], list_counts[1])
    list_fractions = Research.Calculations.fractions(list_counts)
    print(list_fractions[0], list_fractions[1])
