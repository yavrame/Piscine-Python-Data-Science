from config import *
from analytics import Research
import logging
import json
import requests

def send_in_telegramm(text):
    token = "5464113755:AAFN0dPEiUnsamwtzTa6HkhUJWSjWwo21V8"
    chat_id = "498146952"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
    results = requests.get(url_req)
    if results.status_code != 200:
        raise Exception(f'Error server {results.status_code}')

def check_arg(file_name):
    logging.info("Check arguments")
    with open(file_name, 'r') as file:
        line = file.readlines()
        if len(line) == 0 or (len(line) == 1 and (line[0] != '0,1\n' and line[0] != '1,0\n')):
            send_in_telegramm('The report hasn’t been created due to an error')
            raise Exception("Error argument")
        if len(line) > 1:
            for i in range(1, len(line) - 1):
                if line[i] != '0,1\n' and line[i] != '1,0\n':
                    send_in_telegramm('The report hasn’t been created due to an error')
                    raise Exception("Error argument")

def main():
    logging.basicConfig(filename=f'{LOG_FILE}.{EXTENSION_LOG}', 
                        format='%(asctime)s %(message)s',
                        datefmt='%y-%d-%m %H:%M:%S',
                        filemode='w',
                        level=logging.DEBUG)
    if check_arg(FILEPATH):
        send_in_telegramm('The report hasn’t been created due to an error')
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
        observations, 
        tails_count,
        heads_count, 
        tails_fractions,
        heads_fractions,
        NUM_OF_STEPS,
        predict_heads_count,
        predict_tails_count
        )

    Research.Analytics.save_file(report, REPORT_FILE, EXTENSION)
    send_in_telegramm('The report has been successfully created')
    

if __name__ == '__main__':
    main()
