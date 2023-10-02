import pandas as pd
import numpy as np
from ast import literal_eval


class NaiveClassification():
    def __init__(self, data) -> None:
        pos = []
        with open(r'D:\work\Lille Master ML\PJEB\source\algorithms\corpus\utf8_pos.txt',encoding='utf8') as f:
            pos.append(f.readlines())
        
        self.pos = pos[0][0].split(",")
        
        neg = []
        with open(r'D:\work\Lille Master ML\PJEB\source\algorithms\corpus\utf8_neg.txt', encoding='utf8') as f:
            neg.append(f.readlines())
        
        self.neg = neg[0][0].split(",")

        self.data = data

    
    def count_positives(self):

        count = []
        tokens = self.data['Tweet_no_stop'].tolist()

        for i in range(len(tokens)):
            token_par_phrase = literal_eval(tokens[i])
            ct = 0
            for token in token_par_phrase:
                if token in self.pos:
                    ct +=1
            count.append(ct)
        

        return count


            
    def count_negatives(self):
        count = []
        tokens = self.data['Tweet_no_stop'].tolist()

        for i in range(len(tokens)):
            token_par_phrase = literal_eval(tokens[i])
            ct = 0
            for token in token_par_phrase:
                if ' '+token+' ' in self.neg:
                    ct +=1
            count.append(ct)
        

        return count
    


    def classify(self):
        count_pos = self.count_positives()
        print(count_pos)
        count_neg = self.count_negatives()
        print(count_neg)

        naive_class = []
        for p, n in zip(count_pos, count_neg):
            if p > n:
                naive_class.append(4)
            elif n > p :
                naive_class.append(0)
            else:
                naive_class.append(2)

        self.data["naive_label"] = naive_class


    def get_classified(self):
        self.classify()
        return self.data
        

    
data = pd.read_csv(r'D:\work\Lille Master ML\PJEB\small_clean.csv', delimiter=",", quotechar='"')
nc = NaiveClassification(data)
test = nc.get_classified()
print(test)
