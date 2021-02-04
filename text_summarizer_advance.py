import nltk
import string
from nltk.corpus import stopwords
from heapq import nlargest
import speech_recognition as sr
import pyttsx3

# collecting stopwords and punctuations
punct=[]
stop_words=stopwords.words('english')
for i in string.punctuation:
    punct.append(i)

# prints the choices
while True:
    choice=int(input('1. Type the text or copy\paste it\n2. '
                     'Get text from .txt file\n3. Voice text\n\nEnter Text : '))
    if 0<choice<4:
        break
    else:
        print('enter a valid no.')


# gets the input text as per the above choice
def text_type(choice):
    """
    collects the text data as per the user's choice

    :param choice: int value between (1,2 or 3), means to get the text data
    :return: text data
    """

    if choice==1:
        print('If typing, press enter twice to get the summary. '
              'If copy pasting, make sure the paragraphs do not have spacing\n'
              'between them else the summary will not be correct\n\n'
              'Text here :\n')


        data=[]
        while True:
            text=input()
            if text=='':
                break
            data.append(text)
        data=' '.join(data)
        return data

    elif choice==2:
        data=[]
        path=input('enter path of .txt file : ')
        with open(path, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                data.append(line)
        data='. '.join(data)
        return data

    else:
        print("For voice text, do not speak the whole paragraph but only one or two lines.\n"
              "Then wait for the machine to say, 'next sentence'. When finished, say 'done'\n"
              "when it asks you for the next sentence")
        data=[]
        while True:
            r=sr.Recognizer()
            with sr.Microphone() as source :
                print('speak : ')
                audio=r.listen(source)

            try:

                your_text=r.recognize_google(audio)
                print('you said -',your_text)
                data.append(your_text)
                engine=pyttsx3.init('sapi5')
                voices=engine.getProperty('voices')
                engine.setProperty('voice',voices[0].id)
                engine.setProperty('rate',150)
                engine.say('next sentence')
                engine.runAndWait()

                if your_text=='done':
                    data='. '.join(data)
                    break

            except:
                print('sorry, did not get that')
                engine=pyttsx3.init('sapi5')
                voices=engine.getProperty('voices')
                engine.setProperty('voice',voices[0].id)
                engine.setProperty('rate',150)
                engine.say('sorry, did not get that')
                engine.runAndWait()

        return data




mytext=text_type(choice)

# tokenising words from text and removing punctuations and stopwords
def tokenise(text):
    tokens=nltk.word_tokenize(text.lower())
    tokens=[word for word in tokens if word not in punct]
    tokens=[word for word in tokens if word not in stop_words]
    return tokens

# writing the token frequency,
# i.e how many many times a word/token appeared in the text
# and the normalising the frequency by dividing each
# frequency with the max frequency
def token_frequency(text):
    tokens=tokenise(text)
    token_freq={}

    for word in tokens:
        if word not in token_freq.keys():
            token_freq[word]=1
        else:
            token_freq[word]+=1
    max_freq_key=max(token_freq,key=token_freq.get)
    for word in token_freq.keys():
        token_freq[word]=token_freq[word]/token_freq[max_freq_key]

    return token_freq

# tokenising sentences from the text
def tokenise_sent(text):
    tokens_sent=nltk.sent_tokenize(text)
    return tokens_sent

# getting the sentence scores
def sentence(text):

    sent_scores={}

    for sent in tokenise_sent(text):
        for word in nltk.word_tokenize(sent):
            if word.lower() in token_frequency(text).keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=token_frequency(text)[word.lower()]
                else:
                    sent_scores[sent]+=token_frequency(text)[word.lower()]

    return sent_scores

# summarising the text
def summarise(text):
    summ_size=int(len(tokenise_sent(text))*0.4)
    summary = nlargest(summ_size,sentence(text),key=sentence(text).get)
    summary = ' '+' '.join(summary)
    return summary

print('\nsummary - \n')
print(summarise(mytext))

# reading the summary verbally
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',150)
engine.say(summarise(mytext))
engine.runAndWait()
