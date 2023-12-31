import pandas as pd
import numpy as np
from ast import literal_eval


class NaiveClassification():

    """this class represents a naive classifies which will classify tweetw based on how many positive of negative words it contains.
        if |negatives| > |positives| :
            return 0 #overall negative tweet
        elif |negatives| < |positives|:
            return 4 #overall posiive tweet
        else:
            return 2 #overall neutral tweet
    """

    def __init__(self, data, single_input_classification=False) -> None:
        pos = []
        with open(r'algorithms/corpus/utf8_pos.txt',encoding='utf8') as f:
            pos.append(f.readlines())
        
        self.pos = pos[0][0].split(",")
        
        neg = []
        with open(r'algorithms/corpus/utf8_neg.txt', encoding='utf8') as f:
            neg.append(f.readlines())
        
        self.neg = neg[0][0].split(",")

        self.data = data
        self.sic = single_input_classification
    
    def count_positives(self):
        """this function counts the words that are in the tweet belonging to the positive corpus

        Returns:
            int : the number of positive words in the tweet 
        """
        count = []
        if self.sic:
            ct = 0
            tokens = self.data
            for i in range(len(tokens)):
                if ' '+tokens[i] in self.pos:
                    ct+=1
            return ct
        
        else:
            tokens = self.data['Tweet_no_stop'].tolist()

            for i in range(len(tokens)):
                token_par_phrase = literal_eval(str(tokens[i]))
                ct = 0
                for token in token_par_phrase:
                    if ' '+token in self.pos:
                        ct +=1
                count.append(ct)
            return count


            
    def count_negatives(self):
        """this function counts the words that are in the tweet belonging to the negative corpus

        Returns:
            int : the number of negative words in the tweet 
        """
        count = []
        if self.sic:
            ct = 0
            tokens = self.data
            for i in range(len(tokens)):
                if ' '+tokens[i] in self.neg:
                    ct+=1
            return ct
        
        else:
            tokens = self.data['Tweet_no_stop'].tolist()

            for i in range(len(tokens)):
                token_par_phrase = literal_eval(str(tokens[i]))
                ct = 0
                for token in token_par_phrase:
                    if ' '+token in self.neg:
                        ct +=1
                count.append(ct)
        

            return count
    


    def classify(self):
        """this function classifies the tweet based on how many positive/negative words it contains.
            the classification process is purely naive and based solely on the number of words.
        """
        count_pos = self.count_positives()
        count_neg = self.count_negatives()
        
        print(count_pos)
        print(count_neg)
        
        
        if self.sic:
            if count_neg>count_pos:
                return 0
            elif count_pos>count_neg:
                return 4
            else:
                return 2
        
        else:
            naive_class = []
            for p, n in zip(count_pos, count_neg):
                if p > n:
                    naive_class.append(4)
                elif n > p :
                    naive_class.append(0)
                else:
                    naive_class.append(2)
        
        
            self.data["model_class"] = naive_class


    def get_classified(self):
        """this function returns the dataset with the classification column added to it, purely practical

        Returns:
            df : updated dataframe
        """
        self.classify()
        if self.sic:
            return self.data[0]
        else:
            return self.data

    

        

    
# data = pd.read_csv(r'D:\work\Lille Master ML\PJEB\small_clean.csv', delimiter=",", quotechar='"')
# nc = NaiveClassification(data)
# test = nc.get_classified()
# print(test)
