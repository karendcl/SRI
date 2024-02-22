from process_docs import processed_docs
from fuzzy import FuzzyModel
from boolean_Model import BooleanModel

class Document:
    def __init__(self, name, content, author):
        self.name = name
        self.content = content
        self.author = author

def search(query, model):

    print(query)
    tokenized_docs = []
    vector_repr = []
    dictionary = {}
    vocabulary = []
    CompleteDocuments = []
    tokenized_docs, vector_repr, dictionary, vocabulary, CompleteDocuments = processed_docs()

    if model == 'fuzzy':
        docs = FuzzyModel(query, tokenized_docs)
    else:
        docs = BooleanModel(query, tokenized_docs, dictionary)

    return docs