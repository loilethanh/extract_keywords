from src.auto_gettag import *
from src.data_access import *

if __name__ == '__main__':


    models, feature_names = load_model(file_model)
    stop_words = load_stopwords_tfidf(stoppath)

    time.clock()


    while True:
        date = get_lastday_file()

        last_insert = insert_auto(date,stop_words,models,feature_names)
        print("last_insert :",last_insert)

        if last_insert != "":
            write_file(str(last_insert))
        else:
            print("Nothing to write and update file !")
        time.sleep(5)
        print("===================================end=================================")