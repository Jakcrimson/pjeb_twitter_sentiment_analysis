import re
import pandas as pd
import html
import string
from nltk.tokenize import TweetTokenizer
import nltk
import csv
#


class Csv_Cleaner():

    def __init__(self, pathfile) -> None:
        self.data = pd.read_csv(pathfile, header=0)
        self.data.columns = ["target", "ids", "date", "flag", "user", "text"]
        print("csv cleaner init pass")


    def remove_punct(self, text):
        z  = "".join([char for char in text if char not in string.punctuation])
        x = re.sub('[0-9]+', "", z)
        return x

    def link_process(self, text):
        x = re.sub(r"http\S+", "", text)
        x = re.sub(r"https\S+", "", text)
        return x

    def username_process(self, text):
        x = re.sub('@[\w]+',"",text)
        return x

    def rt_process(self, text):
        x = re.sub(r"RT", "", text)
        return x

    def punc_process(self, text):
        x = re.sub(r" / ( [ ! \ ? \ . ; , ] ) /" , "" , text)
        return x

    def pct_process(self, text):
        x = re.sub(r" /([0-9]{1 ,2}\% ) /" , "XX\%" ,text)
        return x 

    def dollar_process(self, text):
        x = re.sub(r"[\€]{1}[\d,]+\.?\d{0,2}","XX$",text)
        z = re.sub(r"[\$]{1}[\d,]+\.?\d{0,2}","XX€",x)
        return z

    def tokenization(self, text):
        text = re.split('\W+', text)
        return text

    def remove_stopwords(self, text):
        stopword = nltk.corpus.stopwords.words('english')
        text = [word for word in text if word not in stopword]
        return text


    def clean(self, data):
        tk = TweetTokenizer()

        self.data["text"] = self.data["text"].apply(lambda x:self.username_process(x))
        self.data["text"] = self.data["text"].apply(lambda x:self.rt_process(x))
        self.data["text"] = self.data["text"].apply(lambda x:self.link_process(x))
        self.data["text"] = self.data["text"].apply(lambda x:self.dollar_process(x))
        self.data["text"] = self.data["text"].apply(lambda x:self.pct_process(x))
        self.data["text"] = self.data["text"].apply(lambda x:self.punc_process(x))

        self.data["Tweet_Tokenized"] = self.data["text"].apply(lambda x:self.tokenization(x))
        self.data["Tweet_no_stop"] = self.data["Tweet_Tokenized"].apply(lambda x:self.remove_stopwords(x))

        self.data = self.data.drop("date", axis=1)
        self.data = self.data.drop("flag", axis=1)
        self.data = self.data.drop("user", axis=1)  
        self.data = self.data.drop("text", axis=1)
        return self.data
