import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import plotly.express as px
import neattext as ntx
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob
from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
)
from io import BytesIO
import base64
import dash.dependencies as dd

data = pd.read_csv("dataset/vaccination_tweets.csv")
data.head()

# Dropping Unnecessary data
pd.DataFrame(
    data.drop(
        columns={
            "id",
            "user_description",
            "user_created",
            "user_followers",
            "user_friends",
            "user_favourites",
            "user_verified",
            "source",
            "is_retweet",
        },
        inplace=True,
    )
)


# Data Cleaning
# using neattext lib.
data["clean_data"] = data["text"].apply(ntx.remove_hashtags)
data["clean_data"] = data["clean_data"].apply(ntx.remove_urls)
data["clean_data"] = data["clean_data"].apply(ntx.remove_userhandles)
data["clean_data"] = data["clean_data"].apply(ntx.remove_multiple_spaces)
data["clean_data"] = data["clean_data"].apply(ntx.remove_special_characters)

lemmatizer = WordNetLemmatizer()
# nltk.download("stopwords")
# nltk.download("wordnet")
stop_words = stopwords.words("english")

# Remove stopwords


def stopWords(tweet):
    clean_tweet = tweet
    clean_tweet = " ".join(
        word for word in clean_tweet.split() if word not in stop_words
    )
    clean_tweet = " ".join(lemmatizer.lemmatize(word)
                           for word in clean_tweet.split())
    return clean_tweet


# creating 'clean_data' column
data["clean_data"] = data["clean_data"].apply(lambda x: stopWords(x))


# Assigning Polarity
def blob_fun(text):
    senti = TextBlob(text)
    senti_polarity = senti.sentiment.polarity
    senti_subjectivity = senti.sentiment.subjectivity

    if senti_polarity > 0:
        res = "Positive"

    elif senti_polarity < 0:
        res = "Negative"

    elif senti_polarity == 0:
        res = "Neutral"

    result = {
        "polarity": senti_polarity,
        "subjectivity": senti_subjectivity,
        "sentiment": res,
    }

    return result


data["results"] = data["clean_data"].apply(blob_fun)
data = data.join(pd.json_normalize(data=data["results"]))
# reference for main.py callback
positive_tweet = data[data["sentiment"] == "Positive"]["clean_data"]
negative_tweet = data[data["sentiment"] == "Negative"]["clean_data"]
neutral_tweet = data[data["sentiment"] == "Neutral"]["clean_data"]
