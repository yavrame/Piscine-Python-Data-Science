import sys
from random import randint

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
        def __init__(self, data):
            self.data = data 
            self.count = self.counts()
            self.fractions = self.fractions()

        def counts(self):
            x = [x[0] for x in self.data]
            y = [y[1] for y in self.data]
            return [sum(x), sum(y)]

        def fractions(self):
            return [(self.count[0] / (self.count[0] + self.count[1])) * 100,
                    (self.count[1] / (self.count[0] + self.count[1])) * 100]


    class Analytics(Calculations):
        def __init__(self, n_steps):
            self.n_steps = n_steps
            self.predict = self.predict_random()
            self.predict_last = self.predict_last()

        def predict_random(self):
            predict_dict = {0: [0, 1], 1: [1, 0]}
            return [predict_dict[randint(0, 1)] for x in range(self.n_steps)]

        def predict_last(self):
            return self.predict[-1]


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
    output = Research(sys.argv[1]).file_reader()
    element = Research.Calculations(output)
    predict = Research.Analytics(3)
    fractions = Research.Calculations.fractions(element)
    print(element.data)
    print(element.count[0], element.count[1])
    print(round(fractions[0], 2), round(fractions[1], 2))
    print(predict.predict)
    print(predict.predict_last)
