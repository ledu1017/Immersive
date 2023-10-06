#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn import metrics

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


# # Load Dataset

# In[2]:


data = pd.read_csv('heart.csv')

data


# In[3]:


data.info()


# # Refine Dataset

# In[4]:


'''
sex                           RestingECG
M : 남성(0)                   Normal  : 0
F : 여성(1)                   ST      : 1
                              LVH     : 2
                              
ChestPainType                 ExerciseAngina
ATA : 0                       N : 0
NAP : 1                       Y : 1
ASY : 2
TA  : 3

ST_Slope
Up   : 2 
Flat : 1
Down : 0

'''
data['Sex'] = data['Sex'].map({'M': 0, 'F': 1})
data['ChestPainType'] = data['ChestPainType'].map({'ATA': 0, 'NAP': 1, 'ASY' : 2, 'TA' : 3})
data['RestingECG'] = data['RestingECG'].map({'Normal': 0, 'ST': 1, 'LVH' : 2})
data['ExerciseAngina'] = data['ExerciseAngina'].map({'N': 0, 'Y': 1})
data['ST_Slope'] = data['ST_Slope'].map({'Up': 2, 'Flat': 1, 'Down' : 0})

data.head()


# In[5]:


data.describe()


# In[6]:


counts = data['HeartDisease'].value_counts()

# 그래프 그리기
plt.figure(figsize=(6, 4))  # 그래프 크기 설정
plt.bar(['No Heart Disease', 'Heart Disease'], counts.values, color=['lightblue', 'pink'])  # 막대 그래프 생성
plt.xlabel('Diagnosis')  # x축 제목
plt.ylabel('Count')  # y축 제목
plt.title('Heart Disease Distribution')  # 그래프 제목
plt.show()  # 그래프 표시


# # Split Train and Test

# In[7]:


train, test = train_test_split(data, test_size=0.2, random_state=2023)

x_train = train.drop(['HeartDisease'], axis=1)
y_train = train.HeartDisease

x_test = test.drop(['HeartDisease'], axis=1)
y_test = test.HeartDisease

print(len(train), len(test))


# # SVM

# In[8]:


model = svm.SVC(gamma='scale')
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print('SVM: %.2f' % (metrics.accuracy_score(y_pred, y_test) * 100))


# # DecisionTreeClassifier

# In[9]:


model = DecisionTreeClassifier()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print('DecisionTreeClassifier: %.2f' % (metrics.accuracy_score(y_pred, y_test) * 100))


# # KneighborsClassifier

# In[10]:


model = KNeighborsClassifier()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print('KNeighborsClassifier: %.2f' % (metrics.accuracy_score(y_pred, y_test) * 100))


# # LogisticRegression

# In[11]:


model = LogisticRegression(solver='lbfgs', max_iter=2000)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print('LogisticRegression: %.2f' % (metrics.accuracy_score(y_pred, y_test) * 100))


# # RandomForestClassifier

# In[12]:


model = RandomForestClassifier(n_estimators=100)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print('RandomForestClassifier: %.2f' % (metrics.accuracy_score(y_pred, y_test) * 100))


# # Compute Feature Importances

# In[13]:


features = pd.Series(
    model.feature_importances_,
    index=x_train.columns
).sort_values(ascending=False)

print(features)


# # Extract Top 5 Features

# In[14]:


top_5_features = features.keys()[:5]

print(top_5_features)


# # SVM(TOP 5)

# In[15]:


model = svm.SVC(gamma='scale')
model.fit(x_train[top_5_features], y_train)

y_pred = model.predict(x_test[top_5_features])

print('SVM(Top 5): %.2f' % (metrics.accuracy_score(y_pred, y_test) * 100))


# # Cross Validaiton (Tedious)

# In[16]:


model = svm.SVC(gamma='scale')

cv = KFold(n_splits=3, shuffle=True, random_state=2023)

accs, scores = [], []

for train_index, test_index in cv.split(data[top_5_features]):
    x_train = data.iloc[train_index][top_5_features]
    y_train = data.iloc[train_index].HeartDisease
    
    x_test = data.iloc[test_index][top_5_features]
    y_test = data.iloc[test_index].HeartDisease

    model.fit(x_train, y_train)
    
    y_pred = model.predict(x_test)

    accs.append(metrics.accuracy_score(y_test, y_pred))

print(accs)


# # Cross Validation (Simple)

# In[17]:


model = svm.SVC(gamma='scale')

cv = KFold(n_splits=5, shuffle=True, random_state=2019)

accs = cross_val_score(model, data[top_5_features], data.HeartDisease, cv=cv)

print(accs)


# # Test All Models

# In[18]:


models = {
    'SVM': svm.SVC(gamma='scale'),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
    'KNeighborsClassifier': KNeighborsClassifier(),
    'LogisticRegression': LogisticRegression(solver='lbfgs', max_iter=2000),
    'RandomForestClassifier': RandomForestClassifier(n_estimators=100)
}

cv = KFold(n_splits=5, shuffle=True, random_state=2023)

for name, model in models.items():
    scores = cross_val_score(model, data[top_5_features], data.HeartDisease, cv=cv)
    
    print('%s: %.2f%%' % (name, np.mean(scores) * 100))


# # Normalize Dataset

# In[19]:


from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[top_5_features])

models = {
    'SVM': svm.SVC(gamma='scale'),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
    'KNeighborsClassifier': KNeighborsClassifier(),
    'LogisticRegression': LogisticRegression(solver='lbfgs', max_iter=2000),
    'RandomForestClassifier': RandomForestClassifier(n_estimators=100)
}

cv = KFold(n_splits=5, shuffle=True, random_state=2023)

for name, model in models.items():
    scores = cross_val_score(model, scaled_data, data.HeartDisease, cv=cv)
    
    print('%s: %.2f%%' % (name, np.mean(scores) * 100))


# In[20]:


from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[top_5_features])

models = {
    'SVM': svm.SVC(gamma='scale'),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
    'KNeighborsClassifier': KNeighborsClassifier(),
    'LogisticRegression': LogisticRegression(solver='lbfgs', max_iter=2000),
    'RandomForestClassifier': RandomForestClassifier(n_estimators=100)
}

cv = KFold(n_splits=5, shuffle=True, random_state=2018)

for name, model in models.items():
    scores = cross_val_score(model, scaled_data, data.HeartDisease, cv=cv)
    
    print('%s: %.2f%%' % (name, np.mean(scores) * 100))


# In[ ]:




