import pandas as pd
import numpy as np

from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import customtkinter as ctk
ctk.set_appearance_mode("dark") 
  
ctk.set_default_color_theme("blue") 

class Metrics(Frame):
    """
    This class is used to get a baseline on model performances, during the project we will only use the error rate and the accuracy.
    if time allows it, further metrics will be implemented, such ac f1-score , OA (overall accuracy) and AUC (area under ROC curve).
    """
    def __init__(self, classified_dataset, parent, model):
        """initializes the window that will display the metrics

        Args:
            classified_dataset (pd.dataframe): a dataset containing a column 'target' (label) and a column 'model_class' (prediction)
            parent (tkinter frame): the main app
            model (str): name of the model that classified the data
        """

        self.classified_dataset = classified_dataset
        self.parent = parent
        self.model = model

    def display(self, mean_cv_score=None, train=True):
        new= ctk.CTkToplevel(master=self.parent)
        new.geometry("400x600")
        new.title("Metrics")
        
        my_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")

        if train==True:
            ctk.CTkLabel(new, text = "Mean CV Accuracy", font=my_font).pack(pady=30)
            ctk.CTkLabel(new, text=f"{mean_cv_score}").pack(pady=20, padx=10)
        else:
            ctk.CTkLabel(new, text=self.model, font=my_font)
            ctk.CTkLabel(new, text="Accuracy", font=my_font).pack(pady=30)
            ctk.CTkLabel(new, text=self.get_accuracy()).pack(pady=20, padx=10)
            
            ctk.CTkLabel(new,text="Error Rate", font=my_font).pack(pady=30)
            ctk.CTkLabel(new, text=self.get_error_rate()).pack(pady=20, padx=10)

            
        ctk.CTkButton(new, text="Exit", command=new.destroy).pack(pady=10)  
        self.wait_window(new)
    

    def get_accuracy(self):
    
        """
        Function to calculate accuracy
        -> param y_true: list of true values
        -> param y_pred: list of predicted values
        -> return: accuracy score
        
        """
        
        # Intitializing variable to store count of correctly predicted classes
        y_true = self.classified_dataset["target"].values
        y_pred = self.classified_dataset["model_class"].values
        correct_predictions = 0
        
        for yt, yp in zip(y_true, y_pred):
            
            if yt == yp:
                
                correct_predictions += 1
        
        #returns accuracy
        return correct_predictions / len(y_true)
    


    def get_error_rate(self):
        """Function to compute the error rate.

        Returns:
            float: the error rate
        """

        # Intitializing variable to store count of correctly predicted classes
        y_true = self.classified_dataset["target"].values
        y_pred = self.classified_dataset["model_class"].values
        correct_predictions = 0
        incorrect_predictions = 0
        for yt, yp in zip(y_true, y_pred):
            
            if yt == yp:
                
                correct_predictions += 1
            else:
                incorrect_predictions +=1
        
        #returns accuracy
        return 1-(correct_predictions / len(y_true))


    def get_cross_validation_dataset(self):
        data = self.classified_dataset
        k = 10
        fold_size = len(data) // k
        indices = np.arange(len(data))
        folds = []
        for i in range(k):
            test_indices = indices[i * fold_size: (i + 1) * fold_size]
            train_indices = np.concatenate([indices[:i * fold_size], indices[(i + 1) * fold_size:]])
            folds.append((train_indices, test_indices))
        return folds
    

    def get_cross_validation_score(self):
        # Initialize a list to store the evaluation scores
        fold_indices = self.get_cross_validation_dataset()
        scores = []
        for train_indices, test_indices in fold_indices:
            self.classified_dataset = self.classified_dataset[train_indices]
            
            # Calculate the accuracy score for this fold
            fold_score = self.get_accuracy()
            
            # Append the fold score to the list of scores
            scores.append(fold_score)

        # Calculate the mean accuracy across all folds
        mean_accuracy = np.mean(scores)
        return [scores, mean_accuracy]



    # Functions to compute True Positives, True Negatives, False Positives and False Negatives

    def true_positive(self,y_true, y_pred):
        
        tp = 0
        
        for yt, yp in zip(y_true, y_pred):
            
            if yt == 1 and yp == 1:
                tp += 1
        
        return tp

    def true_negative(self,y_true, y_pred):
        
        tn = 0
        
        for yt, yp in zip(y_true, y_pred):
            
            if yt == 0 and yp == 0:
                tn += 1
                
        return tn

    def false_positive(self,y_true, y_pred):
        
        fp = 0
        
        for yt, yp in zip(y_true, y_pred):
            
            if yt == 0 and yp == 1:
                fp += 1
                
        return fp

    def false_negative(self,y_true, y_pred):
        
        fn = 0
        
        for yt, yp in zip(y_true, y_pred):
            
            if yt == 1 and yp == 0:
                fn += 1
                
        return fn
    


