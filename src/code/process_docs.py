import nltk
import spacy
import gensim

def tokenization_spacy(texts):
    '''
    This function is used to tokenize a list of documents using spacy

    Args:
        - texts: list of strings, the documents to tokenize

    Returns
        - list of lists of strings, the tokenized documents
    '''
    nlp = spacy.load("en_core_web_sm", enable=["lemmatizer"])
    return [[token for token in nlp(doc)] for doc in texts]


def remove_noise_spacy(tokenized_docs):
    '''
    This function is used to remove non-alphabetic tokens from a list of tokenized documents

    Args
        - tokenized_docs: list of lists of strings, the tokenized documents

    Returns
        - list of lists of strings, the tokenized documents without non-alphabetic tokens
    '''
    return [[token for token in doc if token.is_alpha] for doc in tokenized_docs]


def remove_stopwords_spacy(tokenized_docs):
    '''
    This function is used to remove stopwords from a list of tokenized documents

    Args:
        - tokenized_docs: list of lists of strings, the tokenized documents

    Returns:
        - list of lists of strings, the tokenized documents without stopwords
    '''
    stopwords = spacy.lang.en.stop_words.STOP_WORDS
    return [
    [token for token in doc if token.text not in stopwords] for doc in tokenized_docs]


def morphological_reduction_spacy(tokenized_docs, use_lemmatization=True):
    '''
    This function is used to reduce the words in a list of tokenized documents to their root form

    Args
        - tokenized_docs: list of lists of strings, the tokenized documents
        - use_lemmatization: boolean, if true, lemmatization is used, else stemming is used

    Returns:
        - list of lists of strings, the tokenized documents with the words reduced to their root form
    '''
    stemmer = nltk.stem.PorterStemmer()
    return [
    [token.lemma_ if use_lemmatization else stemmer.stem(token.text) for token in doc]
    for doc in tokenized_docs]


def processed_docs(Corpus):
    '''
    This function is used to process a list of documents

    Args:
        - Corpus: list of strings, the documents to process

    Returns:
        - list of lists of strings, the processed documents
        - gensim.corpora.Dictionary, the dictionary of the documents

    '''
    #Load corpus
    documents = []

    for doc in Corpus:
        CurrentDoc = doc.lower()
        documents.append(CurrentDoc)

    tokenized_docs = []
    dictionary = {}

    tokenized_docs = morphological_reduction_spacy(remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(documents))), True)
    dictionary = gensim.corpora.Dictionary(tokenized_docs)

    return tokenized_docs, dictionary

def processed_query(query):
    '''
    This function is used to process a query

    Args:
        - query: string, the query to process

    Returns
        - string, the processed query
    '''
    query = query.lower()
    Query = []
    Query.append(query)

    processed_Query = morphological_reduction_spacy(remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(Query))), True)

    return ' '.join(processed_Query[0])