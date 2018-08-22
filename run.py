from src.rake_run import *
from setup import  *

if __name__ == '__main__' :

    model,feature_names = load_model(file_model)

    start = time.time()
    stop_words = load_stopwords_tfidf(stoppath)
    print("time load stop words :", time.time() - start )
    id = "2018082015053018"
    start = time.time()
    results , contents = run_api(id,stop_words,model,feature_names)
    # print("contents :",contents)
    # run_all_data(stop_words,model,feature_names)
    print("--- %s seconds ---" % (time.time() - start))
    # get_content(id)
