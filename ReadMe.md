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
 - Se utilizaron 2 datasets, el datadet (insertar nombre) para la aplicacion y el dataset 'vaswani' para la evaluacion de los modelo. El dataset (insertar nombre) es un dataset de (descripción) el cual contiene metadatos que nos facilitaban crear una interfaf visual atractiva, y la implementación de un sistema de recomendacion que se explicará mas adelante. Por otro lado era necesario un dataset con querys y qrels predefinidas para la evaluacion de los modelos, para lo cual se eligio el dataset 'vaswani', de ir-dataset. Este dataset contiene alrededor de 11 resumenes sobre articulos sobre física y 93 querys predefinidas en lenguaje natural. Una ventaja de usar este dataset es la composicion de sus qrels, los cuales solo contienen para cada query los documentos relevantes, en vez de asignar un nivel de relevancia distinto a cada documento del dataset.

 - A la hora de elegir las métricas se eligio la r-precision por encima de la precision ya que el modelo implementado devuelve los resultados en orden de prioridad, por lo que tiene mas sentido analizar los primeros r documentos elegidos por este. Elegimos r=15 pues es el equivalente a las primeras 5 páginas de resultados en la interfaz visual, es poco probable que el usuario busque resultados mas allá de estos.

 - El preprocesamiento del corpus se hizo con la biblioteca spacy debido a la eficiencia de esta. como se puede comprobar, el preprocesamiento del corpus utilizado para la interfaz visual tarda no mas de 30 segundos. El preprocesamiento incluye: Tokenizacion, reduccion de ruido, quitar las stopwords y la reducciom morfológica utilizando la lematizacion. Este preprocesamiento tambien es aplicado a las querys del usuario.

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
- r-accuracy (r=15): This metric is the accuracy of the first r documents retrieved by the model. It is used to measure the relevance of the documents retrieved by the model.
- recall: This metric is the proportion of relevant documents that are retrieved by the model. It is used to measure the effectiveness of the model in retrieving relevant documents.
- fall-out: This metric is the proportion of irrelevant documents that are retrieved by the model. It is used to measure the effectiveness of the model in not retrieving irrelevant documents.
- fb (b=3): This metric is an indicator of the effectiveness of the model, taking into consideration the accuracy and recall. Setting b=3, the recall is given more importance.

**Results for both models:**

Metric | Boolean Model | Fuzzy Boolean Model
---    |---            |---
r-accuracy | 0.04 | 0.18
recall | 0.003 | 0.91
fall-out | 0.0 | 0.17
f3 | 0.007 | 0.5

> These results can be checked by running the metrics.py file from the 'code' folder. The results shown are the individual results per query averaged.

As we can see, the fuzzy model is much more effective than the boolean, but it still lacks in accuracy. The model always retrieves too much information; as can be seen in the recall,most of the relevant information is retrieved, but the low level in accuracy also shows that a lot of irrelevant information was retrieved. Even so, said percentage of irrelevant information retrieved is still low compared to the total irrelevant documents in the dataset, as can be seen in the fall-out.

It is important to say that the poor results of the boolean model are because the natural language queries from the dataset are relatively long and the model is unable to find a document that contains every single word, which means that for most queries from the dataset, the model did not retrieve any documents. Having said that, in other circumstances, the metrics from the boolean model would have been slightly better,but not superior to the fuzzy model.


## Document Recommendation
As an extra feature of the program, we have implemented a document recommendation system. 
This system is based on recommending the books that are most similar to the ones that are retrieved by the model selected.

This degree of similarity is based on a scoring system that takes into consideration the most relevant authors and genres of the search results.

The recommendations are from the documents in the corpus that were not recommended.
