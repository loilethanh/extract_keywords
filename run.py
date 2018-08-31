from src.rake_run import *
from setup import  *
from src.data_access import *
from src.tfidf_v2 import *
from src.tfidf import *

def update_tags(id, results ) :
    string = ''
    for r in results:
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
        print(id, update_date, string)
        update(id, update_date, string)
        print("\n")

    except Exception as e:
        print(e)


if __name__ == '__main__' :
    id = "201808020657441"
    row = get_all(id)
    print(row)
    model,feature_names = load_model(file_model)
    # models,dict = load_model()
    stop_words = load_stopwords_tfidf(stoppath)
    start = time.time()
    results , contents = run_api(id,stop_words,model,feature_names)
    # update_tags(id,results)
    print("--- %s seconds ---" % (time.time() - start))