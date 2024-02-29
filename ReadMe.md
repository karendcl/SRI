# Information Retrieval Project

>Authors
> - [Karen D Cantero Lopez C411]()
> - [Luis A Rodriguez Otero C411]()

## Model Description

In this project, there are two main models that are implemented to solve the problem of information retrieval.

### Boolean Model
The first and simplest model is the boolean model, which is based on the boolean algebra. This model is used to retrieve
documents that contain a specific set of words. 
It converts the query into a boolean expression and then evaluates it to retrieve the documents that satisfy the expression.

### Boolean Model with fuzzy logic
The second model is an extension of the boolean model, which uses fuzzy logic to retrieve documents that contain a set of words.
The fuzzy logic on a boolean model is based on the premise that a document can contain a word with a certain degree of membership, whereas in the pure
boolean model, a document either contains a word or not.
This means that the fuzzy logic gives the boolean model a sense of 'softness'.

## Considerations taken into account

## How to run 
You can simply execute the `startup.sh` script to run the program. This script will install the required dependencies and run the program.

### Defining a query
Our queries are accepted in natural language. The user can input a query in the form of a sentence, and the program will process it to retrieve the documents that satisfy the query.

## Solution Implemented

As we have previously mentioned, we have implemented a boolean model with fuzzy logic

#### Boolean Model with fuzzy logic
The second model implemented is an extension of the boolean model, which uses fuzzy logic to retrieve documents that contain a set of words.
The fuzzy logic on a boolean model is based on the premise that a document can contain a word with a certain degree of membership, whereas in the pure
boolean model, a document either contains a word or not.
In this implementation, we use the TF-IDF values to calculate the degree of membership of a word in a document.
> #### TF-IDF
> The TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical measure that evaluates the importance of a word in a document.
> It is calculated by multiplying the term frequency (TF) and the inverse document frequency (IDF) of a word.
> The term frequency is the number of times a word appears in a document, and the inverse document frequency is the logarithm of the total number of documents divided by the number of documents that contain the word.


In order to give a score to a document based on a query, we use the Paice model.

> #### Paice Model
> The Paice model is a scoring system that takes into consideration all the weights of the words from the query in the document.
> The score is calculated by summing the weights of the words in the query that are present in the document.
> Because we are using the TF-IDF values to calculate the weights of the words, the score is a measure of the relevance of the document to the query.
> 
> We have chosen to implement the Paice model because of its simplicity and its effectiveness in scoring documents based on a query.


## Insufficiencies


## Results
We hereby present the results of the metrics implemented inorder to evaluate the performance of the models.
- r-precision: This metric is the precision of the first r documents retrieved by the model. It is used to measure the relevance of the documents retrieved by the model.
- recall: This metric is the proportion of relevant documents that are retrieved by the model. It is used to measure the effectiveness of the model in retrieving relevant documents.
- fall-out: This metric is the proportion of irrelevant documents that are retrieved by the model. It is used to measure the effectiveness of the model in not retrieving irrelevant documents.
- fallback: This metric is the proportion of relevant documents that are not retrieved by the model. It is used to measure the effectiveness of the model in retrieving relevant documents.



## Document Recommendation
As an extra feature of the program, we have implemented a document recommendation system. 
This system is based on recommending the books that are most similar to the ones that are retrieved by the model selected.

This degree of similarity is based on a scoring system that takes into consideration the most relevant authors and genres of the search results.

The recommendations are from the documents in the corpus that were not recommended.






 



