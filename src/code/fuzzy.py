from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = None
matrix_tfidf = None
def Matrix_TFIDF(documents):
    '''
    This creates the TF-IDF matrix for the documents

    Args:
    documents: list of strings, the documents to create the matrix from

    Returns:
    vectorizer: TfidfVectorizer, the vectorizer used to create the matrix
    matrix_tfidf: sparse matrix, the TF-IDF matrix
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
    query: list of strings, the words in the query
    vectorizer: TfidfVectorizer, the vectorizer used to create the matrix

    Returns:
    list of integers, the indices of the words in the query that are in the vocabulary of the vectorizer
    '''
    return [vectorizer.vocabulary_[word] for word in query if word in vectorizer.vocabulary_]


def Paice_Similarity(query_ind, matrix_tfidf, doc_ind: int):
    '''
    This function calculates the Paice similarity between a query and a document.
    It is basically the sum of the TF-IDF values of the words in the query that are in the document

    Args:
    query_ind: list of integers, the indices of the words in the query that are in the vocabulary of the vectorizer
    matrix_tfidf: sparse matrix, the TF-IDF matrix
    doc_ind: integer, the index of the document

    Returns:
    double, the Paice similarity between the query and the document
    '''
    sum = 0
    for i in query_ind:
        sum += matrix_tfidf[doc_ind, i]
    return sum


def FuzzyModel(query, documents):
    '''
    This function is used to search for documents that satisfy a query according to a fuzzy evaluation

    Args:
    query: string, the query
    documents: list of strings, the documents to search in

    Returns:
    matching_documents: list of integers, the indexes of the documents that satisfy the query

    '''

    vectorizer, matrix_tfidf = Matrix_TFIDF(documents)

    query = query.split()
    query = [word for word in query if word in vectorizer.vocabulary_]
    indices = indices_of_words_from_query(query, vectorizer)

    scores = [Paice_Similarity(indices, matrix_tfidf, i) for i in range(len(documents))]

    #order the documents by the mean score and return the index of the documents
    ordered = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

    #return the indices of docs that have a score greater than 0
    return [i for i in ordered if scores[i] > 0]