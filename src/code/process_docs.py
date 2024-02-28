import nltk
import spacy
import gensim

def tokenization_spacy(texts):
    nlp = spacy.load("en_core_web_sm", enable=["lemmatizer"])
    return [[token for token in nlp(doc)] for doc in texts]


def remove_noise_spacy(tokenized_docs):
    return [[token for token in doc if token.is_alpha] for doc in tokenized_docs]


def remove_stopwords_spacy(tokenized_docs):
    stopwords = spacy.lang.en.stop_words.STOP_WORDS
    return [
    [token for token in doc if token.text not in stopwords] for doc in tokenized_docs]


def morphological_reduction_spacy(tokenized_docs, use_lemmatization=True):
    stemmer = nltk.stem.PorterStemmer()
    return [
    [token.lemma_ if use_lemmatization else stemmer.stem(token.text) for token in doc]
    for doc in tokenized_docs]


def processed_docs(Corpus):
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
    query = query.lower()
    Query = []
    Query.append(query)

    processed_Query = morphological_reduction_spacy(remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(Query))), True)

    return ' '.join(processed_Query[0])