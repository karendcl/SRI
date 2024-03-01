from sklearn.feature_extraction.text import TfidfVectorizer
from boolean_Model import query_to_dnf

vectorizer = None
matrix_tfidf = None
def Matrix_TFIDF(documents):
    '''
    This creates the TF-IDF matrix for the documents

    Args:
        - documents: list of strings, the documents to create the matrix from

    Returns:
        - vectorizer: TfidfVectorizer, the vectorizer used to create the matrix
        - matrix_tfidf: sparse matrix, the TF-IDF matrix
    '''
    global vectorizer, matrix_tfidf

    if matrix_tfidf is None or vectorizer is None:
        docs = [' '.join(doc) for doc in documents]
        vectorizer = TfidfVectorizer()
        matrix_tfidf = vectorizer.fit_transform(docs)
    else:
        pass

    return vectorizer, matrix_tfidf


def indices_of_words_from_query(query, vectorizer):
    '''
    This function returns the indices of the words in the query that are in the vocabulary of the vectorizer

    Args:
        - query: list of strings, the words in the query
        - vectorizer: TfidfVectorizer, the vectorizer used to create the matrix

    Returns:
        - list of integers, the indices of the words in the query that are in the vocabulary of the vectorizer
    '''
    return [vectorizer.vocabulary_[word] for word in query if word in vectorizer.vocabulary_]


# def Paice_Similarity(query_ind, matrix_tfidf, doc_ind: int):
def Paice_Similarity(Query, matrix_tfidf, doc_ind: int):
    '''
    This function calculates the Paice similarity between a query and a document.
    It is basically the sum of the TF-IDF values of the words in the query that are in the document

    Args:
        - query_ind: list of integers, the indices of the words in the query that are in the vocabulary of the vectorizer
        - matrix_tfidf: sparse matrix, the TF-IDF matrix
        - doc_ind: integer, the index of the document

    Returns:
        - double, the Paice similarity between the query and the document
    '''
    # sum = 0
    # for i in query_ind:
    #     sum += matrix_tfidf[doc_ind, i]
    # return sum


    cor1 = 0.4
    cor2 = 0.6

    cand1 = 0.3
    cand2 = 0.7

    terms = Query.split(' | ')

    or_scores = []

    # Función para verificar si un documento satisface una componente conjuntiva de la consulta

    for clause in terms:
            and_scores = []
            if clause[0] == '(':
                clause = clause[1:-1]
            clause_matched = True
            needed = clause.split(' & ')
            for i in needed:
                neg = False
                i = str(i)
                if i[0] == '~':
                    neg = True
                    i = i[1:]
                if i not in vectorizer.vocabulary_:
                    clause_matched = True if neg else False
                    continue
                i = vectorizer.vocabulary_[i]
                if neg:
                    and_scores.append(1 - matrix_tfidf[doc_ind, i])
                    clause_matched = False
                else:
                    and_scores.append(matrix_tfidf[doc_ind, i])

            if clause_matched is True:
                return 1
            else:
                or_scores.append(min(and_scores))

    return max(or_scores)




def FuzzyModel(query, documents):
    '''
    This function is used to search for documents that satisfy a query according to a fuzzy evaluation

    Args:
        - query: string, the query
        - documents: list of strings, the documents to search in

    Returns:
        - list of integers, the indexes of the documents that satisfy the query

    '''

    # query = query.split()
    # query = [word for word in query if word in vectorizer.vocabulary_]
    # indices = indices_of_words_from_query(query, vectorizer)

    query_dnf = query_to_dnf(query)
    if query_dnf == "error":
        return []

    Matrix_TFIDF(documents)
    query = str(query_dnf)

    scores = [Paice_Similarity(query, matrix_tfidf, i) for i in range(len(documents)]]
    # scores = [Paice_Similarity(indices, matrix_tfidf, i) for i in range(len(documents))]

    #order the documents by the mean score and return the index of the documents
    ordered = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

    #return the indices of docs that have a score greater than 0
    return [i for i in ordered if scores[i] > 0]