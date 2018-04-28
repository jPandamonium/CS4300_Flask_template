import json
import gzip
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA
import json
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import nltk.stem
from nltk.corpus import stopwords
import urllib2
# from empath import Empath
# import requests

# lexicon = Empath()







def unpickle(fileNames):
    file = urllib2.urlopen(fileNames[0])
    index_to_vocab = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[1])
    vocab_to_index = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[2])
    ind_to_title = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[3])
    ind_to_price = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[4])
    ind_to_rating = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[5])
    doc_by_vocab = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[6])
    ind_to_url = pickle.load(file)
    file.close()
    return index_to_vocab, vocab_to_index,ind_to_title,ind_to_price,ind_to_rating,doc_by_vocab,ind_to_url

n_feats = 3000

ind_to_vocab_file = "https://storage.googleapis.com/pickles/ind_to_vocab.pickle"
vocab_to_index_file = "https://storage.googleapis.com/pickles/vocab_to_indx.pickle"
ind_to_title_file = "https://storage.googleapis.com/pickles/ind_to_title.pickle"
ind_to_price_file = "https://storage.googleapis.com/pickles/ind_to_price.pickle"
ind_to_rating_file = "https://storage.googleapis.com/pickles/ind_to_rating.pickle"
doc_by_vocab_file = "https://storage.googleapis.com/pickles/doc_by_vocab.pickle"
ind_to_url_file = "https://storage.googleapis.com/pickles/ind_to_url.pickle"



def jaccard(query_words, sentence):
    A = set(query_words)
    B = set(sentence)
    return float(len(A.intersection(B)))/len(A.union(B))    



index_to_vocab, vocab_to_index,ind_to_title,ind_to_price, ind_to_rating, doc_by_vocab, ind_to_url = unpickle([ind_to_vocab_file,vocab_to_index_file,ind_to_title_file,
                           ind_to_price_file, ind_to_rating_file, doc_by_vocab_file,ind_to_url_file])

# def query_expansion(seed):
#     resp = requests.post("http://54.148.189.209:8000/create_category", json={"terms":seed,"size":100,"model":"nytimes"})
#     results = json.loads(resp.text)
#     results=set(results)

#     d={}
#     for item in results:
#         score = jaccard(lexicon.analyze(item,normalize=True),lexicon.analyze("cats",normalize=True))
#         if(score>=0.1):
#             d[item]=jaccard(item,"cats")

#     d=sorted(d.items(), key=lambda x:x[1], reverse=True)[:5]
#     return d




def vectorize_query(query):
    vector = np.zeros(n_feats,)
    ss = SnowballStemmer('english')
    tokens = nltk.word_tokenize(query)
    tokens = [ss.stem(i) for i  in tokens]
    # tokens = [query_expansion([i]) for i in tokens]
    # tokens = [item for sublist in tokens for item in sublist]
    stop_words = set(stopwords.words('english'))
    for i in tokens:
        if i in stop_words:
            continue
        elif i in vocab_to_index:
            index = vocab_to_index[i]
            vector[index] += 1
    return np.transpose(vector)





def calc_sort (matrix,query, lower = 0 , upper = None ):
    vector = vectorize_query(query)
    res = cosine_similarity((vector), (matrix)).reshape(-1)
    arg_sort_array = np.argsort(res)[::-1]
    top_scores = np.sort(res)[::-1]
    if lower is 0 and upper is None :
        arg_sort_array  = arg_sort_array[:5]
    elif lower is 0 :
        upper = float(upper)
        temp = []
        for i in arg_sort_array:
            if float(ind_to_price[i]) > upper:
                continue
            else:
                temp.append(i)
                if len(temp) is 5:
                    arg_sort_array = temp
                    break
    elif upper is None  :
        lower = float(lower)
        temp = []
        for i in arg_sort_array:
            if float(ind_to_price[i]) < lower:
                continue
            else:
                temp.append(i)
                if len(temp) is 5:
                    arg_sort_array = temp
                    break
    else:
        temp = []
        upper = float(upper)
        lower = float(lower)
        for i in arg_sort_array:    
            if float(ind_to_price[i]) < lower or float(ind_to_price[i]) > upper:
                    continue
            else:
                temp.append(i)
                if len(temp) is 5:
                    arg_sort_array = temp
                    break


    return ([ind_to_title[i] for i in arg_sort_array] , [ind_to_price[i] for i in arg_sort_array], [ind_to_rating[i] for i in arg_sort_array],[ind_to_url[i] for i in arg_sort_array],top_scores[:5])
