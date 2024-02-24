from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def Matrix_TFIDF(documents, metrics):
    if metrics:
        pkl_vect_name = 'vect_for_metrics.pkl'
        pkl_matrix_name = 'matrix_tfidf_for_metrics.pkl'
    else:
        pkl_vect_name = 'vect.pkl'
        pkl_matrix_name = 'matrix_tfidf.pkl'

    try:
        with open(pkl_vect_name, 'rb') as f:
            vectorizer = pickle.load(f)
        with open(pkl_matrix_name, 'rb') as f:
            matrix_tfidf = pickle.load(f)
        return vectorizer, matrix_tfidf
    except:
        docs = [' '.join(doc) for doc in documents]
        vectorizer = TfidfVectorizer()
        matrix_tfidf = vectorizer.fit_transform(docs)
        with open(pkl_vect_name, 'wb') as f:
            pickle.dump(vectorizer, f)
        with open(pkl_matrix_name, 'wb') as f:
            pickle.dump(matrix_tfidf, f)