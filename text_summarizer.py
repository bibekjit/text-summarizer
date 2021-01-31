import nltk
import string
from nltk.corpus import stopwords

# reading the text file line by line and appending the lines in a list
data=[]
with open('sample_text.txt', 'r', encoding='utf8') as f:
    for line in f:
        line = line.strip()
        data.append(line)

# creating the text
text=' '.join(data)

# creating a list of punctuations
punct=[]
stop_words=stopwords.words('english')
for i in string.punctuation:
    punct.append(i)

# tokenising the words in 'text' and then removing
# the punctuations and stopwords
tokens=nltk.word_tokenize(text.lower())
tokens=[word for word in tokens if word not in punct]
tokens=[word for word in tokens if word not in stop_words]

token_freq={}

# calculating token frequency in 'text' for each tokenised word
for word in tokens:
    if word not in token_freq.keys():
        token_freq[word]=1
    else:
        token_freq[word]+=1

# normalizing token frequency
for word in token_freq.keys():
    token_freq[word]=token_freq[word]/12

# tokenising sentences
tokens_sent=nltk.sent_tokenize(text)

# calculating frequency of tokenised words in tokenised sentences
sent_scores={}

for sent in tokens_sent:
    for word in nltk.word_tokenize(sent):
        if word.lower() in token_freq.keys():
            if sent not in sent_scores.keys():
                sent_scores[sent]=token_freq[word.lower()]
            else:
                sent_scores[sent]+=token_freq[word.lower()]


from heapq import nlargest

# initiating summary size ( in this case, 40% of original text)
summary_size=int(len(tokens_sent)*0.4)

# creating the summary
summary=nlargest(summary_size,sent_scores,key=sent_scores.get)
print(' '+' '.join(summary))



