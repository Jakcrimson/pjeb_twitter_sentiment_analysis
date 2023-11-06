import pandas as pd
import numpy as np

from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font



class Metrics(Frame):

    def __init__(self, classified_dataset, parent, model):

        self.classified_dataset = classified_dataset
        new= tk.Toplevel(parent)
        new.geometry("400x500")
        new.title("Metrics")

        tk.Label(new, text=model, font=('Helvetica 18 bold'))
        
        tk.Label(new, text="Accuracy", font=('Helvetica 12 bold')).pack(pady=30)
        tk.Label(new, text=self.get_accuracy(), font=('Helvetica 11 bold')).pack(pady=30, padx=10)
        
        tk.Label(new,text="Error Rate", font=('Helvetica 12 bold')).pack(pady=30)
        tk.Label(new, text=self.get_error_rate(), font=('Helvetica 11 bold')).pack(pady=40, padx=10)
            
        tk.Button(new, text="Exit", command=new.destroy).pack(pady=45)  
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
    


