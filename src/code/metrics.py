import ir_datasets
from process_docs import processed_docs
import pickle
from boolean_Model import BooleanModel
from fuzzy import FuzzyModel
from tfIdf_Matrix import Matrix_TFIDF

dataset = ir_datasets.load("vaswani")
Querys = [query for query in dataset.queries_iter()]
Qrels = [qrel for qrel in dataset.qrels_iter()]
Docs = [doc for doc in dataset.docs_iter()]
Texts = [doc.text for doc in dataset.docs_iter()]
tokenized_docs = []
dictionary = {}    

try:
    with open('tokenized_docs_for_metrics.pkl', 'rb') as f:
        tokenized_docs = pickle.load(f)
    with open('dictionary_for_metrics.pkl', 'rb') as f:
        dictionary = pickle.load(f)
except:
    tokenized_docs, vector_repr, dictionary, vocabulary = processed_docs(Texts)
    Matrix_TFIDF(tokenized_docs, True)
    with open('tokenized_docs_for_metrics.pkl', 'wb') as f:
        pickle.dump(tokenized_docs, f)
    with open('dictionary_for_metrics.pkl', 'wb') as f:
        pickle.dump(dictionary, f)

def my_relevant_documents(query_id):
    documents = []
    for qrel in Qrels:
        if query_id == qrel.query_id:
            documents.append(qrel.doc_id)
    
    return documents

def index_to_id(IntList):
    id_List = []
    for i in IntList:
        id_List.append(Docs[i].doc_id)

    return id_List


def Tp(recovered_documents, relevant_documents):
    temp = 0
    for v in relevant_documents:
        if v in recovered_documents:
            temp += 1
    return temp


def Fp(recovered_documents, relevant_documents):
    temp = 0
    for v in recovered_documents:
        if v not in relevant_documents:
            temp += 1
    return temp


def Fn(recovered_documents, relevant_documents):
    temp = 0
    for v in relevant_documents:
        if v not in recovered_documents:
            temp += 1
    return temp


def Tn(recovered_documents, relevant_documents):
    temp = 0
    for v in Docs:
        if v.doc_id not in recovered_documents and v not in relevant_documents:
            temp += 1
    return temp


def accuracy(recovered_documents, relevant_documents):
    """
    Calculate the measure (accuracy)
  
    Args:
      - recovered_documents (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
      - relevant_documents (list): Set of relevant documents. Each document is defined by its identifier.
  
    Return:
      double: Value between 0 and 1.
  
    """
    tp = Tp(recovered_documents, relevant_documents)
    fp = Fp(recovered_documents, relevant_documents)
    if(tp+fp == 0):
        return 0
    else:
        return tp / (tp + fp)


def recall(recovered_documents, relevant_documents):
    """
    Calculate the measure (recall)
  
    Args:
      - recovered_documents (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
      - relevant_documents (list): Set of relevant documents. Each document is defined by its identifier.
  
    Return:
      double: Value between 0 and 1.
  
    """
    tp = Tp(recovered_documents, relevant_documents)
    fn = Fn(recovered_documents, relevant_documents)

    return tp / (tp + fn)


def f1(recovered_documents, relevant_documents):
    """
    Calculate the measure (f1)
  
    Args:
      - recovered_documents (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
      - relevant_documents (list): Set of relevant documents. Each document is defined by its identifier.

    Return:
      double: Value between 0 and 1.
  
    """

    p = accuracy(recovered_documents, relevant_documents)
    r = recall(recovered_documents, relevant_documents)
    
    num = 2 * p * r
    den = p + r
    if den == 0:
        return 0
    else:
        return num / den


def fallout(recovered_documents, relevant_documents):
    """
    Calculate the measure (fallout)
  
    Args:
      - recovered_documents (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
      - relevant_documents (list): Set of relevant documents. Each document is defined by its identifier.
  
    Return:
      double: Value between 0 and 1.
  
    """
    fp = Fp(recovered_documents, relevant_documents)
    tn = Tn(recovered_documents, relevant_documents)
    
    return fp / (fp + tn)


def calculate_measures(model):
    accuracys = []
    recalls = []
    f1s = []
    fallouts = []

    for query in Querys:
    
        recovered_documents = []
        relevant_documents = my_relevant_documents(query.query_id)

        if model == "fuzzy":
            recovered_documents = FuzzyModel(query.text.lower(), tokenized_docs, True)

        else:
            print(query.text.lower())
            recovered_documents = BooleanModel(query.text.lower(), tokenized_docs, dictionary)

        current_accuracy = accuracy(recovered_documents, relevant_documents)
        current_recall = recall(recovered_documents, relevant_documents)
        current_f1 = f1(recovered_documents, relevant_documents)
        current_fallout = fallout(recovered_documents, relevant_documents)

        accuracys.append(current_accuracy)
        recalls.append(current_recall)
        f1s.append(current_f1)
        fallouts.append(current_fallout)

    accuracy_media = sum(accuracys) / len(accuracys)
    recall_media = sum(recalls) / len(recalls)
    f1_media = sum(f1s) / len(f1s)
    fallout_media = sum(fallouts) / len(fallouts)

    return accuracy_media, recall_media, f1_media, fallout_media
    

def show_results():
    accuracy_value, recall_value, f1_value, fallout_value = calculate_measures("boolean")

    print("Fuzzy Boolean Model:")
    print("--------------------")
    print(f"Accuracy: {accuracy_value}")
    print(f"Recall:   {recall_value}")
    print(f"f1:       {f1_value}")
    print(f"Fallout:  {fallout_value}")
    print("____________________")
    accuracy_value, recall_value, f1_value, fallout_value = calculate_measures("boolean")
    print("____________________")
    print("Boolean Model:")
    print("--------------------")
    print(f"Accuracy: {accuracy_value}")
    print(f"Recall:   {recall_value}")
    print(f"f1:       {f1_value}")
    print(f"Fallout:  {fallout_value}")
        
show_results()