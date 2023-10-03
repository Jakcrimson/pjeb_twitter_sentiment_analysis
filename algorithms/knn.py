class KNN():
    
    def __init__(self, data, tweet_a_categoriser, nombre_voisins, distance, vote):
        self.data = data
        self.tweet_a_categoriser = tweet_a_categoriser
        self.nombre_voisins = nombre_voisins
        self.distance = distance
        self.vote = vote
        
        
    def liste_distance(self):
        if self.distance == "naïve":
            distances = []
            mots_tweet = self.tweet_a_categoriser.split()
            nombre_de_mots_tweet = len(mots_tweet)
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
    
    def classification(self):
        if self.vote == "majoritaire":
            label_et_distance_proches_voisins_croissant = [(x,y) for (x,y) in zip(self.data["target"],self.liste_distance())]
            label_et_distance_proches_voisins_croissant.sort(key=lambda x: x[1])
            votes = {}
            votes["4"] = 0
            votes["2"] = 0
            votes["0"] = 0
            for i in range(0,self.nombre_voisins):
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
        