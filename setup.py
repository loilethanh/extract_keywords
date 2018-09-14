
config_path ="config.json"
threshold = 5
file_lastdate = "data/last_datetime.txt"
file_update = "data/last_update.txt"

# stoppath = "data/stoplists/stopwords.txt"

stoppath = "data/stoplists/vietnamese-stopwords.txt"
file_model = 'models/vectorizer_v2.pk'
# file_model_test = 'models/vectorizer_test.pk'
# model_tfidf_file = "models/models.tfidf"
# dictionary_file ="models/tfidf.dict"

PoS_tag = ['Np','Ny']
PoS = ['Nu', 'L', 'Ny', "C", "Cc", "T", 'X', "E", 'Z', 'A', 'R', 'M']
PoS_v2 = ['Nu', 'L', 'Ny', "C", "Cc", "T", 'X', "E", 'R', 'Z', 'A', ]

check_pos = ['Nu','L','Ny',"C","Cc","T",'X',"E",'R','Z','M',"V",'P','A','Nc','Nb',
             'VV','NV','VN','NpV','VVb','VA','AA','NP',
             'NNV']

check_pos_word = ['Z','N','Nu','Nc','M','R','V','A']
