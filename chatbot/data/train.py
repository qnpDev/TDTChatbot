# Create folder "model" if not exist yet
from pathlib import Path
Path("./model").mkdir(parents=True, exist_ok=True)

from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.utils.np_utils import to_categorical

import tensorflow as tf
import keras
from tensorflow import keras
import pickle
import json
import re

patterns = {
	'[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
	'[đ]': 'd',
	'[èéẻẽẹêềếểễệ]': 'e',
	'[ìíỉĩị]': 'i',
	'[òóỏõọôồốổỗộơờớởỡợ]': 'o',
	'[ùúủũụưừứửữự]': 'u',
	'[ỳýỷỹỵ]': 'y'
}

stop_words = [
	'bạn', 
	'ban', 
	'anh', 
	'chị', 
	'chi', 
	'em', 
	'shop', 
	'bot', 
	'ad',
	'vậy',
	'vay',
	'nao',
	'nào',
	'phải không',
	'phai khong',
	'khong',
	'không',
	'gi',
	'gì'
	]

def convert_to_no_accents(text):
	output = text
	for regex, replace in patterns.items():
        #Re.sub() thay thế tất cả các kết quả khớp với regex có trong output bằng một nội dung replace và trả về output mới đã được sửa đổi
		output = re.sub(regex, replace, output)
		output = re.sub(regex.upper(), replace.upper(), output)
	return output

#Loading JSON Data
trains = {}
with open('chatbot/data/data.json', 'r', encoding='utf-8') as json_data:
	intents = json.load(json_data)
	for intent in intents['intents']:
		sentences = intent['patterns']
		trains[intent['tag']] = sentences

classes = {}
X_train = []
y_train = []
for i, (key, value) in enumerate(trains.items()):
    X_train += [word_tokenize(v, format="text") for v in value] + [convert_to_no_accents(v) for v in value]
    y_train += [i]*len(value)*2
    classes[i] = key

pickle.dump(classes, open("chatbot/model/classes.pkl", "wb"))
y_train = to_categorical(y_train)
vectorizer = TfidfVectorizer(lowercase=True, stop_words=stop_words)

# độ quan trọng của các từ trong x_train
X_train = vectorizer.fit_transform(X_train).toarray()
pickle.dump(vectorizer, open("chatbot/model/tfidf_vectorizer.pkl", "wb"))

# Model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(8, input_dim = X_train.shape[1] ))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Dense(len(y_train[0]), activation='softmax'))
callbacks = [
	keras.callbacks.ModelCheckpoint('chatbot/model/model.h5', save_best_only=True),
]
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=5000, batch_size=8, callbacks=callbacks)
model.save('chatbot/model/model.h5')