import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

# from nltk.book import *
los = ['hello my name is', 'i am a person', 'am i alive', 'jokes on you person']
lon = [1, 0, 0, 1]
sorting = TfidfVectorizer()
logistic = LogisticRegression()
matrix = sorting.fit_transform(los)
matrix1 = logistic.fit(matrix, lon)
sentence = ['hello name is joke']
print(logistic.predict(sorting.transform(sentence)))
