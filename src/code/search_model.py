from process_docs import processed_docs, processed_query
from fuzzy import FuzzyModel
from boolean_Model import BooleanModel
import pickle


def search(query, model, documents):
    '''
    This function is used to search for documents in the database that are related to a query

    Args:
        - query: string, the query
        - model: string, the model to use for the search (fuzzy or boolean)
        - documents: list of strings, the documents to search in

    Returns
        - list of integers, the indices of the documents that satisfy the query
    '''
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