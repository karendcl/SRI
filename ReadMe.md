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
 - Two different datasets were used, the 'Goodreads' dataset for the app and the 'vaswani' dataset for the evaluation of the models. The 'Goodreads' dataset is a dataset of books that contains metadata that facilitated the creation of an attractive visual interface, and the implementation of a recommendation system that will be explained later. On the other hand, it was necessary to use a dataset with predefined queries and qrels for the evaluation of the models, for which the 'vaswani' dataset from ir-dataset was chosen. This dataset contains around 11k summaries of articles on physics and 93 predefined queries in natural language. An advantage of using this dataset is the composition of its qrels, which only contain the relevant documents for each query, instead of assigning a different level of relevance to each document in the dataset.
 - The preprocessing of the corpus was done with the spacy library due to its efficiency. As can be seen, the preprocessing of the corpus used for the visual interface takes no more than 30 seconds. The preprocessing includes: Tokenization, noise reduction, removing stopwords, and morphological reduction using lemmatization. This preprocessing is also applied to the user's queries.
 

## How to run 
You can simply execute the `startup.sh` script to run the program. This script will install the required dependencies and run the program.

### Defining a query
Our queries are accepted in natural language. The user can input a query in the form of a sentence, and the program will process it to retrieve the documents that satisfy the query.

## Solution Implemented

As we have previously mentioned, we have implemented a boolean model with fuzzy logic

#### Boolean Model with fuzzy logic
This model is an extension of the boolean model, which uses fuzzy logic to retrieve documents that contain a set of words.
The fuzzy logic on a boolean model is based on the premise that a document can contain a word with a certain degree of membership, whereas in the pure
boolean model, a document either contains a word or not.
In this implementation, we use the TF-IDF values to calculate the degree of membership of a word in a document.
> #### TF-IDF
> The TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical measure that evaluates the importance of a word in a document.
> It is calculated by multiplying the term frequency (TF) and the inverse document frequency (IDF) of a word.
> The term frequency is the number of times a word appears in a document, and the inverse document frequency is the logarithm of the total number of documents divided by the number of documents that contain the word.


In order to determine whether a document is relevant to a query, we use the MMM(Mixed Min-Max) model.

> #### MMM Model
> As we have said before, in fuzzy-set theory, a word has a degree of membership in a document as opposed to the boolean model, where a word either belongs to a document or not.
> In MMM, each index term has a fuzzy set associated with it. 
> A document's weight with respect to an index term is considered to be the degree of membership of the document in the fuzzy set.
> More specifically, the MMM model uses the minimum and maximum degree of membership of a document in the fuzzy set of the index terms to determine the relevance of the document to the query.
> The MMM model is calculated as follows:
> - $$ d_{A \cap B} = min(d_A, d_B) $$
> - $$ d_{A \cup B} = max(d_A, d_B) $$
> - $$ d_{ \neg A} = -d_A $$
> 
> This means that the degree of membership of a document in the intersection of two index terms is the minimum of the degrees of membership of the document in the two index terms, and the degree of membership of a document in the union of two index terms is the maximum of the degrees of membership of the document in the two index terms.
> Hence, we can consider the $$ \cap $$ as an AND operator and the $$ \cup $$ as an OR operator.
> The negation of the degree of membership of a document in an index term is the opposite of the degree of membership of the document in the index term.
> 
> The MMM model tries to soften the Boolean operators by considering the query-document similarity to be a linear combination of the min and max weights.
> - $$ SIM (d, q_{or}) = c_{or1} \cdot max_{i=1}^{n} d_{i} + c_{or2} \cdot min_{i=1}^{n} d_{i} $$
> - $$ SIM (d, q_{and}) = c_{and1} \cdot max_{i=1}^{n} d_{i} + c_{and2} \cdot min_{i=1}^{n} d_{i} $$
> 
> Where $$ c_{or1} $$, $$ c_{or2} $$, $$ c_{and1} $$, and $$ c_{and2} $$ are constants that are used to adjust the weights of the min and max operators.
> 
> In our implementation, we take advantage of transforming our query to DNF (Disjunctive Normal Form) to calculate the weights of the min and max operators.


## Insufficiencies
 - The model implemented has very low accuracy results. 
 - The model does not compute the degree of relevance of the documents
retrieved, so it is not possible to order the documents by relevance. It only
determines if it is relevant or not.

  
## Results
We hereby present the results of the metrics implemented inorder to evaluate the performance of the models.
- accuracy: This metric is the proportion of relevant documents compared to irrelevant documents that are retrieved by the model. It is used to measure the relevance of the documents retrieved by the model.
- recall: This metric is the proportion of relevant documents that are retrieved by the model. It is used to measure the effectiveness of the model in retrieving relevant documents.
- fall-out: This metric is the proportion of irrelevant documents that are retrieved by the model. It is used to measure the effectiveness of the model in not retrieving irrelevant documents.
- fb (b=3): This metric is an indicator of the effectiveness of the model, taking into consideration the accuracy and recall. Setting b=3, the recall is given more importance.

**Results for both models:**

Metric | Boolean Model | Fuzzy Boolean Model
---    |---            |---
accuracy | 0.04 | 0.01
recall | 0.005 | 0.90
fall-out | 0.001 | 0.16
f3 | 0.005 | 0.25

> These results can be checked by running the metrics.py file from the 'code' folder. The results shown are the individual results per query averaged.

As we can see, the fuzzy model is much more effective than the boolean, but it still lacks in accuracy. The model always retrieves too much information; as can be seen in the recall,most of the relevant information is retrieved, but the low level in accuracy also shows that a lot of irrelevant information was retrieved. Even so, said percentage of irrelevant information retrieved is still low compared to the total irrelevant documents in the dataset, as can be seen in the fall-out.

It is important to say that the poor results of the boolean model are because the natural language queries from the dataset are relatively long and the model is unable to find a document that contains every single word, which means that for most queries from the dataset, the model did not retrieve any documents. Having said that, in other circumstances, the metrics from the boolean model would have been slightly better,but not superior to the fuzzy model.


## Document Recommendation
As an extra feature of the program, we have implemented a document recommendation system. 
This system is based on recommending the books that are most similar to the ones that are retrieved by the model selected.

This degree of similarity is based on a scoring system that takes into consideration the most relevant authors and genres of the search results.

The recommendations are from the documents in the corpus that were not recommended.

## Images
> ## Main Page + Results Page
> ![image](https://i.postimg.cc/LXkCkXX4/photo-5121144838987819819-y.jpg)

> ## Recommendations Page
> ![image](https://i.postimg.cc/qvMtXMJJ/photo-5120976085427792776-y.jpg)
> ![image](https://i.postimg.cc/Ghj8ys1g/photo-5120976085427792775-y.jpg)
