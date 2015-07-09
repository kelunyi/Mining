__author__ = 'Shengnuo'
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import  MultinomialNB
import pickle

def desc_to_words(desc):
    words = re.sub("[^a-zA-z0-9]"," ",desc).split()
    stops = set(nltk.corpus.stopwords.words('english'))
    meaning_ful = [w for w in words if w not in stops]
    return (" ".join(meaning_ful))

def classify(desc):
    desc_features = vectorizer.transform([desc_to_words(desc)]).toarray()
    clf2 = pickle.loads(s)
    return clf2.predict(desc_features)[0]


if __name__ == '__main__':
    pass
else:

    engine = create_engine('mysql://root:genghiskhan@localhost/job_database')
    train = pd.read_sql('SELECT * from job_table ', engine, index_col='URL', )

    num_jobs = train["Description"].size
    clean_train_desc = []

    for i in xrange(0, num_jobs):
        clean_train_desc.append(desc_to_words(train["Description"][i]))

    vectorizer = CountVectorizer(analyzer="word")
    train_data_features = vectorizer.fit_transform(clean_train_desc).toarray()
    clf = MultinomialNB(alpha=0.01)

    clf.fit(train_data_features[:],train["Difficulty"][:])
    s = pickle.dumps(clf)
