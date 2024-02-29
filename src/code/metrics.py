import ir_datasets
from process_docs import processed_docs, processed_query
import pickle
from boolean_Model import BooleanModel
from fuzzy import FuzzyModel


def my_relevant_documents(query_id):
    '''
    This function returns the relevant documents for a given query

    :param query_id: int, the identifier of the query
    :return: list of strings, the identifiers of the relevant documents
    '''
    documents = []
    for qrel in Qrels:
        if query_id == qrel.query_id:
            documents.append(qrel.doc_id)
    
    return documents

def index_to_id(IntList):
    '''
    This function returns the identifiers of the documents given their indexes

    :param IntList: list of integers, the indexes of the documents
    :return: list of strings, the identifiers of the documents
    '''
    id_List = []
    for i in IntList:
        id_List.append(Docs[i].doc_id)

    return id_List


def Tp(recovered_documents, relevant_documents):
    '''
    Calculate the measure (True Positives)
    :param recovered_documents: (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
    :param relevant_documents: (list): Set of documents relevant to the query. Each document is defined by its identifier.
    :return: the number of true positives
    '''
    temp = 0
    for v in relevant_documents:
        if v in recovered_documents:
            temp += 1
    return temp


def Fp(recovered_documents, relevant_documents):
    '''
    Calculate the measure (False Positives)
    :param recovered_documents: (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
    :param relevant_documents: (list): Set of documents relevant to the query. Each document is defined by its identifier.
    :return: the number of false positives
    '''
    temp = 0
    for v in recovered_documents:
        if v not in relevant_documents:
            temp += 1
    return temp


def Fn(recovered_documents, relevant_documents):
    '''
    Calculate the measure (False Negatives)
    :param recovered_documents: (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
    :param relevant_documents: (list): Set of documents relevant to the query. Each document is defined by its identifier.
    :return: the number of false negatives
    '''
    temp = 0
    for v in relevant_documents:
        if v not in recovered_documents:
            temp += 1
    return temp


def Tn(recovered_documents, relevant_documents):
    '''
    Calculate the measure (True Negatives)
    :param recovered_documents: (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
    :param relevant_documents: (list): Set of documents relevant to the query. Each document is defined by its identifier.
    :return: the number of true negatives
    '''
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


def fb(recovered_documents, relevant_documents, b):
    """
    Calculate the measure(f)
  
    Args:
      - recovered_documents (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
      - relevant_documents (list): Set of relevant documents. Each document is defined by its identifier.
      - b (int): Number that represents the importance of accuracy or recall.
  
    Return:
      double: Value between 0 and 1.
  
    """

    p = r_accuracy(recovered_documents, relevant_documents, 30)
    r = recall(recovered_documents, relevant_documents)
    
    num = (1 + b ** 2) * p * r
    den = (b ** 2) * p + r
    if den == 0:
        return 0
    return num / den


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

def r_accuracy(recovered_documents, relevant_documents, r):
    """
    Calculate the measure
  
    Args:
      - recovered_documents (list): Set of documents recovered by the SRI. Each document is defined by its identifier.
      - relevant_documents (list): Set of relevant documents. Each document is defined by its identifier.
      - r (int): Ranking position to apply the cut
  
    Return:
      double: Value between 0 and 1.
  
    """
    
    return accuracy(recovered_documents[:r], relevant_documents)


def calculate_measures(model):
    '''
    This function calculates the measures for a given model
    :param model : (string) the name of the model to use
    :return: (tuple) the measures results {accuracy, recall, fb, f1, fallout, r_accuracy}
    '''
    accuracys = []
    recalls = []
    fbs = []
    f1s = []
    fallouts = []
    r_accuracys = []

    for i in range(len(Querys)):
        query = Querys[i]
        recovered_documents = []
        relevant_documents = my_relevant_documents(query.query_id)
        text_query = processed_query(query.text)
        
        if model == "fuzzy":
            recovered_documents = index_to_id(FuzzyModel(text_query, tokenized_docs))

        else:
            recovered_documents = index_to_id(BooleanModel(text_query, tokenized_docs, dictionary))

        current_accuracy = accuracy(recovered_documents, relevant_documents)
        current_recall = recall(recovered_documents, relevant_documents)
        current_fb = fb(recovered_documents, relevant_documents, 3)
        current_f1 = f1(recovered_documents, relevant_documents)
        current_fallout = fallout(recovered_documents, relevant_documents)
        current_r_accuracy = r_accuracy(recovered_documents, relevant_documents, 15)

        accuracys.append(current_accuracy)
        recalls.append(current_recall)
        fbs.append(current_fb)
        f1s.append(current_f1)
        fallouts.append(current_fallout)
        r_accuracys.append(current_r_accuracy)

    accuracy_media = sum(accuracys) / len(accuracys)
    recall_media = sum(recalls) / len(recalls)
    fb_media = sum(fbs) / len(fbs)
    f1_media = sum(f1s) / len(f1s)
    fallout_media = sum(fallouts) / len(fallouts)
    r_accuracy_media = sum(r_accuracys) / len(r_accuracys)

    return accuracy_media, recall_media, fb_media, f1_media, fallout_media, r_accuracy_media
    

def show_results():
    accuracy_value, recall_value, fb_value, f1_value, fallout_value, r_accuracy_value = calculate_measures("fuzzy")

    print("Fuzzy Boolean Model:")
    print("--------------------")
    print(f"Accuracy:  {accuracy_value}")
    print(f"Recall:    {recall_value}")
    print(f"fb:        {fb_value}")
    print(f"f1:        {f1_value}")
    print(f"Fallout:   {fallout_value}")
    print(f"R_Accuracy:{r_accuracy_value}")
    print("____________________")
    accuracy_value, recall_value, fb_value, f1_value, fallout_value, r_accuracy_value = calculate_measures("boolean")
    print("____________________")
    print("Boolean Model:")
    print("--------------------")
    print(f"Accuracy:  {accuracy_value}")
    print(f"Recall:    {recall_value}")
    print(f"fb:        {fb_value}")
    print(f"f1:        {f1_value}")
    print(f"Fallout:   {fallout_value}")
    print(f"R_Accuracy:{r_accuracy_value}")

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
    tokenized_docs, dictionary = processed_docs(Texts)

    with open('tokenized_docs_for_metrics.pkl', 'wb') as f:
        pickle.dump(tokenized_docs, f)
    with open('dictionary_for_metrics.pkl', 'wb') as f:
        pickle.dump(dictionary, f)

show_results()