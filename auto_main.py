from src.auto_gettag import *
from src.data_access import *
# from src.tfidf_v2 import *
from src.tfidf import *
# from tfidf_run import *
from datetime import timedelta



if __name__ == '__main__':

    models, feature_names = load_model(file_model)

    stop_words = load_stopwords_tfidf(stoppath)
    # start = time.time()
    while True:
        date_update = get_lastday_file(file_update)
        now = datetime.datetime.now()
        ob = datetime.datetime.strptime(date_update, '%Y-%m-%d %H:%M:%S') + timedelta(days=3)
        print(ob)
        # Last_date for get news auto generate tags
        date = get_lastday_file(file_lastdate)

        """
         Update model if time >= 3 days

        """

        if  now.date() > ob.date() :
            print("Updating Models TFIDF !")
            doc_set = getData()
            print("lenght : ",len(doc_set))
            build_models(doc_set, file_model , True)
            models,feature_names = load_model(file_model)
            write_file(str(now.strftime("%Y-%m-%d %H:%M:%S")), file_update)
            print("Update to Done !")

        last_insert = insert_auto(date, stop_words, models, feature_names)
        print("last_insert :", last_insert)

        if last_insert != "":
            write_file(str(last_insert),file_lastdate)
        else:
            print("Nothing to write and update file !")

        print("===================================end=================================")

        time.sleep(5)
