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

def give_weight(documents):
    '''
    Give each word of the corpus a weight based on its relevance (tfidf)
    The weight is continuous between 0 and 1

    Parameters
    documents: list of strings

    Returns
    dict: word: weight
    '''

    vectorizer, matrix_tfidf = TFIDF_first_time(documents)

    weights: list[dict] = []
    for doc in range(len(documents)):
        weights.append(dict(zip(vectorizer.get_feature_names_out(), matrix_tfidf.toarray()[doc])))

    return weights

def Similitud_MMM(query, pesos):

    co1 = 0.2
    co2 = 0.7

    cy1 = 0.8
    cy2 = 0.2

    sim_o = max(pesos[term] for term in query.split())
    sim_y = min(pesos[term] for term in query.split())

    return co1*sim_o + co2*sim_y, cy1*sim_o + cy2*sim_y


def FuzzyModel(query, documents):

    docs = [' '.join(doc) for doc in documents]

    pesos = give_weight(docs)
    scores = [Similitud_MMM(query, peso) for peso in pesos]

    mean_score_doc = [sum(score) / len(score) for score in scores]

    #order the documents by the mean score and return the index of the documents
    return sorted(range(len(mean_score_doc)), key=lambda k: mean_score_doc[k], reverse=True)




doc1 = ['the', 'cat', 'in', 'the', 'hat']
doc2 = ['the', 'cat', 'in', 'the', 'tree']
doc3 = ['the', 'dog', 'in', 'the', 'hat']
doc4 = ['this', 'is', 'a', 'test', 'document']
doc5 = ['the', 'cat', 'in', 'the', 'hat', 'and', 'the', 'tree', 'tree']
query = 'the cat in the tree'

print(FuzzyModel(query, [doc1, doc2, doc3, doc4, doc5]))