import pickle
import os

import numpy as np

import Vectorizer as vec
import text_preprocessing as prep
from flask import Flask, jsonify, request, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, Float
# from flask_marshmallow import Marshmallow
from text_preprocessing import clean
import os
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from flask_mail import Mail, Message
import re, html
from bert_model import get_predictions
from topic_model import get_topic



app = Flask(__name__)  # Declaring the flask APP
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)


def model_prediction(text):
    print(2)
    clean_text = clean(text)
    print(3)
    lst,sentiment_class = get_predictions(clean_text)
    print(6)
    topic = get_topic(clean_text)
    return lst,sentiment_class,topic


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('tweets.html')


@app.route('/tweets', methods=['POST', 'GET'])
def get_sentiment():

    if request.method == "POST":

        text = request.form["message"]
        lst,sentiment_class,topic = model_prediction(text)
        neg_sent, neu_sent, pos_sent = str(np.round_(lst[0],decimals=3)), str(np.round_(lst[1],decimals=3)), \
                                       str(np.round_(lst[2],decimals=3))
        jsonify(negative_percent=neg_sent, neutral_percent=neu_sent, positive_percent=pos_sent)

        return render_template('result.html',sentiment_class = sentiment_class,negative=neg_sent, neutral=neu_sent, positive=pos_sent,topic=topic)
    # else:
    #     return render_template("tweets.html")


if __name__ == '__main__':
    app.run(debug=True)
