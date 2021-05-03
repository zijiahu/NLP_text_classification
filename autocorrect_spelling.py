# import autocorrect
# from autocorrect import Speller

# arr = ['I', "dont","eat", 'appple']

# spell = Speller()
# for word in arr:
#     correct = spell(word)
#     print(correct)


# ACKNOWLEDGMENT:
# the following code is from the link below:
# https://stackoverflow.com/questions/195010/how-can-i-split-multiple-joined-words/
import re
from collections import Counter

def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = Counter(words(open('big.txt').read()))  # 'big.txt' is from https://norvig.com/big.txt
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

result = viterbi_segment('relevantso')
print(result)
# p = re.compile("([a-z]+)|([A-Z]{1}[a-z]*)")