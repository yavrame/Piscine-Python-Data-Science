import sys

class Research:
    def __init__(self, file_name):
        self.file_name = file_name

    def file_reader(self):
        with open(self.file_name, 'r') as file:
            return(file.read())

def check_arg(file_name):
    with open(file_name, 'r') as file:
        line = file.readlines()
        if len(line) < 2 or len(line[0].split(',')) !=2:
            raise Exception("Error argument")
        for i in range(1, len(line) - 1):
            if line[i] != '0,1\n' and line[i] != '1,0\n':
                raise Exception("Error argument")

if __name__ == '__main__':
    if len (sys.argv) != 2 or check_arg(sys.argv[1]):
        raise Exception("Error argument")
    print(Research(sys.argv[1]).file_reader())
