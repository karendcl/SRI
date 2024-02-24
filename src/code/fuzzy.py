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


def Similitud_MMM(query_ind, matrix_tfidf, doc_ind: int):

    co1 = 0.2
    co2 = 0.7

    cy1 = 0.8
    cy2 = 0.2

    min = inf
    max = -inf

    for i in query_ind:
        if matrix_tfidf[doc_ind, i] < min:
            min = matrix_tfidf[doc_ind, i]
        if matrix_tfidf[doc_ind, i] > max:
            max = matrix_tfidf[doc_ind, i]

    return co1 * min + co2 * max, cy1 * min + cy2 * max



def FuzzyModel(query, documents, metrics):

    vectorizer, matrix_tfidf = Matrix_TFIDF(metrics)

    query = query.split()
    query = [word for word in query if word in vectorizer.vocabulary_]
    indices = indices_of_words_from_query(query, vectorizer)

    print("Empecé similitud")
    scores = [Similitud_MMM(indices, matrix_tfidf, i) for i in range(len(documents))]
    print("terminé similitud")

    print('got scores')

    mean_score_doc = [sum(score) / len(score) for score in scores]

    #order the documents by the mean score and return the index of the documents
    ordered =  sorted(range(len(mean_score_doc)), key=lambda k: mean_score_doc[k], reverse=True)

    #return the indices of docs that have a score greater than 0
    return [i for i in ordered if mean_score_doc[i] > 0]

