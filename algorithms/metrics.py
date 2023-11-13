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
        new= ctk.CTkToplevel(master=parent)
        new.geometry("400x500")
        new.title("Metrics")
        
        my_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        ctk.CTkLabel(new, text=model, font=my_font)
        ctk.CTkLabel(new, text="Accuracy", font=my_font).pack(pady=30)
        ctk.CTkLabel(new, text=self.get_accuracy(), font=my_font).pack(pady=30, padx=10)
        
        ctk.CTkLabel(new,text="Error Rate", font=my_font).pack(pady=30)
        ctk.CTkLabel(new, text=self.get_error_rate(), font=my_font).pack(pady=40, padx=10)
            
        ctk.CTkButton(new, text="Exit", command=new.destroy).pack(pady=45)  
        parent.wait_window(new)

    

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
    


