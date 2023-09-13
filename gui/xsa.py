import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
from pathlib import Path



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
    # DISPLAYS THE DATA FROM THE CSV ONTO THE TREEVIEW
    def display_csv_data(file_path):
        try:
            with open(file_path, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Read the header row
                tree.delete(*tree.get_children())  # Clear the current data

                tree["columns"] = header
                for col in header:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)

                for row in csv_reader:
                    tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")

        
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    ############################################






    ############################################
    # FRAME BUILDING
    ############################################
    splash_root.destroy()

    root = tk.Tk()
    root.title("X(Twitter) Sentiment Analysis - GUI")

    paned_window = ttk.PanedWindow(root, orient="vertical")
    paned_window.pack(fill='both', expand=True)



    upper_frame = tk.Frame(paned_window, background='grey')
    down_frame = tk.Frame(paned_window, background='white')


    # down frame
    RBttn = tk.Radiobutton(down_frame, text = "Algo1", command = do_nothing,
                    value = 1)
    RBttn.pack(padx = 5, pady = 5)
    RBttn2 = tk.Radiobutton(down_frame, text = "Algo2", command = do_nothing,
                        value = 2)
    RBttn2.pack(padx = 50, pady = 5)

    Button = tk.Button(down_frame, text = "Train", command = do_nothing)
    Button.pack()


    #upper frame
    style = ttk.Style(upper_frame)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="grey", 
                    fieldbackground="grey", foreground="white")
    
    tree = ttk.Treeview(upper_frame, show="headings")
    tree.pack(padx=20, pady=20, fill="both", expand=True)

    status_label = tk.Label(upper_frame, text="", padx=20, pady=10)
    status_label.pack()

    open_button = tk.Button(upper_frame, text="Open CSV File", command=open_csv_file)
    open_button.pack(padx=20, pady=10)




    paned_window.add(upper_frame)
    paned_window.add(down_frame)


# Set Interval
splash_root.after(3000, main)
 
# Execute tkinter
splash_root.mainloop()
    


