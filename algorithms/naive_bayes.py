from ast import literal_eval
import pandas as pd
import numpy as np
from collections import Counter

class NaiveBayes():
    
    def __init__(self, data, variante1, variante2, variante3):
        """
        variante1 : taper "fréquence" ou "présence"
        variante2 : mots sans importance (longueur<3), taper "avec" ou "sans"
        variante3 : taper "uni-gramme", "bi-gramme", "both"
        """
        self.data = data
        self.variante1 = variante1
        self.variante2 = variante2
        self.variante3 = variante3
        self.p_0 = self.data["target"].value_counts()[0]/self.data.shape[0]
        self.p_2 = self.data["target"].value_counts()[2]/self.data.shape[0]
        self.p_4 = self.data["target"].value_counts()[4]/self.data.shape[0]
        self.dictionnaire_0, self.dictionnaire_2, self.dictionnaire_4 = self.dictionnaire()  
        
    def dictionnaire(self): # on crée le dictionnaire des mots et de leur occurence dans la database d'entraînement
        dictionnaire_0 = {}
        dictionnaire_2 = {}
        dictionnaire_4 = {}
        
        
        if self.variante3 == "uni-gramme" or self.variante3 == "both":
            if self.variante2 == "avec":
                for i in range(0,self.data.shape[0]):
                    if self.data["target"][i] == 0:
                        for y in (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split(): #join et literal_eval pour transformer les series en liste de mot. Puis .split pour découper pour chaque mot
                            if y not in dictionnaire_0 : 
                                dictionnaire_0[y] = 1
                            else :
                                dictionnaire_0[y] += 1

                    if self.data["target"][i] == 2:
                        for y in (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split(): #join et literal_eval pour transformer les series en liste de mot. Puis .split pour découper pour chaque mot
                            if y not in dictionnaire_2 : 
                                dictionnaire_2[y] = 1
                            else :
                                dictionnaire_2[y] += 1

                    if self.data["target"][i] == 4:
                        for y in (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split(): #join et literal_eval pour transformer les series en liste de mot. Puis .split pour découper pour chaque mot
                            if y not in dictionnaire_4 : 
                                dictionnaire_4[y] = 1
                            else :
                                dictionnaire_4[y] += 1
                                
        
            if self.variante2 == "sans":
                for i in range(0,self.data.shape[0]):
                    if self.data["target"][i] == 0:
                        for y in (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split(): #join et literal_eval pour transformer les series en liste de mot. Puis .split pour découper pour chaque mot
                            if y not in dictionnaire_0 and len(y)>3 : 
                                dictionnaire_0[y] = 1
                            elif len(y)>3 :
                                dictionnaire_0[y] += 1

                    if self.data["target"][i] == 2:
                        for y in (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split(): #join et literal_eval pour transformer les series en liste de mot. Puis .split pour découper pour chaque mot
                            if y not in dictionnaire_2 and len(y)>3  : 
                                dictionnaire_2[y] = 1
                            elif len(y)>3  :
                                dictionnaire_2[y] += 1

                    if self.data["target"][i] == 4:
                        for y in (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split(): #join et literal_eval pour transformer les series en liste de mot. Puis .split pour découper pour chaque mot
                            if y not in dictionnaire_4 and len(y)>3 : 
                                dictionnaire_4[y] = 1
                            elif len(y)>3  :
                                dictionnaire_4[y] += 1
                                
                                
        if self.variante3 == "bi-gramme" or self.variante3 == "both":
            if self.variante2 == "avec":
                for i in range(0,self.data.shape[0]):
                    if self.data["target"][i] == 0:
                        mots = (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split()
                        for y in range(0,len(mots)-1):
                            if mots[y]+" "+mots[y+1] not in dictionnaire_0 : 
                                dictionnaire_0[mots[y]+" "+mots[y+1]] = 1
                            else :
                                dictionnaire_0[mots[y]+" "+mots[y+1]] += 1


                    if self.data["target"][i] == 2:
                        mots = (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split()
                        for y in range(0,len(mots)-1):
                            if mots[y]+" "+mots[y+1] not in dictionnaire_2 : 
                                dictionnaire_2[mots[y]+" "+mots[y+1]] = 1
                            else :
                                dictionnaire_2[mots[y]+" "+mots[y+1]] += 1

                    if self.data["target"][i] == 4:
                        mots = (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split()
                        for y in range(0,len(mots)-1):
                            if mots[y]+" "+mots[y+1] not in dictionnaire_4 : 
                                dictionnaire_4[mots[y]+" "+mots[y+1]] = 1
                            else :
                                dictionnaire_4[mots[y]+" "+mots[y+1]] += 1
                                
        
            if self.variante2 == "sans":
                for i in range(0,self.data.shape[0]):
                    if self.data["target"][i] == 0:
                        mots = (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split()
                        for y in range(0,len(mots)-1):
                            if mots[y]+" "+mots[y+1] not in dictionnaire_0 and len(mots[y])>3 and len(mots[y+1])>3: 
                                dictionnaire_0[mots[y]+" "+mots[y+1]] = 1
                            elif len(mots[y])>3 and len(mots[y+1])>3:
                                dictionnaire_0[mots[y]+" "+mots[y+1]] += 1


                    if self.data["target"][i] == 2:
                        mots = (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split()
                        for y in range(0,len(mots)-1):
                            if mots[y]+" "+mots[y+1] not in dictionnaire_2 and len(mots[y])>3 and len(mots[y+1])>3: 
                                dictionnaire_2[mots[y]+" "+mots[y+1]] = 1
                            elif len(mots[y])>3 and len(mots[y+1])>3:
                                dictionnaire_2[mots[y]+" "+mots[y+1]] += 1

                    if self.data["target"][i] == 4:
                        mots = (" ".join(literal_eval(self.data["Tweet_Tokenized"][i]))).split()
                        for y in range(0,len(mots)-1):
                            if mots[y]+" "+mots[y+1] not in dictionnaire_4 and len(mots[y])>3 and len(mots[y+1])>3: 
                                dictionnaire_4[mots[y]+" "+mots[y+1]] = 1
                            elif len(mots[y])>3 and len(mots[y+1])>3:
                                dictionnaire_4[mots[y]+" "+mots[y+1]] += 1


        return dictionnaire_0,dictionnaire_2,dictionnaire_4

                        
    def classification(self, tweet_a_categoriser, single_input_classification=False):
        mots_tweet_a_categoriser = tweet_a_categoriser.split()
        n_0 = np.array(list(self.dictionnaire_0.values())).sum() # nombre de mot contenus dans les tweets 0
        n_2 = np.array(list(self.dictionnaire_2.values())).sum() # nombre de mot contenus dans les tweets 2
        n_4 = np.array(list(self.dictionnaire_4.values())).sum() # nombre de mot contenus dans les tweets 4
        N = n_0 + n_2 + n_4
        n_0_N = n_0 + N
        n_2_N = n_2 + N
        n_4_N = n_4 + N
        
        n_t_0 = 1
        n_t_2 = 1
        n_t_4 = 1
        p_t_0 = 1
        p_t_2 = 1
        p_t_4 = 1
        
        if self.variante1 == "présence":
            
            for i in mots_tweet_a_categoriser:
                if i in self.dictionnaire_0: 
                    n_t_0 = (self.dictionnaire_0[i] + 1)
                else:
                    n_t_0 = 1
                p_t_0 *= n_t_0/n_0_N


                if i in self.dictionnaire_2: 
                    n_t_2 = (self.dictionnaire_2[i] + 1)
                else:
                    n_t_2 = 1
                p_t_2 *= n_t_2/n_2_N


                if i in self.dictionnaire_4: 
                    n_t_4 = (self.dictionnaire_4[i] + 1)
                else:
                    n_t_4 = 1
                p_t_4 *= n_t_4/n_4_N
        
        
        if self.variante1 == "fréquence":
            occurence_mots_tweet = Counter(mots_tweet_a_categoriser)
            
            for i in occurence_mots_tweet:
                if i in self.dictionnaire_0: 
                    n_t_0 = (self.dictionnaire_0[i] + 1)
                else:
                    n_t_0 = 1
                p_t_0 *= (n_t_0/n_0_N) * occurence_mots_tweet[i]


                if i in self.dictionnaire_2: 
                    n_t_2 = (self.dictionnaire_2[i] + 1)
                else:
                    n_t_2 = 1
                p_t_2 *= (n_t_2/n_2_N) * occurence_mots_tweet[i]


                if i in self.dictionnaire_4: 
                    n_t_4 = (self.dictionnaire_4[i] + 1)
                else:
                    n_t_4 = 1
                p_t_4 *= (n_t_4/n_4_N) * occurence_mots_tweet[i]


        p_0_t = p_t_0 * self.p_0
        p_2_t = p_t_2 * self.p_2
        p_4_t = p_t_4 * self.p_4

        probas = [p_0_t, p_2_t, p_4_t]
        labels = [0, 2, 4]

        label_pred = labels[probas.index(max(probas))]

        if (single_input_classification):
            return label_pred
        else:
            return label_pred