
from sklearn.feature_extraction.text import TfidfVectorizer
#
#
corpus = ["tim have jam and chocolates",
          "say hi haha tim and jam ",
          "now you see me 2"]
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2))
#
tf.fit(corpus)
# voc = tfidf_matrix.vocabulary_
# print(voc.__len__())

# tfs = TfidfVectorizer(analyzer='word', ngram_range=(1,3),vocabulary= voc)
str = ["say hihi hi haha yeal for all everybody with jam and tim",
       "tim"]

tfidf = tf.fit_transform(str)
# print(tfidf)
# print(tfidf.vocabulary_.__len__())

# print(tfidf)
# print(tfidf_matrix)
#
feature_names = tf.get_feature_names()
#
doc = 0
feature_index = tfidf[doc,:].nonzero()[1]
#
tfidf_scores = zip(feature_index, [tfidf[doc, x] for x in feature_index])
#
result = []
for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
    print(w,s)
    # result.append((str(w),s))
#
# result.sort(key= lambda x: x[1],reverse= True)
# print(result)
