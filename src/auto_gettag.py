from src.rake_run import *
import time
import datetime
from setup import *


def get_lastday_file():

    file  = open(file_lastdate,"r")
    date = file.read()
    print(date)
    file.close()
    return date

def write_file(date) :
    try:
        file = open(file_lastdate,"w")
        file.write(date)
        file.close()
        print("Done !")
    except Exception as e :
        print(e)

def insert_auto(date,stop_words,models,feature_names):
    news = get_new_nearly(date)
    print("length :",len(news))
    last_insert = ""
    if ( len(news) > 0 ):
        last_insert = news[len(news)-1]['insertDate']

        for row in news:
            result = run_content(row, stop_words, models, feature_names)
            string = ''
            for r in result:
                string += r + ";"
            update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(row['news_id'], update_date, row['insertDate'], string)
            try:
                insert(row['news_id'], update_date, row['publishDate'], string)
            except Exception as e:
                print(e)

    return last_insert
