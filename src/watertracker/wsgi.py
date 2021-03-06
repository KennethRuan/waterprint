"""
WSGI config for watertracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import string

REMOVE_PUNCTUATION_TABLE = str.maketrans({x: None for x in string.punctuation})
TOKENIZER = TreebankWordTokenizer()
STEMMER = PorterStemmer()


def tokenize_and_stem(s):
    return [STEMMER.stem(token) for token
            in TOKENIZER.tokenize(s.translate(REMOVE_PUNCTUATION_TABLE))]


data = pd.read_csv(r'crops.csv')
data2 = pd.read_csv(r'meats.csv')
df = pd.DataFrame(data)
df2 = pd.DataFrame(data2)
crops = df["Product description (HS)"].to_list()
avg = df["Global average"].to_list()
meats = df2["Product discription (HS)"].to_list()
avg2 = df2["Weighted average all"].to_list()
mp = {}
crops2 = []

for i in range(1, 1060, 3):
    tmp = re.sub(r"[^a-zA-Z0-9]+", " ", crops[i])
    " ".join(tmp.split())
    crops2.append(tmp)
    mp[tmp] = avg[i]+avg[i+1]+avg[i+2]

for i in range(0, 318, 3):
    tmp = re.sub(r"[^a-zA-Z0-9]+", " ", meats[i])
    crops2.append(tmp)
    mp[tmp] = avg2[i]+avg2[i+1]+avg2[i+2]

vectorizer = TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words='english')
vectorizer.fit(crops2)
crop_vectors = vectorizer.transform(crops2)


project_folder = os.path.expanduser('~/waterprint')
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watertracker.settings')

application = get_wsgi_application()
