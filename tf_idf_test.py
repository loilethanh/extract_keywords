
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
# #
# corpus = ["tim have jam and chocolates",
#           "say hi haha tim and jam ",
#           "now you see me 2"]
# tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2))
# # #
# tf.fit(corpus)
# # # # pickle.dump(tf, open("vectorizer.pickle", "wb"))
# with open('vectorizerss.pk', 'wb') as fin:
#     model = pickle.dump(tf, fin)
# # # # #


with open('vectorizerss.pk', 'rb') as fin:
    tf = pickle.load(fin)

# #
str = ["tim and jam say hi hi haha and see me"]
# # #
# # #
# # #
tfidf = tf.fit_transform(str)
# # #
# # # #
feature_names = tf.get_feature_names()
#
doc = 0
feature_index = tfidf[doc,:].nonzero()[1]
tfidf_scores = zip(feature_index, [tfidf[doc, x] for x in feature_index])
result = []
for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
    # print(w,s)
    result.append((w,s))
#
result.sort(key= lambda x: x[1],reverse= True)
print(result)
