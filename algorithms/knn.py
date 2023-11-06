from ast import literal_eval
from algorithms.pytextdist.edit_distance import * #distances calculées à l'échelle du caractères
from algorithms.pytextdist.vector_similarity import * #distances calculées en vectorisant les chaînes de caractères.Ici en mots, mais configurable pour des n-grammes.
import pandas as pd

class KNN():
    
    def __init__(self, data, nombre_voisins, distance, vote):
        self.data = data
        self.nombre_voisins = nombre_voisins
        self.distance = distance
        self.vote = vote
        
        
    def liste_distance(self, tweet_a_categoriser):
        distances = []
        if self.distance == "naïve":
            mots_tweet = tweet_a_categoriser.split()
            nombre_de_mots_tweet = len(self.data["text"])
            for autre_tweet in self.data["text"]:
                mots_autre_tweet = autre_tweet.split()
                nombre_de_mots_autre_tweet = len(mots_autre_tweet)
                nombre_total_mots = nombre_de_mots_tweet + nombre_de_mots_autre_tweet

                mots_communs = set()
                for mot in mots_tweet:
                    if mot in mots_autre_tweet:
                        mots_communs.add(mot)

                nombre_mots_commun = len(mots_communs)
                distance_tweet = (nombre_total_mots - nombre_mots_commun)/nombre_total_mots
                distances.append(distance_tweet)
            return distances
        
        if self.distance == "levenshtein":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = levenshtein_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet) 
            return distances
        
        if self.distance == "lcs":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = lcs_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances

        if self.distance == "damerau_levenshtein":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = damerau_levenshtein_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances
        
        if self.distance == "hamming":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = hamming_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances
        
        if self.distance == "jaro":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = jaro_winkler_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances
            
        if self.distance == "cosine":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = cosine_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances
        
        if self.distance == "jaccard":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = jaccard_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances
        
        if self.distance == "sorensen_dice":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = sorensen_dice_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances

        if self.distance == "qgram_dice":
            for autre_tweet in self.data["Tweet_Tokenized"]:
                autre_tweet_temp = " ".join(autre_tweet)
                simi = qgram_similarity(tweet_a_categoriser,autre_tweet_temp)
                distance_tweet = 1 - simi
                distances.append(distance_tweet)
            return distances
        
    
    def classification(self, tweet_a_categoriser):
        label_et_distance_proches_voisins_croissant = [(x,y) for (x,y) in zip(self.data["target"],self.liste_distance(tweet_a_categoriser))]
        label_et_distance_proches_voisins_croissant.sort(key=lambda x: x[1])
        votes = {}
        votes["4"] = 0
        votes["2"] = 0
        votes["0"] = 0
            
        if self.vote == "majoritaire":
            for i in range(0,int(self.nombre_voisins)):
                if label_et_distance_proches_voisins_croissant[i][0] == 4:
                    votes["4"] += 1
                elif label_et_distance_proches_voisins_croissant[i][0] == 2:
                    votes["2"] += 1
                else:
                    votes["0"] += 1 
            # on sélectionne l'étiquette avec le maximum de votes
            label = ""
            vote_majoritaire = max(votes.values())
            for i in votes:
                if votes[i] == vote_majoritaire:
                    label = i #on prend en compte la dernière étiquette égale au max 
            return label
        
        if self.vote == "pondéré":
            for i in range(0,int(self.nombre_voisins)):
                if label_et_distance_proches_voisins_croissant[i][0] == 4:
                    votes["4"] += 1/((label_et_distance_proches_voisins_croissant[i][1])**2)
                    
                elif label_et_distance_proches_voisins_croissant[i][0] == 2:
                    votes["2"] += 1/((label_et_distance_proches_voisins_croissant[i][1])**2)
                else:
                    votes["0"] += 1/((label_et_distance_proches_voisins_croissant[i][1])**2)
            # on sélectionne l'étiquette avec le maximum de votes
            label = ""
            vote_majoritaire = max(votes.values())
            for i in votes:
                if votes[i] == vote_majoritaire:
                    label = i #on prend en compte la dernière étiquette égale au max 
            return label
            