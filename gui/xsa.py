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







############################################
def main():


    ############################################
    # OPENS A CSV FILE
    def open_csv_file():
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            display_csv_data(file_path)

    ############################################
    # DOES NOTHING
    def do_nothing():
        pass


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

            if clean_data:
                    df = pd.read_csv(file_path)
                    cleaner = Csv_Cleaner(file_path)
                    df = cleaner.clean(df)

                    f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
                    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                        return
                    f.write(df.to_csv(index=False, sep=",", header=True, quotechar='"', line_terminator="\r"))
                    file_name = f.name
                    f.close()
            else:
                file_name = file_path

            header_prsent = ask("Does the file have a header ?")
            with open(file_name, 'r', newline='') as file:
                csv_reader = csv.reader(file)
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
                    tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")

        
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")




    def train_model():
        pass

    def test_model():
        pass

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
    alignment_var = tk.StringVar()
    algos = ('Dictionnary', 'KNN', 'Naive Bayes')
    alignments = ('Left', 'Center', 'Right')

    algoFrame = ttk.LabelFrame(paned_window, text="Algorithm Selection")
    algoFrame.grid(column=0, row=0, padx=20, pady=20)

    grid_column = 0
    for name, al in zip(algos, alignments):
        # create a radio button
        radio = ttk.Radiobutton(algoFrame, text=name, value=al, variable=alignment_var)
        radio.grid(column=grid_column, row=0, ipadx=10, ipady=10)
        # grid column
        grid_column += 1

    ###########
    buttonFrame = ttk.LabelFrame(paned_window, text="Action Buttons")
    buttonFrame.grid(column=0, row=0, padx=20, pady=20)

    alignment_var = tk.StringVar()
    bts = ('Train', 'Test', 'View Stats')
    alignments = ('Left', 'Center', 'Right')

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
    


