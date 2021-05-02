import csv
import re
import nltk
import ssl
from nltk.tokenize import sent_tokenize, word_tokenize

filename = "500_Reddit_users_posts_labels.csv"

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
nltk.download('punkt')

# { user_id, {word, occurrence} }
users = {}
user = {}
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
    next(reader) # skip the first row
    for row in reader:
        user_id = row[0]
        post = row[1]
        label = row[2]
        total_posts += 1
        
        p = re.compile("[a-zA-Z]+")
        m = p.findall(post)

        for word in m:
            if word in stop_words: continue
            if word not in user:
                user[word] = 1
            else:
                user[word] += 1
            # print(word , ': ' , user[word])
        
        users[user_id] = user # add the frequency of every word in user_id's post to users


# calculating IDF:

# for each user-id, calculate its IDF score 
for user in users:
    # for each word in the post of user-id:
    for word in users[user]:
        # find NumberOfDocumentsContaining(word)

        # calculate the natural log of ( total_posts/NumberOfDocumentsContaining(word) )
 

    


