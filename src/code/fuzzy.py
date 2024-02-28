from sklearn.feature_extraction.text import TfidfVectorizer

def Matrix_TFIDF(documents):
    docs = [' '.join(doc) for doc in documents]
    vectorizer = TfidfVectorizer()
    matrix_tfidf = vectorizer.fit_transform(docs)

    return vectorizer, matrix_tfidf


def indices_of_words_from_query(query, vectorizer):
    return [vectorizer.vocabulary_[word] for word in query if word in vectorizer.vocabulary_]


def Paice_Similarity(query_ind, matrix_tfidf, doc_ind: int):
    sum = 0
    for i in query_ind:
        sum += matrix_tfidf[doc_ind, i]
    return sum


def FuzzyModel(query, documents):

    vectorizer, matrix_tfidf = Matrix_TFIDF(documents)

    query = query.split()
    query = [word for word in query if word in vectorizer.vocabulary_]
    indices = indices_of_words_from_query(query, vectorizer)

    scores = [Paice_Similarity(indices, matrix_tfidf, i) for i in range(len(documents))]

    #order the documents by the mean score and return the index of the documents
    ordered = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

    #return the indices of docs that have a score greater than 0
    return [i for i in ordered if scores[i] > 0]