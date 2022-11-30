

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from fuzzywuzzy import fuzz

import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os 

