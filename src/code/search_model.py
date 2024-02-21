from src.code.process_docs import process_docs
from src.code.fuzzy import FuzzyModel

class Document:
    def __init__(self, name, content, author):
        self.name = name
        self.content = content
        self.author = author
def search(query, model):
    documents = process_docs()

    if model == 'fuzzy':
        docs = FuzzyModel(query, documents)
    else:
        docs = BooleanModel(query, documents)

    # create a list of Document objects
    docs = [Document(doc, content, author) for doc, content, author in docs]
    return docs