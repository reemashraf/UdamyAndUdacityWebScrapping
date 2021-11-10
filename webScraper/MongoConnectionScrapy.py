#!/usr/bin/env python
# coding: utf-8

# # # By : REEM ASHRAF SALAH

# In[36]:


import pymongo
from pymongo import MongoClient

import pandas as pd
import re
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC,LinearSVC, SVR
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer,TfidfTransformer 
from sklearn.metrics import r2_score


# In[2]:


import nltk
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer

import string
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')


# In[5]:


client = MongoClient()
#point the client at mongo URI
client = MongoClient('localhost' , 27017)
#select database
db = client['coursesdb']
#select the collection within the database
udemy = db.udemy
#convert entire collection to Pandas dataframe
udemyData = pd.DataFrame(list(udemy.find()))
# select the collection within the database
udacity = db.udacity
#convert entire collection to Pandas dataframe
udacityData = pd.DataFrame(list(udacity.find()))


# In[6]:


udemyData.head(5)


# In[9]:


udacityData.head(5)


# In[10]:


print(udacityData.shape)
print(udemyData.shape)


# In[11]:


print(udacityData.isna().sum())

print("______________________________________________")

print(udemyData.isna().sum())


# In[12]:


udacityData.level.unique()


# In[13]:


pricesPerLevel = { '' : '$25',
                'beginner' : '$75' ,
                 'intermediate' :'$100' ,
                 'advanced' : '$120'}
prices = []
for level in udacityData['level']:
    prices.append(pricesPerLevel[level])
udacityData['price'] = prices


# In[14]:


udacityData.head(5)


# In[15]:


df = pd.concat([udemyData, udacityData])


# In[16]:


df


# In[17]:


df.isna().sum()


# In[18]:


df.drop(['id','_id','link','prerequisites','instructors','description'], inplace = True , axis = 1)


# In[19]:


df


# In[20]:


df['source'] = df['source'].replace({'udemy':1, 'udacity':2})
df


# In[21]:


df['level'] = df['level'].fillna(0)
df


# In[22]:


df['level'] = df['level'].replace({0:0, 'beginner':1, 'intermediate':2, 'advanced':3,"":4})
df


# In[23]:


df['level'].unique()


# In[24]:


df.isna().sum()


# In[ ]:





# In[27]:


df['title']


# In[28]:


stopwords = nltk.corpus.stopwords.words('english')
words = set(nltk.corpus.words.words())
lemmatizer = WordNetLemmatizer()


# In[29]:


df['title']= df['title'].str.replace(r'<[^<>]*>', '')
df['title']= df['title'].str.replace(r':','')
df['title']= df['title'].str.replace('[^a-zA-Z]',' ')

df['price'] = df['price'].str.replace(r'$','')
df['price'] = df['price'].astype(float)


# In[30]:


df['title']= df['title'].str.replace('[{}]'.format(string.punctuation), '')
df['title']= df['title'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))


# In[31]:


df


# In[32]:


X = df[['source','level']] 

#the column text contains textual data to extract features from.
y = df['price']

#this is the column we are learning to predict.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)


# In[33]:


X['level'].unique()


# In[34]:


models = []
models.append(("SVR",SVR()))
models.append(("RandomForest",RandomForestRegressor()))


# In[35]:


accuracy = []
names = []
for name,model in models:
    model.fit(X_train, y_train)
    y_pred_class = model.predict(X_test)    
    names.append(name)
    accuracy.append(r2_score(y_test, y_pred_class))

for i in range(len(names)):
    print("{} accuracy = {:.3f}".format(names[i],accuracy[i]))


# # Models accuracy is very bad as data is very noise and small .
# ## { Most of data is approximated manually ie Level , price}

# In[ ]:




