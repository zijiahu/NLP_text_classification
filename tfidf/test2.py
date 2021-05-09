import re
import csv
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
from autocorrect_spelling import autocorrect_misspelling, viterbi_segment

from sklearn.datasets import make_blobs  # new 


np.random.seed(500)

allwords = []

stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
            'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
            'onto','out','over','past','per','plus','since','till','to','under','until','up',\
            'via','vs','with','that','can','cannot','could','may','might','must',\
            'need','ought','shall','should','will','would','have','had','has','having','be',\
            'is','am','are','was','were','being','been','get','gets','got','gotten',\
            'getting','seem','seeming','seems','seemed',\
            'enough', 'both', 'all', 'your', 'those', 'this', 'these', \
            'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
            'its', 'his', 'her', 'every', 'either', 'each', 'any', 'another',\
            'an', 'a', 'just', 'mere', 'such', 'merely', 'right', 'no', 'not',\
            'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
            'most', 'less', 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
            'rather', 'somewhat', 'sufficiently', 'same', 'different', 'such',\
            'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
            'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
            'anything', 'anytime', 'anywhere', 'everybody', 'everyday',\
            'everyone', 'everyplace', 'everything', 'everywhere', 'whatever',\
            'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
            'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
            'you','your','yours','me','my','mine','I','we','us','much','and/or',
            'youre', 'i', 'youll', 'theyre', 'theyd', 'theyve', 'doesnt', 'wont',\
            'isnt', 'Im'
            ]

# df = pd.read_csv("500_Reddit_users_posts_labels.csv", skiprows=1, header=None, chunksize=10000)
df = pd.read_csv("Reddit_Cleaned.csv", skiprows=1, header=None, chunksize=10000)

header = True
for chunk in df:
    # print(chunk)
    chunk.rename(columns={0:'user_id'},inplace=True)
    chunk.rename(columns={1:'post'},inplace=True)
    chunk.rename(columns={2:'label'},inplace=True)

    ## data pre-processing
    # remove blank row
    chunk['post'].dropna(inplace=True)
    # lower case
    chunk['post'] = [entry.lower() for entry in chunk['post']]
    # tokenization
    chunk['post'] =  [word_tokenize(entry) for entry in chunk['post']]
    
    # separate multi-joined words
    new_post = []
    for entry in chunk['post']:
        new_entry = []
        for word in entry:
            if word not in allwords:
                result = viterbi_segment(word)
                for w in result :
                    new_entry.append(w)
                    allwords.append(w)
            else:
                new_entry.append(word)
        new_post.append(new_entry)
    chunk['post'] = new_post

    # stop words
    chunk['post'] = chunk['post'].apply(lambda x: [item for item in x if item not in stop_words])

    chunk.to_csv('final.csv', mode='a', header=True, index=False)
    header = False

Corpus = pd.read_csv("final.csv", index_col=0)
Corpus = Corpus.dropna()
# Corpus = Corpus.drop("user_id", axis=0)

# prepare train and test data set
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['post'], Corpus['label'], test_size=0.3, random_state=0)

# encoding the label to numerical values so that the model can understand
Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

# word vectorization - tfidf
Tfidf_vect = TfidfVectorizer(max_features=500000)
Tfidf_vect.fit(Corpus['post'])

# Train_X_Tfidf and Test_X_Tfidf now contain for each row a list of unique integer num and its associted importance as calculated by tfidf
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)
# if print: 1.row number of "Train_X_Tfidf" 2.unique integer num 3.score calculated by tfidf vectorizer

## SVM
# fit the training dataset on the classifier
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto', tol=0.002)
SVM.fit(Train_X_Tfidf, Train_Y)
# predict the labels on validation dataset
predictions_SVM = SVM.predict(Test_X_Tfidf)
# accuracy score
print("SVM Accuracy Score:", accuracy_score(predictions_SVM, Test_Y)*100)
print("SVM f1_score:", f1_score(predictions_SVM, Test_Y, average="macro"))
print("SVM Precision score:", precision_score(predictions_SVM, Test_Y, average="macro"))
print("SVM Recall score:", recall_score(predictions_SVM, Test_Y, average="macro"))

## Naive Bayes
# fit the training dataset on the NB classifier
Naive = naive_bayes.MultinomialNB()
Naive.fit(Train_X_Tfidf,Train_Y)
# predict the labels on validation dataset
predictions_NB = Naive.predict(Test_X_Tfidf)
# accuracy score
print("Naive Bayes Accuracy Score:", accuracy_score(predictions_NB, Test_Y)*100)



