from config import *
from analytics import Research

def check_arg(file_name):
    with open(file_name, 'r') as file:
        line = file.readlines()
        if len(line) == 0 or (len(line) == 1 and (line[0] != '0,1\n' and line[0] != '1,0\n')):
            raise Exception("Error argument")
        if len(line) > 1:
            for i in range(1, len(line) - 1):
                if line[i] != '0,1\n' and line[i] != '1,0\n':
                    raise Exception("Error argument")

def main():
    if check_arg(FILEPATH):
        raise Exception("Error argument")
    output = Research(FILEPATH).file_reader()
    element = Research.Calculations(output)
    predict = Research.Analytics(3)
    observations = len(output)
    heads_count = element.count[0]
    tails_count = element.count[1]
    heads_fractions = round(element.fractions[0], 2)
    tails_fractions = round(element.fractions[1], 2)
    predict_heads_count = predict.count[0]
    predict_tails_count = predict.count[1]

    report = REPORT.format(
        observations , 
        tails_count,
        heads_count, 
        tails_fractions,
        heads_fractions,
        NUM_OF_STEPS,
        predict_heads_count,
        predict_tails_count
        )

    Research.Analytics.save_file(report, REPORT_FILE, EXTENSION)

if __name__ == '__main__':
    main()
