
import Prepross
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from fuzzywuzzy import fuzz

import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="wdips-functions\wdips-creds.json"
#"wdips-functions\wdips-creds.json
# "

def matching_score(a,b):
   return fuzz.ratio(a,b)
   # exactly the same, the score becomes 100
def get_appid_from_index(df, index):
   return df[df.index == index]['appid'].values[0]

def get_title_year_from_index(df, index):
   return df[df.index == index]['startYr'].values[0]

def get_title_from_index(df, index):
   return df[df.index == index]['title'].values[0]

def get_index_from_title(df, title):
   return df[df.name == title].index.values[0]

def get_votes_from_index(df, index):
   return df[df.index == index]['votes'].values[0]

def get_weighted_score_from_index(df, index):
   return df[df.index == index]['weighted_score'].values[0]

def get_total_audience_from_index(df, index):
   return df[df.index == index]['totalAudience'].values[0]

def get_platform_from_index(df, index):
   return df[df.index == index]['mediaType'].values[0]