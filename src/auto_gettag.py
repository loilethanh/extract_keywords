from src.rake_run import *
import time
import datetime

file_lastdate = "../data/last_datetime.txt"

def get_last_day_():

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

def insert_auto(date,models,feature_names):
    news = get_new_nearly(date)
    for row in news :
        print(row['news_id'])
        result = run_content(row,stop_words,models,feature_names)
        string = ''
        for r in result:
            string += r + ";"
        print(row['news_id'],row['publishDate'],row['publishDate'],string)
        try:
            insert(row['news_id'],row['publishDate'],row['publishDate'],string)
        except Exception as e :
            print(e)

if __name__ == '__main__':
    models, feature_names = load_model(file_model)
    stop_words = load_stopwords_tfidf(stoppath)
    start = time.time()

    time.clock()

    while True:
        elapsed = time.time() - start
        print ("loop cycle time: %f, seconds count: %02d" % (time.clock(),elapsed))
        date = get_last_day_()
        insert_auto(date,models,feature_names)
        last_Date = get_last_day()['last_date']
        write_file(str(last_Date))
        time.sleep(5)
        print("====================================================================")