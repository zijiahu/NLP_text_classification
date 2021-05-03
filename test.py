import csv
import re
import nltk
import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from autocorrect_spelling import *

filename = "500_Reddit_users_posts_labels.csv"
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# stop_words = set(stopwords.words("english"))
# print(stop_words)

# { user_id, {word, occurrence} }
users = {}
user = {}
all_words = [] # all valid words
# { user_id, {word, tfidf score} }
vectors = {}
vector = {}
total_posts = 0

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
            'you','your','yours','me','my','mine','I','we','us','much','and/or'
            ]


with open(filename) as f:
    reader = csv.reader(f)
    next(reader) # skip the first row (header)

    for row in reader:
        user_id = row[0]
        post = row[1]
        label = row[2]
        total_posts += 1
        user = {}
        
        p = re.compile("[a-zA-Z]+")
        # p = re.compile("([a-z]+)|([A-Z]{1}[a-z]*)")
        m = p.findall(post)

        for word in m:
            # check if this word is misspelled
            word = autocorrect_misspelling(word)

            # if this word is multiple words joined together, split it
            result = viterbi_segment(word.lower())
            for w in result:
                if w in stop_words: continue
                if w not in all_words: all_words.append(w)
                if w not in user:
                    user[w] = 1
                else:
                    user[w] += 1

            # if word in stop_words: continue

            # if word not in all_words: all_words.append(word)

            # if word not in user:
            #     user[word] = 1
            # else:
            #     user[word] += 1
            # print(word , ': ' , user[word])
        
        users[user_id] = user # add the frequency of every word in user_id's post to users


# calculating IDF:

# for each user-id, calculate its IDF score 
for user in users:
    # for each word in the post of user-id:
    for word in users[user]:
        # find NumberOfDocumentsContaining(word)
        occurrence = 0 # number of documents containing word
        for u in users:
            if user != u and word in users[u]:
                occurrence += 1
        
        # calculate the natural log of ( total_posts/NumberOfDocumentsContaining(word) )
        idf = math.log(total_posts/occurrence)
        tf = users[user][word]
        tfidf = idf * tf
        users[user][word] = tfidf

    for w in all_words:
        if w in users[user]:
            vector[w] = users[user][w]
        else:
            vector[w] = 0
    vectors[user] = vector
    vector = {}

for vector in vectors:
    for word in vectors[vector]:
        print(vector, ": ", word , ": ", vectors[vector][word])

 



