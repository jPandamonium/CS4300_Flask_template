import json
import gzip
import pickle
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import linalg as LA
import re

def tokenize(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: Array
    """
    lowertext = text.lower()
    
    tokens = re.findall(r'[a-z]+', lowertext)
    return tokens



def unpickle(fileNames):
 	file = open(fileNames[0],'rb')
	index_to_vocab = pickle.load(file)
	file.close()
	file = open(fileNames[1],'rb')
	vocab_to_index = pickle.load(file)
	file.close()
	file = open(fileNames[2],'rb')
	ind_to_title = pickle.load(file)
	file.close()
	file = open(fileNames[3],'rb')
	ind_to_price = pickle.load(file)
	file.close()
	file = open(fileNames[4],'rb')
	ind_to_rating = pickle.load(file)
	file.close()
	file = open(fileNames[5],'rb')
	doc_by_vocab = pickle.load(file)
	file.close()
	return index_to_vocab, vocab_to_index,ind_to_title,ind_to_price,ind_to_rating,doc_by_vocab
n_feats = 5000

index_to_vocab, vocab_to_index,ind_to_title,ind_to_price, ind_to_rating, doc_by_vocab = unpickle(['ind_to_vocab.pickle','vocab_to_indx.pickle','ind_to_title.pickle',
                           'ind_to_price.pickle', 'ind_to_rating.pickle','doc_by_vocab.pickle'])



def vectorize_query(query):
    vector = np.empty(n_feats)
    for i in tokenize(query):
        if i in vocab_to_index:
            index = vocab_to_index[i]
            vector[index] += 1
    norm = LA.norm(vector)
    for i in vector:
        i = i/norm
    return vector



def get_sim(query, vec):
    return np.dot(query, vec )/(LA.norm(query)*LA.norm(vec))

def calc_sort (matrix,query ):
    vector = vectorize_query(query)
    res = np.empty(len(matrix))
    for i in (0,len(matrix)-1):
        score = get_sim(vector,matrix[i])
        res[i] = score
    arg_sort_array = np.argsort(res)[::-1][:5]
    return [ind_to_title[i] for i in arg_sort_array] , [ind_to_price[i] for i in arg_sort_array], [ind_to_rating[i] for i in arg_sort_array]
