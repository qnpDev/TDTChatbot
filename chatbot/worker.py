from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from underthesea import word_tokenize
import numpy as np
import tensorflow as tf
import numpy
import random
import pickle
import json

with open('chatbot/data/data.json', 'r', encoding='utf-8') as json_data:
	intents = json.load(json_data)
classes = pickle.load(open("chatbot/model/classes.pkl", "rb"))
model = tf.keras.models.load_model('chatbot/model/model.h5')
model.summary()
vectorizer = pickle.load(open("chatbot/model/tfidf_vectorizer.pkl", "rb"))

class Worker:

    def predict_class(self, sentence):
        sentence = word_tokenize(sentence, format="text")
        results = model.predict(vectorizer.transform([sentence]).toarray())[0]
        results = numpy.array(results)
        idx = numpy.argsort(-results)[0]
        return classes[idx], results[idx]

    def get_response(self, msg):
        tag, pred = self.predict_class(msg)
        if pred < 0.5:
            tag = 'sorry'
        for i in intents['intents']:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        
        
class ApiChatbot(APIView):
    def post(self, request):
        msg = request.data['msg']
        res = Worker().get_response(msg)
        return Response({'success': True, 'data': res}, status=status.HTTP_200_OK) 

    def get(self, request):
        return Response({'success':False, 'msg':'use POST'}, status=status.HTTP_200_OK)
    
   