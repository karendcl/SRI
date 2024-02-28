from process_docs import processed_docs, processed_query
from fuzzy import FuzzyModel
from boolean_Model import BooleanModel
import pickle

class Document:
    def __init__(self, name, content, author):
        self.name = name
        self.content = content
        self.author = author

def search(query, model, documents):
    query = processed_query(query)

    try:
        with open('tokenized_docs.pkl', 'rb') as f:
            tokenized_docs = pickle.load(f)
        with open('dictionary.pkl', 'rb') as f:
            dictionary = pickle.load(f)
    except:
        tokenized_docs, dictionary = processed_docs(documents)

        with open('tokenized_docs.pkl', 'wb') as f:
            pickle.dump(tokenized_docs, f)
        with open('dictionary.pkl', 'wb') as f:
            pickle.dump(dictionary, f)

    if model == 'fuzzy':
        docs = FuzzyModel(query, tokenized_docs)
    else:
        docs = BooleanModel(query, tokenized_docs, dictionary)

    return docs