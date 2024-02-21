from process_docs import processed_docs
from fuzzy import FuzzyModel

class Document:
    def __init__(self, name, content, author):
        self.name = name
        self.content = content
        self.author = author
def search(query, model):

    print(query)
    documents = processed_docs()

    if model == 'fuzzy':
        docs = FuzzyModel(query, documents)
    else:
        docs = BooleanModel(query, documents)

    # create a list of Document objects
    docs = [Document(doc, content, author) for doc, content, author in docs]
    return docs