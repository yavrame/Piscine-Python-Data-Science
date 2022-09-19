class Research:
    def file_reader():
        with open('data.csv', 'r') as file:
            return(file.read())

if __name__ == '__main__':
    print(Research.file_reader())
