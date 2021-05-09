import autocorrect
import re
from collections import Counter
from autocorrect import Speller
import os


def autocorrect_misspelling(word):
    spell = Speller()
    correct = spell(word)
    return correct


# ACKNOWLEDGMENT:
# the following code is from the link below:
# https://stackoverflow.com/questions/195010/how-can-i-split-multiple-joined-words/
def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        # print("prob_k: " , prob_k)
        # print("k: " , k)
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    # return words, probs[-1]
    return words

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower()) 

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

dictionary = Counter(words(open('./big.txt').read()))  # 'big.txt' is from https://norvig.com/big.txt
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

result = viterbi_segment('supportiveOkay'.lower())
print(result)
print(autocorrect_misspelling("thnking"))