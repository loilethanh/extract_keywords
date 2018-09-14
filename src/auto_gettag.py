from src.rake_run import *
import time
import datetime
from setup import *


def get_lastday_file(file_):

    file  = open(file_,"r")
    date = file.read()
    print(file_, "  ",date)
    file.close()
    return date

def write_file(date,file_) :
    try:
        file = open(file_,"w")
        file.write(date)
        file.close()
        print("Done !")
    except Exception as e :
        print(e)

def insert_auto(date,stop_words,models,feature_names):
    news = get_new_nearly(date)
    print("length news nearly :",len(news))
    last_insert = ""
    if ( len(news) > 0 ):
        last_insert = news[len(news)-1]['insertDate']

        for row in news:
            # result = run_content(row, stop_words, models, feature_names)
            result,c = run_api(row['news_id'],stop_words, models, feature_names)
            string = ''
            for r in result:
                string += r + ";"
            if ("\'") in string:
                str = ''
                split = string.split("\'")
                for i in range(len(split) - 1):
                    str += split[i].strip() + "\\" + "\'"
                str += split[len(split) - 1].strip()
                string = str
            update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print(row['news_id'], update_date, row['insertDate'], string)
                insert(row['news_id'], update_date, row['publishDate'], string)
                print("\n")

            except Exception as e:
                print(e)

    return last_insert
