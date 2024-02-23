from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def TFIDF_first_time(documents):
    vectorizer = TfidfVectorizer()
    matrix_tfidf = vectorizer.fit_transform(documents)
    with open('vect.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    with open('matrix_tfidf.pkl', 'wb') as f:
        pickle.dump(matrix_tfidf, f)
    
    return vectorizer, matrix_tfidf

def Matrix_TFIDF(documents):
    try:
        with open('vect.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        with open('matrix_tfidf.pkl', 'rb') as f:
            matrix_tfidf = pickle.load(f)
        return vectorizer, matrix_tfidf
    except:
        vectorizer = TfidfVectorizer()
        matrix_tfidf = vectorizer.fit_transform(documents)
        with open('vect.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        with open('matrix_tfidf.pkl', 'wb') as f:
            pickle.dump(matrix_tfidf, f)
        return vectorizer, matrix_tfidf

def indices_of_words_from_query(query, vectorizer):
    return [vectorizer.vocabulary_[word] for word in query if word in vectorizer.vocabulary_]

from math import inf
def Similitud_MMM(query_ind, matrix_tfidf, doc_ind: int):
    print('similitud')

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



def FuzzyModel(query, documents):

    docs = [' '.join(doc) for doc in documents]

    vectorizer, matrix_tfidf = Matrix_TFIDF(docs)

    query = query.lower()
    query = query.split()
    query = [word for word in query if word in vectorizer.vocabulary_]
    indices = indices_of_words_from_query(query, vectorizer)

    scores = [Similitud_MMM(indices, matrix_tfidf, i) for i in range(len(documents))]

    mean_score_doc = [sum(score) / len(score) for score in scores]

    #order the documents by the mean score and return the index of the documents
    ordered =  sorted(range(len(mean_score_doc)), key=lambda k: mean_score_doc[k], reverse=True)

    #return the indices of docs that have a score greater than 0
    return [i for i in ordered if mean_score_doc[i] > 0]

