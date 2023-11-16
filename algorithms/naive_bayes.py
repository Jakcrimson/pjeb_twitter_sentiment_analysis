import numpy as np
from ast import literal_eval

class NaiveBayes():
    
    def __init__(self, data):
        self.data = data
        #self.variante1 = variante1
        #self.variante2 = variante2
        #self.variante3 = variante3
        self.p_0 = self.data["target"].value_counts()[0]/self.data.shape[0]
        
        self.p_2 = self.data["target"].value_counts()[2]/self.data.shape[0]
        self.p_4 = self.data["target"].value_counts()[4]/self.data.shape[0]
        self.dictionnaire_0, self.dictionnaire_2, self.dictionnaire_4 = self.dictionnaire()  
        
    def dictionnaire(self): # on crée le dictionnaire des mots et de leur occurence dans la database d'entraînement
        dictionnaire_0 = {}
        dictionnaire_2 = {}
        dictionnaire_4 = {}
        
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
        
        