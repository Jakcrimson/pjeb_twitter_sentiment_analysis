from ast import literal_eval
import os, sys
import customtkinter as ctk 
from PIL import Image

ctk.set_appearance_mode("dark") 
  
ctk.set_default_color_theme("blue") 

from numpy import number
sys.path.insert(0, os.path.dirname("algorithms"))

import copy
import tkinter as tk
from tkinter import PanedWindow, ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
from pathlib import Path
import pandas as pd
from tkinter import Menu
from tkinter import font
from tkinter import filedialog

from csv_cleaner import Csv_Cleaner
from csv_editor import Application
from algorithms.naive_classification import NaiveClassification
from algorithms.metrics import Metrics
from algorithms.knn import KNN 

############################################
### splash window
splash_root = tk.Tk()
splash_root.title('XSA - GUI')
 
# Adjust size
splash_root.geometry("500x500")
 
path = Path(__file__).parent / "."
logo_path = (path / "./assets/black_logo.png").resolve()

photo = tk.PhotoImage(file=logo_path)
image_label = ttk.Label(
    splash_root,
    image=photo,
    text='XSA',
    compound='top'
)
image_label.pack()
############################################



number_of_k_value = None
distance_value = None
active_dataset = None
############################################
def main(): 

    def set_active_dataset(df):
        global active_dataset
        active_dataset = df

    def get_active_dataset():
        global active_dataset
        return active_dataset

    ############################################
    # OPENS A CSV FILE
    def open_csv_file():
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            display_csv_data(file_path)

    ############################################
    # ASKS THE USER A YES NO QUESTION
    def ask(question):
        response = messagebox.askyesno("XSA - User input",
                          question,
                          icon ='question')
        if response:    # If the answer was "Yes" response is True
            return True
        else:           # If the answer was "No" response is False
            return False

    ############################################
    # DISPLAYS THE DATA FROM THE CSV ONTO THE TREEVIEW
    def display_csv_data(file_path):
        #try:
            clean_data = ask("Would you like to clean your data ?")
            file_name = ""
            df = pd.read_csv(file_path)
            set_active_dataset(df)

            if clean_data:
                    df = pd.read_csv(file_path)
                    cleaner = Csv_Cleaner(file_path)
                    df = cleaner.clean(df)

                    set_active_dataset(df)

                    f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                        return
                    f.write(active_dataset.to_csv(index=False, sep=",", header=True, quotechar='"', lineterminator="\r"))
                    file_name = f.name
                    f.close()
            else:
                file_name = file_path

            header_prsent = ask("Does the file have a header ?")
            with open(file_name, 'r', newline='') as file:
                csv_reader = csv.reader(file, quoting=csv.QUOTE_ALL)
                if header_prsent:
                    header = next(csv_reader)
                else:
                    header=["target", "ids", "date", "flag", "user", "text"]

                tree.delete(*tree.get_children())  # Clear the current data

                tree["columns"] = header
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, width=300, stretch=True)

                for row in csv_reader:
                    tree.insert('', "end", values=row)

            #status_label.config(text=f"CSV file loaded: {file_path}")

        
        #except Exception as e:
            #status_label.setvar(text=f"Error: {str(e)}")


    def user_selection_model_parameter(model):
        """Allows the user to select the hyperparameters of his model before training the model.

        Args:
            model (str): the str equivalent of the model (e.g : 'knn', 'naive_classification', 'naive_bayes' ...)
        """
        global number_of_k_value
        global distance_value
        global vote_value


        number_of_k_value = tk.StringVar()
        distance_value = tk.StringVar()
        vote_value = tk.StringVar()

        if model == 'knn':
            new= ctk.CTkToplevel(master=root)
            new.geometry("400x600")
            new.title("User Input")
            
            my_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")


            ctk.CTkLabel(new, text="Number of K", font=my_font).pack(pady=20)
            ctk.CTkEntry(new, textvariable=number_of_k_value).pack(pady=20, padx=10)
            
            ctk.CTkLabel(new,text="Distance", font=my_font).pack(pady=20)
            choices = ["naive", "levenshtein", "lcs", "damerau_levenshtein", "hamming", "jaro", "cosine", "jaccard", "sorensen_dice", "qgram_dice"]
            ctk.CTkComboBox(new, variable=distance_value, values=choices).pack(pady=40, padx=10)

            ctk.CTkLabel(new, text="Vote", font=my_font).pack(pady=20)
            votes = ["majoritaire", "pondéré"]
            ctk.CTkComboBox(new, variable=vote_value, values=votes).pack(pady=20, padx=10)

        if model == "naive_bayes":
            pass
                
        ctk.CTkButton(new, text="Validate Parameters and exit", command=new.destroy).pack(pady=30)   
        root.wait_window(new)


    def train_model():
        """trains the model based on the parameters that were input by the user.
        """
        selection = algo_var.get()
        if selection == 'naive_bayes':
            messagebox.showinfo(title="Info", message="Not implemented yet -_-")

        elif selection == 'knn':
            if isinstance(get_active_dataset(), type(None)):
                messagebox.showwarning(title="Warning", message="Please load a training dataset in the CSV viewer")
            else:
                messagebox.showinfo(title="Info", message="KNN Classification doesn't technically need training")

        elif selection == 'naive_classification':
            messagebox.showinfo(title="Info", message="Naïve Classification doesn't need training")




    def test_model():
        """tests the model based on the parameters that were input by the user.
        """
        selection = algo_var.get()
        
        if selection == 'naive_bayes':
            messagebox.showinfo(title="Info", message="Not implemented yet -_-")

        elif selection == 'knn':
            if isinstance(get_active_dataset(), type(None)):
                messagebox.showwarning(title="Warning", message="Please load a training dataset in the CSV viewer")
            else:

                df_train = copy.deepcopy(active_dataset)
                messagebox.showinfo(title="Info KNN", message="Load your testing data")
                open_csv_file()
                df_test = copy.deepcopy(active_dataset)
                user_selection_model_parameter("knn")
                print("DISTANCE VALUE ",distance_value.get())
                print("N°K ",number_of_k_value.get())
                print("VOTE VALUE ",vote_value.get())
                knn_model = KNN(df_train ,number_of_k_value.get(), distance_value.get(), vote_value.get())
                

                classifications = []
                for tweet_token in df_test["Tweet_Tokenized"]:
                    tweet_a_categoriser = " ".join(literal_eval(tweet_token))
                    classifications.append(knn_model.classification(tweet_a_categoriser))
                df_test["model_class"] = classifications

                set_active_dataset(df_test)
                f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                    return

                f.write(active_dataset.to_csv(index=False, sep=",", header=True, quotechar='"', lineterminator="\r"))
                file_name = f.name
                f.close()
                display_csv_data(file_name)
            

        elif selection == 'naive_classification':
            if isinstance(get_active_dataset(), type(None)):
                messagebox.showwarning(title="Warning", message="Please load a dataset in the CSV viewer")
            else: 
                nc = NaiveClassification(active_dataset)
                classified_df = nc.get_classified()
                set_active_dataset(classified_df)
                f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                    return

                f.write(active_dataset.to_csv(index=False, sep=",", header=True, quotechar='"', lineterminator="\r"))
                file_name = f.name
                f.close()
                display_csv_data(file_name)
                


    def show_model_stats():
        selection = algo_var.get()
        if selection=="knn":
            metrics = Metrics(active_dataset, parent=root, model=selection)
        if selection=="naive_bayes":
            messagebox.showinfo(title="Information", message="Not implemented yet")
        if selection=="naive_classification":
            metrics = Metrics(active_dataset, parent=root, model=selection)


        

    ############################################


    ############################################
    # FRAME BUILDING
    ############################################

    splash_root.destroy()
    root = ctk.CTk()
    root.geometry("1000x600")
    root.title("X(Twitter) Sentiment Analysis - GUI")

    paned_window = tk.PanedWindow(root, orient="vertical", borderwidth=0)
    paned_window.pack(fill='both', expand=True)

    upper_frame = ctk.CTkFrame(paned_window, width=600, height=600,  border_width=0)
    middle_frame = ctk.CTkFrame(paned_window, width=600, height=600,  border_width=0)

    ###########"
    # STYLES ###"
    ###########"
    # Create style Object    
    style = ttk.Style(upper_frame)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="white", 
                    fieldbackground="#1e1b24", foreground="black")
    style.configure("TPanedwindow", background="black")




    ############"
    # FRAMES ###"
    ############"
    #upper frame    
    tree = ttk.Treeview(upper_frame, show="headings")
    tree.pack(padx=20, pady=20, fill="both", expand=True)

    status_label = ctk.CTkLabel(upper_frame, text="", padx=20, pady=10)
    status_label.pack()

    open_button = ctk.CTkButton(upper_frame, text="Open CSV file",command=open_csv_file)
    open_button.pack(padx=20, pady=10)


    #middle frame
    csv_editor = Application(middle_frame)
    csv_editor.pack()
    open_button = ctk.CTkButton(middle_frame, text="Open CSV file",command=csv_editor.loadCells)
    open_button.pack(padx=50, pady=10)

    menubar = Menu(root, background='#1E1B24', fg='white')

    filemenu = Menu(menubar, tearoff=0, background='#1E1B24', fg='white')
    filemenu.add_command(label="New", command=csv_editor.newCells)     # add save dialog
    # add save dialog
    filemenu.add_command(label="Open", command=csv_editor.loadCells)
    filemenu.add_command(label="Save as", command=csv_editor.saveCells)
    filemenu.add_command(label="Exit", command=csv_editor.quit)

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_command(label="Exit", command=csv_editor.quit)

    root.config(menu=menubar, background="#1E1B24")

    default_font = font.nametofont("TkTextFont")
    default_font.configure(family="Helvetica")

    root.option_add("*Font", default_font)    


    # down frame
    algo_var = tk.StringVar()

    algoFrame = ctk.CTkFrame(paned_window, width=600, height=600,  border_width=0)
    algoFrame.grid(column=0, row=0, padx=20, pady=20)
    
    # create a radio button
    naive_classif = ctk.CTkRadioButton(algoFrame, text='Dictionnary', value='naive_classification', variable=algo_var)
    naive_classif.grid(column=0, row=0, ipadx=10, ipady=10)
    knn = ctk.CTkRadioButton(algoFrame, text='KNN', value='knn', variable=algo_var)
    knn.grid(column=1, row=0, ipadx=10, ipady=10, sticky=tk.E)
    naive_bayes = ctk.CTkRadioButton(algoFrame, text='Naive Bayes', value='naive_bayes', variable=algo_var)
    naive_bayes.grid(column=2, row=0, ipadx=10, ipady=10, sticky=tk.NS)


    ###########
    buttonFrame = ctk.CTkFrame(paned_window, width=600, height=600, border_width=0)
    buttonFrame.grid(column=0, row=0, padx=20, pady=20)

    train = ctk.CTkButton(buttonFrame, text="Train", command=train_model)
    train.grid(column=0, row=0, ipadx=10, ipady=10)
    test = ctk.CTkButton(buttonFrame, text="Test", command=test_model)
    test.grid(column=1, row=0, ipadx=10, ipady=10)
    stats = ctk.CTkButton(buttonFrame, text="Stats", command=show_model_stats)
    stats.grid(column=2, row=0, ipadx=10, ipady=10)


    paned_window.add(middle_frame)
    paned_window.add(upper_frame)
    paned_window.add(algoFrame)
    paned_window.add(buttonFrame)

    root.mainloop()


# Set Interval
splash_root.after(0, main)
 
# Execute tkinter
splash_root.mainloop()