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
    vocab_to_index = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[1])
    ind_to_title = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[2])
    ind_to_price = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[3])
    ind_to_rating = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[4])
    doc_by_vocab = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[5])
    ind_to_url = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[6])
    asin_dic = pickle.load(file)
    file.close()
    file = urllib2.urlopen(fileNames[7])
    text_dic = pickle.load(file)
    file.close()
    return  vocab_to_index,ind_to_title,ind_to_price,ind_to_rating,doc_by_vocab,ind_to_url,asin_dic,text_dic

n_feats = 1500

ind_to_vocab_file = "https://storage.googleapis.com/pickles/ind_to_vocab.pickle"
vocab_to_index_file = "https://storage.googleapis.com/pickles/vocab_to_indx.pickle"
ind_to_title_file = "https://storage.googleapis.com/pickles/ind_to_title.pickle"
ind_to_price_file = "https://storage.googleapis.com/pickles/ind_to_price.pickle"
ind_to_rating_file = "https://storage.googleapis.com/pickles/ind_to_rating.pickle"
doc_by_vocab_file = "https://storage.googleapis.com/pickles/doc_by_vocab.pickle"
ind_to_url_file = "https://storage.googleapis.com/pickles/ind_to_url.pickle"
asin_dic_file = "https://storage.googleapis.com/pickles/asin_dic.pickle"
text_dic_file = "https://storage.googleapis.com/pickles/text_dic.pickle"


def jaccard(query_words, sentence):
    A = set(query_words)
    B = set(sentence)
    return float(len(A.intersection(B)))/len(A.union(B))    



vocab_to_index,ind_to_title,ind_to_price, ind_to_rating, doc_by_vocab, ind_to_url,asin_dic,text_dic = unpickle([vocab_to_index_file,ind_to_title_file,
                           ind_to_price_file, ind_to_rating_file, doc_by_vocab_file,ind_to_url_file,asin_dic_file,text_dic_file])

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







def calc_sort (query, lower = 0 , upper = None ):
    vector = vectorize_query(query)
    res = cosine_similarity(vector, doc_by_vocab)
    res_sec = res.tolist()
    flatenned =  [item for sublist in res_sec for item in sublist]
    res = np.array(flatenned)
    arg_sort_array = np.argsort(res)[::-1]

    arg_sort_array = arg_sort_array.tolist()

    top_scores = np.sort(res)[::-1]
    top_scores = top_scores.tolist()
    if lower is '' and upper is '' :
        arg_sort_array  = arg_sort_array[:20]
    elif lower is '' or lower is None:
        upper = float(upper)
        temp = []
        for i in arg_sort_array:
            if float(ind_to_price[i]) > upper:
                continue
            else:
                temp.append(i)
                if len(temp) is 20:
                    arg_sort_array = temp
                    break
    elif upper is ''  or upper is None :
        lower = float(lower)
        temp = []
        for i in arg_sort_array:
            if float(ind_to_price[i]) < lower:
                continue
            else:
                temp.append(i)
                if len(temp) is 20:
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
                if len(temp) is 20:
                    arg_sort_array = temp
                    break

    asin_array = [asin_dic[i] for i in arg_sort_array]
    return ([ind_to_title[i] for i in arg_sort_array] , [ind_to_price[i] for i in arg_sort_array], [ind_to_rating[i] for i in arg_sort_array],[ind_to_url[i] for i in arg_sort_array],top_scores[:20],asin_array,[text_dic[j] for j in asin_array])
