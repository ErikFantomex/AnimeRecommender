import pandas as pd
import numpy as np
import re

#Activar ambiente
#.\my_env\Scripts\activate

#

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
    df['weighted_score'] = df.apply(weighted_rating, axis=1, args=(m, C))

    return df

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

    # count the number of occurences for each genre in the data set
    counts = dict()
    for i in df.index:
    #for each element in list (each row, split by ' ', in tags column)
    #-- we're splitting by space so tfidf can interpret the rows
        for g in df.loc[i,'tags'].split(' '):
        #if element is not in counts(dictionary of genres)
            if g not in counts:
                #give genre dictonary entry the value of 1
                counts[g] = 1
            else:
                #increase genre dictionary entry by 1
                counts[g] = counts[g] + 1
    #Test Genre Counts
    counts.keys()
    print(counts['Action'])
    return df