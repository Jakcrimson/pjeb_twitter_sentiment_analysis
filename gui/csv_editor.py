# pylint: disable=C0103,C0111,W0614,W0401,C0200,C0325
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import csv

##
# Credit to Sebastian Safari for global architecture of the editor
##
## Code adapted by Pierre Lague for XSA App.
##

class Application(Frame):

    cellList = []
    currentCells = []
    currentCell = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createDefaultWidgets()

    def focus_tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_right(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(j >= len(self.currentCells[0]) - 1 ):
                        j = -1    
                    self.currentCells[i][j+1].focus()
        return "break"

    def focus_left(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(j == 0):
                        j = len(self.currentCells[0])    
                    self.currentCells[i][j-1].focus()
        return "break"

    def focus_up(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(i < 0):
                        i = len(self.currentCells)
                    self.currentCells[i-1][j].focus()
        return "break"

    def focus_down(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if( i >= len(self.currentCells) - 1):
                        i = -1
                    self.currentCells[i+1][j].focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    def saveFile(self, event):
        self.saveCells()

    # TODO: Create bind for arrow keys and enter

    def createDefaultWidgets(self):
        w, h = 4, 4
        self.sizeX = 1
        self.sizeY = 1
        self.defaultCells = []
        for i in range(self.sizeY):
            self.defaultCells.append([])
            for j in range(self.sizeX):
                self.defaultCells[i].append([])

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.saveFile)
                #TODO: Add resize check on column when changing focus
                tmp.insert(END, "")
                tmp.grid(padx=0, pady=0, column=j, row=i)

                self.defaultCells[i][j] = tmp
                self.cellList.append(tmp)

        self.defaultCells[0][0].focus_force()
        self.currentCells = self.defaultCells
        self.currentCell = self.currentCells[0][0]

        # TODO: Add buttons to create new rows/columns

    def newCells(self):
        self.removeCells()
        self.createDefaultWidgets()

    def removeCells(self):
        while(len(self.cellList) > 0):
            for cell in self.cellList:
                # print str(i) + str(j)
                cell.destroy()
                self.cellList.remove(cell)

    def loadCells(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        ary = []
        col = -1
        rows = []

        # get array size & get contents of rows
        with open(filename, "r", newline='\n') as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            for row in rd:
                ary.append([])
                col = len(row)
                rows.append(row)

        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])

        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                print(rows[i][j])
                ary[i][j] = rows[i][j]

        self.removeCells()

        # get the max width of the cells
        widths = []
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                widths.append(len(ary[i][j]))
        w = 15

        loadCells = []
        for i in range(len(ary)):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])

        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                tmp = Text(self, width=widths[j]+20, height=2)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.saveFile)
                tmp.insert(END, ary[i][j])

                if(i == 0):
                    tmp.config(font=("Helvetica", 10, font.BOLD))
                    tmp.config(relief=FLAT, bg="white")

                loadCells[i][j] = tmp
                tmp.focus_force()
                self.cellList.append(tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)

        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]


    def saveCells(self):
        filename = filedialog.asksaveasfilename(initialdir=".", title="Save File", filetypes=(
            ("csv files", "*.csv"), ("all files", "*.*")), defaultextension=".csv")

        vals = []
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                vals.append(self.currentCells[i][j].get(1.0, END).strip())

        with open(filename, "w") as csvfile:
            for rw in range(len(self.currentCells)):
                row = ""
                for i in range(len(self.currentCells[0])):
                    x = rw * len(self.currentCells[0])
                    if(i != len(self.currentCells[0]) - 1):
                        row += '"'+vals[x + i]+'"' + ","
                    else:
                        row += '"'+vals[x + i]+'"'

                csvfile.write(row +"\n")

        messagebox.showinfo("", "Saved!")


# End Application Class #


# End functions #