import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

# 데이터 준비 (예제로 간단하게 구성)
title = []
position = []

with open('titles.txt', encoding = 'UTF-8') as f:
    for line in f:
        split_text = f.readline().split(',')
        title.append(split_text[0])
        position.append(int(split_text[1].strip()))

print(title)
print(position)
# 텍스트 토큰화
tokenizer = Tokenizer()
tokenizer.fit_on_texts(title)
total_words = len(tokenizer.word_index) + 1

# 시퀀스 생성 및 패딩
input_sequences = tokenizer.texts_to_sequences(title)
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='post')

# 모델 구성
model = Sequential()
model.add(Embedding(total_words, 64, input_length=max_sequence_len))
model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(32))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 모델 학습
model.fit(np.array(input_sequences), np.array(position), epochs=50)

# 예측
test_msg = ["다낭 가볼까?"]
test_seq = tokenizer.texts_to_sequences(test_msg)
test_seq = pad_sequences(test_seq, maxlen=max_sequence_len, padding='post')
prediction = model.predict(test_seq)
print("해외여행 확률:", prediction[0][0])
