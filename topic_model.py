import pickle as plk

import numpy

from text_preprocessing import clean
import gensim

import nltk as nt
from nltk.corpus import stopwords
nt.download('stopwords')
sw = stopwords.words( 'english' )
my_list = ['I','The',"b'It",'On']
sw = sw + my_list


def remove_stopwords(text):
    l = []
    for i in str(text).split():
        if i not in sw:
            l.append(i.strip('\'\"'))
    return l


with open('topic_model.pkl', 'rb') as f:
    model = plk.load(f)
f.close()

with open('dict.pkl', 'rb') as f:
    id2word = plk.load(f)
f.close


def get_topic(clean_text):
    tokens = remove_stopwords(clean_text)
    b = id2word.doc2bow(tokens)
    topic_list = model[b]
    n = []
    for i in topic_list:
        n.append(i[1])

    n = numpy.array(n)
    topic_array = n.argmax()
    topics = model.print_topic(topic_list[topic_array][0])
    l = topics.split('+')
    topic = []
    for i in l:
        index = i.find('*')
        topic.append(i[index + 1:])

    return topic[:5]

