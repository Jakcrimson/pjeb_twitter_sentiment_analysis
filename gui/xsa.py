import os, sys
sys.path.insert(0, os.path.dirname("algorithms"))

import tkinter as tk
from tkinter import ttk
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

############################################
### splash window
splash_root = tk.Tk()
splash_root.title('XSA - GUI')
 
# Adjust size
splash_root.geometry("500x500")
 
path = Path(__file__).parent / "."
logo_path = (path / "./assets/logo.png").resolve()

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
        try:
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
                    f.write(active_dataset.to_csv(index=False, sep=",", header=True, quotechar='"', line_terminator="\r"))
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

            status_label.config(text=f"CSV file loaded: {file_path}")

        
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")


    def user_selection_model_parameter(model):
        global number_of_k_value
        global distance_value

        number_of_k_value = tk.StringVar()
        distance_value = tk.StringVar()

        if model == 'knn':
            new= tk.Toplevel(root)
            new.geometry("400x500")
            new.title("User Input")
            
            tk.Label(new, text="Number of K", font=('Helvetica 12 bold')).pack(pady=30)
            tk.Entry(new, textvariable=number_of_k_value).pack(pady=30, padx=10)
            
            tk.Label(new,text="Distance", font=('Helvetica 12 bold')).pack(pady=30)
            tk.Entry(new, textvariable=distance_value).pack(pady=40, padx=10)
                
        tk.Button(new, text="Validate Parameters and exit", command=new.destroy).pack(pady=45)   
        root.wait_window(new)


    def train_model():
        selection = algo_var.get()
        if selection == 'naive_bayes':
            pass

        elif selection == 'knn':
            print("going in KNN")
            user_selection_model_parameter("knn")
            # print(number_of_k_value.get())
            # print(distance_value.get())

        elif selection == 'naive_classification':
            messagebox.showinfo(title="Info", message="Naïve Classification doesn't need training")




    def test_model():
        selection = algo_var.get()
        
        if selection == 'naive_bayes':
            pass

        elif selection == 'knn':
            # knn_classifier = KNN(number_of_k_value, distance_value)
            pass

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

                f.write(active_dataset.to_csv(index=False, sep=",", header=True, quotechar='"', line_terminator="\r"))
                file_name = f.name
                f.close()
                display_csv_data(file_name)
                


    def show_model_stats():
        pass

    ############################################






    ############################################
    # FRAME BUILDING
    ############################################
    splash_root.destroy()

    root = tk.Tk()
    root.geometry("800x800")
    root.title("X(Twitter) Sentiment Analysis - GUI")

    paned_window = ttk.PanedWindow(root, orient="vertical")
    paned_window.pack(fill='both', expand=True)



    upper_frame = ttk.Labelframe(paned_window, text="CSV Viewer")
    middle_frame = ttk.Labelframe(paned_window, text="CSV Editor")



    ############"
    # STYLES ###"
    ############"
    # Create style Object    
    style = ttk.Style(upper_frame)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="white", 
                    fieldbackground="white", foreground="black")








    ############"
    # FRAMES ###"
    ############"
    #upper frame    
    tree = ttk.Treeview(upper_frame, show="headings")
    tree.pack(padx=20, pady=20, fill="both", expand=True)

    status_label = tk.Label(upper_frame, text="", padx=20, pady=10)
    status_label.pack()

    open_button = tk.Button(upper_frame, text="Open CSV file", activebackground='#345',activeforeground='white', command=open_csv_file)
    open_button.pack(padx=20, pady=10)


    #middle frame
    csv_editor = Application(middle_frame)
    csv_editor.pack()
    open_button = tk.Button(middle_frame, text="Open CSV file",activebackground='#345',activeforeground='white', command=csv_editor.loadCells)
    open_button.pack(padx=50, pady=10)

    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=csv_editor.newCells)     # add save dialog
    # add save dialog
    filemenu.add_command(label="Open", command=csv_editor.loadCells)
    filemenu.add_command(label="Save as", command=csv_editor.saveCells)
    filemenu.add_command(label="Exit", command=csv_editor.quit)

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_command(label="Exit", command=csv_editor.quit)

    root.config(menu=menubar)

    default_font = font.nametofont("TkTextFont")
    default_font.configure(family="Helvetica")

    root.option_add("*Font", default_font)    


    # down frame
    algo_var = tk.StringVar()

    algoFrame = ttk.LabelFrame(paned_window, text="Algorithm Selection (Testing and Training are done on the file opened in the CSV Viewer !)")
    algoFrame.grid(column=0, row=0, padx=20, pady=20)
    
    # create a radio button
    naive_classif = ttk.Radiobutton(algoFrame, text='Dictionnary', value='naive_classification', variable=algo_var)
    naive_classif.grid(column=0, row=0, ipadx=10, ipady=10)
    knn = ttk.Radiobutton(algoFrame, text='KNN', value='knn', variable=algo_var)
    knn.grid(column=1, row=0, ipadx=10, ipady=10)
    naive_bayes = ttk.Radiobutton(algoFrame, text='Naive Bayes', value='naive_bayes', variable=algo_var)
    naive_bayes.grid(column=2, row=0, ipadx=10, ipady=10)


    ###########
    buttonFrame = ttk.LabelFrame(paned_window, text="Action Buttons")
    buttonFrame.grid(column=0, row=0, padx=20, pady=20)

    train = ttk.Button(buttonFrame, text="Train", command=train_model)
    train.grid(column=0, row=0, ipadx=10, ipady=10)
    test = ttk.Button(buttonFrame, text="Test", command=test_model)
    test.grid(column=1, row=0, ipadx=10, ipady=10)
    stats = ttk.Button(buttonFrame, text="Stats", command=show_model_stats)
    stats.grid(column=2, row=0, ipadx=10, ipady=10)


    paned_window.add(middle_frame)
    paned_window.add(upper_frame)
    paned_window.add(algoFrame)
    paned_window.add(buttonFrame)



# Set Interval
splash_root.after(3000, main)
 
# Execute tkinter
splash_root.mainloop()
    


