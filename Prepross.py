import pandas as pd
import numpy as np
import re

## import matplotlib.pyplot as plt
def importData(filename):
    df = pd.read_csv(filename, encoding = "utf-8")
    fileName = "Datos\anime.csv"
    return df

#
def replace_foreign_characters(s):
    return re.sub(r'[^\x00-\x7f]',r'', s)

def extractYear(date):
    year = date[:4]
    if year.isnumeric():
        return int(year)
    else:
        return np.nan


def dropNoDevPub(df):
    idxNoNDP = df[(df['title'] == '')].index
    df.drop(idxNoNDP , inplace=True)
    df.reset_index(drop=True, inplace=True)
    idxNoNDP = df[(df['mediaType'] == '') & (df['studios'] == '')].index
    df.drop(idxNoNDP , inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

#Funcion que devuelve el valor de rating de un anime
def getRating(df):
    return df['rating']

#df = importData("Datos\anime.csv")
#Funcion para calcular la audiencia total de un anime
def totalAudience(row):
    posCount = row['watched']
    negCount = row['dropped']
    mCount = row['watching']
    WantCount = row['wantWatch']

    totalCount = posCount + negCount + mCount + WantCount
    return totalCount

#adding la nueva columna
def addTotalAudience(df):
    df['totalAudience'] = df.apply(totalAudience, axis=1)
    return df


# Function that computes the weighted rating of each game
def weighted_rating(x, m, C):
    v = x['rating']
    R = x['votes']
    # Calculation based on the IMDB formula
    return round((v/(v+m) * R) + (m/(m+v) * C), 2)

#Añadimos weighted rating
def addWeightedRating(df):
    # C is the mean vote across the whole report
    C = df['rating'].mean()
    # m is the minimum votes required to be listed in the chart
    m = df['votes'].quantile(0.90)
    # Filter out all qualified movies into a new DataFrame
    q_animes = df.copy().loc[df['votes'] >= m]
    # Calculate score using the IMDB formula
    q_animes['score'] = q_animes.apply(weighted_rating, args=(m, C), axis=1)
    # Sort movies based on score calculated above
    q_animes = q_animes.sort_values('score', ascending=False)
    return q_animes

def combine(x, colA, colB, colC):
    return x[colA] + ' ' + x[colB] + ' ' + x[colC]
def combine2(x, *features):
    result = ''
    # turn features to string  
    for f in features:
        result += str(x[f]) + ' '
    return result

#Formato de las columnas
def formatColumns(df):
    df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    df['title'] = df['title'].apply(lambda x: replace_foreign_characters(x))
    df['studios'] = df['studios'].str.replace(r'\[|\]|\'', '')
    df['studios'] = df['studios'].apply(lambda x: replace_foreign_characters(x))
    df['mediaType'] = df['mediaType'].apply(lambda x: replace_foreign_characters(x))
    #etiquetas para los generos
    df['contentWarn'] = df['contentWarn'].str.replace('[', '')
    df['contentWarn'] = df['contentWarn'].str.replace(']', '')

    df['tags'] = df['tags'].str.replace('[', '')
    df['tags'] = df['tags'].str.replace(']', '')

    
    df['title']= df['title'].str.strip()
    df['studios']= df['studios'].str.strip()
    df['mediaType']= df['mediaType'].str.strip()

    features = ['tags', 'contentWarn','votes', 'studios']

    df['merged'] = df.apply(combine2, axis=1, args = features)
    print(df['merged'].head())

# count the number of occurences for each tags in the data set

    counts = dict()
    # for each element in list (each row, split by ' ', in genres column)
    # we're splitting by space so tfidf can interpret the rows
    for i in df.index:
        for tag in df['merged'][i].split():
            if tag in counts:
                counts[tag] += 1
            else:
                counts[tag] = 1