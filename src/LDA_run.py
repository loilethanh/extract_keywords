from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
from gensim.models import CoherenceModel
import gensim, csv
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd

tokenizer = RegexpTokenizer(r'\w+')
data = []
stop_words = []
mallet_path = 'mallet-2.0.8/bin/mallet'

file_path = "data/data_news_soha_10000.csv"

for x in open('data/stoplists/vietnamese-stopwords.txt', 'r').read().split('\n'):
    stop_words.append(x)
6
for i in range(0,100):
    stop_words.append(str(i))
# print(stop_words)


def readFile():
    data = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content =''
            id = row['newsId']
            dict = {'id':id}
            content += row['title_token'] +" "+ row['sapo_token'] + " " + row['content_token']
            dict_content = {"content" : content}
            dict.update(dict_content)
            data.append(dict)
    return data[0:1000]

doc_set = readFile()
texts = []

def load_postag ():
    data_postag = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in  reader :
            content = ''
            id = row['newsId']
            content +=row['title_postag']+" "+row['sapo_postag']+" "+row['content_postag']

            content_postag ={}
            word_tokens = tokenizer.tokenize(content)
            for word in word_tokens :
                w = ''
                postag = ''
                for i in range(len(word)):
                    if word[i] == "_":
                        word= word[:i].lower()+"_"+word[i+1:].lower()
                    if word[i] == "/" :
                        w = word[:i].lower()
                        postag = word[i+1:]
                        break
                content_postag.update({w:postag})
            data_postag.append({'id':id,'content_postag':content_postag})
    return data_postag


def loadStopwords():
    data_pos = load_postag()
    pos = ['Ab','B','C','Cc','I','T','X','Z','R','M','CH','E','L','p']
    # pos=['C','Cc','A']
    stop_words = []
    for x in open('data/stoplists/vietnamese-stopwords.txt', 'r').read().split('\n'):
        stop_words.append(x)

    for d in data_pos :
        for w in d['content_postag'] :
            if(d['content_postag'][w] in pos ) :
                stop_words.append(w)

    return stop_words


def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


for d in doc_set:
    d = d['content']
    raw = d.lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = []
    for w in tokens:
        word = w
        # if(len(word) == 2 or len(word) == 1 ) :
        #     print(word)
        for i in range(len(w)):
            if (w[i] == "_"):
                word = w[:i] + " " + w[i + 1:]
        if not word in stop_words:
            if(len(word) > 5 ) :
                # print(word)
                stopped_tokens.append(w)
    # print(stopped_tokens)
    texts.append(stopped_tokens)


test = texts[0:5]
dictionary = corpora.Dictionary(texts)
dictionary.filter_extremes(no_below=1, no_above=0.2)

corpus = [dictionary.doc2bow(text) for text in texts]

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=20,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

# print('\nPerplexity: ', lda_model.log_perplexity(corpus))
coherence_model_lda = CoherenceModel(model=lda_model, texts = texts, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

print("saving model ...")
lda_model.save("model.lda")
print("\n done")

model = gensim.models.LdaModel.load("model.lda")
for topic in model.print_topics(num_words=10) :
    print(topic)
# #
#


###########################################################################################################
# ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=dictionary)
# for topic in ldamallet.show_topics(formatted=False) :
#     print(topic)
# #
# coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=texts, dictionary=dictionary, coherence='c_v')
# coherence_ldamallet = coherence_model_ldamallet.get_coherence()
# print('\nCoherence Score: ', coherence_ldamallet)

##################################################################################################################3


for i,d in enumerate(test) :
    bow = dictionary.doc2bow(d)
    print(doc_set[i]['id'])
    re = model.get_document_topics(bow, per_word_topics= False)
    print()






# ##########################################################################################Find k
# # model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=texts, start=10, limit=11, step=2)
# #
# # for m, cv in zip(x, coherence_values):
# #     print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
# # print(lda_model[corpus])
# # def format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data):
# #     # Init output
# #     sent_topics_df = pd.DataFrame()
# #
# #     # Get main topic in each document
# #     for i, row in enumerate(ldamodel[corpus]):
# #         print(row)
#     #     row = sorted(row, key=lambda x: (x[1]), reverse=True)
#     #     # Get the Dominant topic, Perc Contribution and Keywords for each document
#     #     for j, (topic_num, prop_topic) in enumerate(row):
#     #         if j == 0:  # => dominant topic
#     #             wp = ldamodel.show_topic(topic_num)
#     #             topic_keywords = ", ".join([word for word, prop in wp])
#     #             sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num),
#     #                                                               round(prop_topic,4), topic_keywords]), ignore_index=True)
#     #         else:
#     #             break
#     # sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
#     #
#     # # Add original text to the end of the output
#     # contents = pd.Series(texts)
#     # sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
#     # return(sent_topics_df)
#
#
# # df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=data)
#
# # Format
# # df_dominant_topic = df_topic_sents_keywords.reset_index()
# # df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
#
# # Show
# # df_dominant_topic.head(10)