import numpy as np 
import pandas as pd
movies = pd.read_csv("prjmcl\\CSV\\tmdb_5000_credits.csv")
credits = pd.read_csv("prjmcl\\CSV\\tmdb_5000_movies.csv")
print(movies.head(5))

movies = movies.merge(credits,on='title')

# Keeping important columns for recommendation
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew',"homepage"]]

movies.isnull().sum()

movies.dropna(inplace=True)

movies.isnull().sum()

movies.shape

# handle genres

movies.iloc[0]['genres']

import ast #for converting str to list

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L

movies['genres'] = movies['genres'].apply(convert)
movies.head()
#convert to string
movies['homepage']=movies['homepage'].apply(str)
# handle keywords
movies.iloc[0]['keywords']
movies['keywords'] = movies['keywords'].apply(convert)
movies.head()
movies.iloc[0]['cast']

# top 3 cast

def convert_cast(text):# top 3 cast
    L = []
    for i in ast.literal_eval(text):
        if len(L) < 3:
            L.append(i['name'])
    return L

movies['cast'] = movies['cast'].apply(convert_cast)
movies.head()

def fetch_director(text):#director
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

movies.head()

# handle overview (converting to list)

movies.iloc[0]['overview']

movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.sample(4)

movies.iloc[0]['overview']

def remove_space(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1
movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)

# Concatinate all
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.iloc[0]['tags']

new_df = movies[['movie_id','title','tags','homepage']]

new_df.head()

# Converting list to str
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df.head()

new_df.iloc[0]['tags']

# Converting to lower case
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

new_df.head()

new_df.iloc[0]['tags']

import nltk
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def stems(text):
    T = []
    
    for i in text.split():
        T.append(ps.stem(i))
    
    return " ".join(T)

new_df['tags'] = new_df['tags'].apply(stems)
new_df.iloc[0]['tags']  

#from sklearn.feature_extraction.text import TfidfVectorizer
#cv = TfidfVectorizer(stop_words='english',max_features=5000)
#vector = cv.fit_transform(new_df['tags'])

#vector=pd.DataFrame(vector.todense(),index=new_df["title"])
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vector = cv.fit_transform(new_df['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)
#similarity=pd.DataFrame(similarity,columns=new_df["title"],index=new_df["title"])
#new_df[new_df['title'] == 'The Lego Movie'].index[0]

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)
import pickle
pickle.dump(new_df,open('prjmcl\\artifacts\\movie_list.pkl','wb'))
pickle.dump(similarity,open('prjmcl\\artifacts\\similarity.pkl','wb'))