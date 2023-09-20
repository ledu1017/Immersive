#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from scipy import stats
import tensorflow as tf
import seaborn as sns
from pylab import rcParams
from sklearn.model_selection import train_test_split
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers

# 시각화 라이브러리 설정
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set(style='whitegrid', palette='muted', font_scale=1.5)

rcParams['figure.figsize'] = 14, 8

# RANDOM_SEED와 LABELS 설정
RANDOM_SEED = 42
LABELS = ["Normal", "Fraud"]


# In[2]:


df = pd.read_csv('zezu.csv', encoding='cp949')


# In[3]:


df.shape    # 데이터 구성 확인


# In[4]:


df.isnull().values.any()    # 결측값 확인


# In[5]:


df    # 데이터 출력


# In[6]:


mean = np.mean(df['이용금액_전체'])    # 평균


# In[7]:


var = np.var(df['이용금액_전체'])    # 분산


# In[8]:


std = np.std(df['이용금액_전체'])     # 표준편차


# In[9]:


print(mean, var, std)


# In[10]:


q1 = df['이용금액_전체'].quantile(0.25)    # 이상치 구하기위한 공식
q2 = df['이용금액_전체'].quantile(0.5)
q3 = df['이용금액_전체'].quantile(0.75)
iqr = q3-q1


# In[11]:


weird_data = df['이용금액_전체'] > q3 + 1.5*iqr
df[weird_data]    # 이상치로 걸린 데이터


# In[12]:


outlier_idx = df[weird_data].index    # 이상치의 인덱스번호 저장


# In[13]:


for i in range(len(df)):
    if i in outlier_idx:
        df.loc[i, '이상'] = 1
    else:
        df.loc[i, '이상'] = 0


# In[14]:


count_classes = pd.value_counts(df['이상'], sort = True)
count_classes.plot(kind = 'bar', rot=0)
plt.title("Amount used")
plt.xticks(range(2), LABELS)
plt.xlabel("weird")
plt.ylabel("Frequency");


# In[15]:


frauds = df[df.이상 == 1]
normal = df[df.이상 == 0]
frauds.shape


# In[16]:


normal.shape


# In[17]:


frauds.describe()


# In[18]:


normal.describe()


# In[19]:


# Fraud 데이터와 Normal 데이터를 합치기
combined_data = pd.concat([frauds, normal])

# 그래프 생성
fig, ax = plt.subplots()

# Fraud 데이터를 빨간색으로 표시
ax.scatter(combined_data.이용건수_전체, combined_data.이용금액_전체, c=combined_data.index.map(lambda x: 'red' if x in frauds.index else 'blue'))

# 그래프 제목 설정
ax.set_title('Combined Fraud and Normal')

# x축, y축 레이블 설정
plt.xlabel('Number of uses')
plt.ylabel('Amount')

# 그래프 표시
plt.show()


# In[20]:


from sklearn.preprocessing import StandardScaler

#columns_to_keep = ['승인일자', '이용건수_전체', '이용금액_전체', '이상']
columns_to_keep = ['이용건수_전체', '이용금액_전체', '이상']
data = df[columns_to_keep]

data['이용건수_전체'] = StandardScaler().fit_transform(data['이용건수_전체'].values.reshape(-1, 1))
data['이용금액_전체'] = StandardScaler().fit_transform(data['이용건수_전체'].values.reshape(-1, 1))


# In[21]:


data


# In[22]:


X_train, X_test = train_test_split(data, test_size=0.2, random_state=RANDOM_SEED)
X_train = X_train[X_train.이상 == 0]
X_train = X_train.drop(['이상'], axis=1)
print('-'*15)
print('X_train')
print(X_train)
print('-'*15)
print()

y_test = X_test['이상']
X_test = X_test.drop(['이상'], axis=1)
print()
print('-'*15)
print('X_test')
print(X_test)
print('-'*15)
print()

X_train = X_train.values
X_test = X_test.values
print()
print('-'*15)
print(X_train.shape, X_test.shape)
print('-'*15)


# In[23]:


X_train


# In[24]:


input_dim = X_train.shape[1]
encoding_dim = 14

input_layer = Input(shape=(input_dim, ))

encoder = Dense(encoding_dim, activation="tanh", 
                activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)
decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)


# In[25]:


nb_epoch = 50
batch_size = 32
autoencoder.compile(optimizer='adam', 
                    loss='mean_squared_error', 
                    metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath="model.h5",
                               verbose=0,
                               save_best_only=True)
tensorboard = TensorBoard(log_dir='./logs',
                          histogram_freq=0,
                          write_graph=True,
                          write_images=True)
history = autoencoder.fit(X_train, X_train,
                    epochs=nb_epoch,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_data=(X_test, X_test),
                    verbose=1,
                    callbacks=[checkpointer, tensorboard]).history


# In[26]:


autoencoder = load_model('model.h5')


# In[27]:


plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right');


# In[28]:


import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler


# In[29]:


import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

# 모델 로드
model = keras.models.load_model('model.h5')

# 거래량과 거래비용 입력 (예시)
transaction_volume = np.array([230.0])  # 거래량 값 (숫자로 변환)
transaction_cost = np.array([8200.0])   # 거래비용 값 (숫자로 변환)

# 스케일링을 위한 객체 생성
scaler = StandardScaler()

# 스케일링을 학습 데이터의 통계 정보로 적용
scaler.fit(data[['이용건수_전체', '이용금액_전체']])

# 테스트 데이터에 스케일링 적용
scaled_test_data = scaler.transform(np.column_stack((transaction_volume, transaction_cost)))

# 모델을 사용하여 예측 수행
reconstructed_data = model.predict(scaled_test_data)

# 입력 데이터와 복원된 데이터 간의 차이 계산
reconstruction_error = np.mean(np.square(scaled_test_data - reconstructed_data))

# 임계값 설정 (필요한 경우 조정)
threshold = 0.1  # 이상치로 판단할 임계값

# 이상치 여부 확인
if reconstruction_error > threshold:
    print("입력 데이터는 이상치입니다.")
else:
    print("입력 데이터는 정상입니다.")


# In[ ]:




