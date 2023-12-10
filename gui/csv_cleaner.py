import re
import pandas as pd
import html
import string
from nltk.tokenize import TweetTokenizer
import nltk
import csv
#



class Csv_Cleaner():
    """
    This class is used to clean a tweet. It processes various forms of text and tokenizes a tweet in order for it to be properly processed by
    classification models.
    """
    def __init__(self, pathfile=None, is_single_input=False, single_input=None) -> None:
        """Initialize the class

        Args:
            pathfile (string, optional): path to the csv file containing various tweets Defaults to None.
            is_single_input (bool, optional): if the user decides to clean a single tweet. Defaults to False.
            single_input (string, optional): if is_single_input is set to true, then this parameter has the value of the raw tweet. Defaults to None.
        """
        self.is_single_input = is_single_input
        if is_single_input == True:
            self.data = single_input
        else:
            self.data = pd.read_csv(pathfile, on_bad_lines="skip", sep=";")
            self.data.columns = ["target", "ids", "date", "flag", "user", "text"]
            print("csv cleaner init pass")


    def link_process(self, text):
        """Removes any links of form https:// or http:// etc.

        Args:
            text (str): text to be modified

        Returns:
            str: the text with no links
        """
        x = re.sub(r"http\S+", "", text)
        x = re.sub(r"https\S+", "", text)
        return x

    def username_process(self, text):
        """Removes any usernames or @s in the tweet

        Args:
            text (str): text to be modified

        Returns:
            str: the text with no usernames
        """
        x = re.sub('@[\w]+',"",text)
        return x

    def rt_process(self, text):
        """Removes the re-tweet syntax integrated into the tweet

        Args:
            text (str): text to be modified

        Returns:
            str: the text with no RT syntax
        """
        x = re.sub(r"RT", "", text)
        return x

    def punc_process(self, text):
        """Removes punctuation characters from the text

        Args:
            text (str): text to be modified

        Returns:
            str: the text with no punctuation characters
        """
        x = re.sub(r" / ( [ ! \ ? \ . ; , ] ) /" , "" , text)
        return x

    def pct_process(self, text):
        """Modifies any number% characters in the tweet and replaces them by XX%, the value of the percentage is not relevant in the classification.

        Args:
            text (str): text to be modified

        Returns:
            str: the text with modified % values
        """
        x = re.sub(r" /([0-9]{1 ,2}\% ) /" , "XX\%" ,text)
        return x 

    def dollar_process(self, text):
        """Modifies any number$ characters in the tweet and replaces them by XX$, the value of the price/equity is not relevant in the classification.

        Args:
            text (str): text to be modified

        Returns:
            str: the text with modified $ values
        """
        x = re.sub(r"[\€]{1}[\d,]+\.?\d{0,2}","XX$",text)
        z = re.sub(r"[\$]{1}[\d,]+\.?\d{0,2}","XX€",x)
        return z

    def tokenization(self, text):
        """Tokenizes the text given in parameter.
        FYI : Tokenization is a process that transforms a sentence into an array of independant words (eg. "hello, my name is Pierre" -> ["hello", ",", "my", "name", "is", "Pierre"])

        Args:
            text (str): text to be modified

        Returns:
            str: the tokenized text
        """
        text = re.split('\W+', text)
        return text

    def remove_stopwords(self, text):
        """Removes stopwords from the token array previously made with func tokenization.
        FYI : a stopwod is a linkage word (eg. 'is', 'my', 'the', 'but' etc...)
        Args:
            text (str): text to be modified

        Returns:
            str: the tokenized text without stopwords
        """
        stopword = nltk.corpus.stopwords.words('english')
        text = [word for word in text if word not in stopword]
        return text


    def clean(self):
        """Cleans the attribute self.data which is a dataframe is the user is not in a single input context.

        Returns:
            pd.dataframe or string: the cleaned dataset or string
        """
        if self.is_single_input == False:
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
        
        else :
            self.data = self.username_process(self.data)
            self.data = self.rt_process(self.data)
            self.data = self.link_process(self.data)
            self.data = self.dollar_process(self.data)
            self.data = self.pct_process(self.data)
            self.data = self.punc_process(self.data)
            self.data = self.tokenization(self.data)
            self.data = self.remove_stopwords(self.data)
            print(self.data)
            return self.data

