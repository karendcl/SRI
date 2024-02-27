from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from math import inf

def Matrix_TFIDF(metrics):
    if metrics:
        pkl_vect_name = 'vect_for_metrics.pkl'
        pkl_matrix_name = 'matrix_tfidf_for_metrics.pkl'
    else:
        pkl_vect_name = 'vect.pkl'
        pkl_matrix_name = 'matrix_tfidf.pkl'

    with open(pkl_vect_name, 'rb') as f:
        vectorizer = pickle.load(f)
    with open(pkl_matrix_name, 'rb') as f:
        matrix_tfidf = pickle.load(f)

    return vectorizer, matrix_tfidf


def indices_of_words_from_query(query, vectorizer):
    return [vectorizer.vocabulary_[word] for word in query if word in vectorizer.vocabulary_]


def Similitud_Paice(query_ind, matrix_tfidf, doc_ind: int):
    sum = 0
    for i in query_ind:
        sum += matrix_tfidf[doc_ind, i]
    return sum



def FuzzyModel(query, documents, metrics):

    vectorizer, matrix_tfidf = Matrix_TFIDF(metrics)

    query = query.split()
    query = [word for word in query if word in vectorizer.vocabulary_]
    indices = indices_of_words_from_query(query, vectorizer)

    scores = [Similitud_Paice(indices, matrix_tfidf, i) for i in range(len(documents))]

    #order the documents by the mean score and return the index of the documents
    ordered = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

    #return the indices of docs that have a score greater than 0
    return [i for i in ordered if scores[i] > 0.2]