from src.rake_run import *
from setup import  *
from src.data_access import *
from src.tfidf import *
from collections import Counter

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

    id = '2018091317064979'

    row = get_all_content(id)
    model,feature_names = load_model(file_model)
    print("leng feature_name : ", len(feature_names))
    stop_words = load_stopwords_tfidf(stoppath)

    results , contents = run_api(id,stop_words,model,feature_names)
    print(row['tags'])

    # update_tags(id,results)

