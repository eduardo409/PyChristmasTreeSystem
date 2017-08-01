import tkinter as tk
from tkinter import ttk
try:
    import cPickle as pickle
except:
    import pickle


LARGE_FONT = ("Verdana", 24)


class System(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # full screen
        #tk.Tk.wm_state(self, 'zoomed')
        tk.Tk.wm_title(self, "Alpine Christmas Trees")
        # this variable will keep track of the current amount of trees
        self.counter = 0
        self.stock = []
        self.file = open("files\data.p", 'rb')

        self.u = pickle.Unpickler(self.file)
        while True:
            try:
                self.stock = self.u.load()
            except EOFError:
                break
        self.file.close()
        print(self.stock)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Add new pages here
        for F in (MainPage, EmployeePage, InventoryAddPage, InventoryMainPage,InventoryRemovePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.focus_set()
        frame.tkraise()


    def addInventory(self,entry,amount):
        id = entry.get()
        entry.delete(0,len(id))
        if id not in self.stock and id != "":
            self.stock.append(id)
            self.file = open("files\data.p", 'wb')
            self.p = pickle.Pickler(self.file, 3)
            self.p.dump(self.stock)
            self.file.close()
            print(self.stock)
            amount.config(text = "AMOUNT:\n "+ str(len(self.stock)))
    def removeInventory(self, entry, amount):
        id = entry.get()
        entry.delete(0,len(id))
        if id in self.stock:
            self.stock.remove(id)
            self.file = open("files\data.p", 'wb')
            self.p = pickle.Pickler(self.file, 3)
            self.p.dump(self.stock)
            self.file.close()
            print(self.stock)
            amount.config(text = "AMOUNT:\n "+ str(len(self.stock)))

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # When using grid, any extra space in the parent(self)is allocated
        #  proportionate to the "weight" of a row and/or a column
        self.grid_columnconfigure(0, weight=1)

        # header tree image
        self.tree_logo = tk.PhotoImage(file= "images/1.png").subsample(4,4)
        label = ttk.Label(self, text="Welcome To Alpine Christmas Trees ", background = "#2a2a2a", foreground="white",
                          font=LARGE_FONT,image=self.tree_logo, compound="left",takefocus = False)
        label.grid(row=0, sticky="nesw")

        # Butt

        self.logo = tk.PhotoImage(file="images/2.png" ).subsample(2, 2)
        inventory_button = ttk.Button(self, text="Inventory",takefocus = False,image=self.logo,compound='right',
                             command=lambda: controller.show_frame(InventoryMainPage))
        inventory_button.grid(pady = 20,padx=400, sticky = "nesw")

        self.logo2 = tk.PhotoImage(file="images/3.png").subsample(2, 2)
        employee_button = ttk.Button(self, text="Employee",takefocus = False,image=self.logo2,compound='right',
                            command=lambda: controller.show_frame(EmployeePage))
        employee_button.grid(pady = 20,padx=400, sticky = "nesw")

        self.logo3 = tk.PhotoImage(file="images/4.png").subsample(2, 2)
        inventory_button = ttk.Button(self, text="Report",takefocus = False,image=self.logo3,compound='right',)
        inventory_button.grid(pady = 20,padx=400, sticky = "nesw")




class EmployeePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        #
        # button1 = ttk.Button(self, text="Back to Home",takefocus = False,
        #                      command=lambda: controller.show_frame(MainPage))
        # button1.pack()
        #
        # button2 = ttk.Button(self, text="Page Two",
        #                      command=lambda: controller.show_frame(InventoryPage))
        # button2.pack()


class InventoryMainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Inventory Main", font=LARGE_FONT,takefocus = False)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Scan Item",takefocus = False,
                             command=lambda: controller.show_frame(InventoryAddPage))
        button1.pack()

        button2 = ttk.Button(self, text="Remove Item",takefocus = False,
                             command=lambda: controller.show_frame(InventoryRemovePage))
        button2.pack()


class InventoryAddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.focus_set()
        self.grid_columnconfigure(0, weight=1)
        self.tree_logo = tk.PhotoImage(file= "images\\2.png").subsample(1,1)
        label = ttk.Label(self, text="Inventory", foreground="green",takefocus = False,
                          font=LARGE_FONT,image=self.tree_logo, compound="left")
        label.grid(row=0, sticky="nesw")
        amountLabel = tk.Label(self,text = "Amount:\n" + str(len(controller.stock)),font = LARGE_FONT,takefocus = False,background = "red", justify = "center" )
        amountLabel.grid(row =0, sticky = "ne", padx = 200,pady = 50)

        #label/entry/add_button inside frame1
        self.frame1 = tk.Frame(self, takefocus = False)
        self.frame1.grid()
        eLabel = ttk.Label(self.frame1,text = "Entry", font = LARGE_FONT,takefocus = False)
        eLabel.grid(sticky = "w")
        self.entry = ttk.Entry(self.frame1, font = LARGE_FONT, takefocus = True)
        self.entry.grid()
        self.add_button = ttk.Button(self.frame1, text="ADD +",takefocus = False,
                             command=lambda: controller.addInventory(self.entry,amountLabel))
        self.add_button.grid(pady = 10)
        self.entry.bind("<Return>", self.enter_key_pressed)
        #backbutton
        self.logo = tk.PhotoImage(file = "images\\5.png").subsample(5,5)

        backbutton =  ttk.Button(self, text="Back", image = self.logo,cursor = "hand2",compound = "top",takefocus = False,
                    command=lambda: controller.show_frame(InventoryMainPage))
        backbutton.grid(sticky = "w", padx = 20, pady = 250)
        self.entry.focus()
        #
        # button2 = ttk.Button(self, text="Page One",
        #                      command=lambda: controller.show_frame(EmployeePage))
        # button2.pack()
    def enter_key_pressed(self,*args):
        self.add_button.invoke()
        print("Add item")

class InventoryRemovePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.focus_set()
        self.grid_columnconfigure(0, weight=1)
        self.tree_logo = tk.PhotoImage(file= "images\\7.png").subsample(1,1)
        label = ttk.Label(self, text="Inventory", foreground="green",takefocus = False,
                          font=LARGE_FONT,image=self.tree_logo, compound="left")
        label.grid(row=0, sticky="nesw")
        amountLabel = tk.Label(self,text = "Amount:\n" + str(len(controller.stock)),font = LARGE_FONT,takefocus = False,background = "red", justify = "center" )
        amountLabel.grid(row =0, sticky = "ne", padx = 200,pady = 50)

        #label/entry/add_button inside frame1
        self.frame1 = tk.Frame(self)

        eLabel = ttk.Label(self.frame1,text = "Entry", font = LARGE_FONT,takefocus = False)
        eLabel.grid(sticky = "w")
        self.entry2 = ttk.Entry(self.frame1, font = LARGE_FONT, takefocus = True)

        self.entry2.grid()
        self.remove_button = ttk.Button(self.frame1, text="REMOVE -",takefocus = False,
                             command=lambda: controller.removeInventory(self.entry2,amountLabel))
        self.remove_button.grid(pady = 10)
        self.entry2.bind("<Return>", self.enter_key_pressed)
        self.frame1.grid()
        #backbutton
        self.logo = tk.PhotoImage(file = "images\\5.png").subsample(5,5)
        self.backbutton =  ttk.Button(self, text="Back", image = self.logo,cursor = "hand2",compound = "top",takefocus = False,
                    command=lambda: controller.show_frame(InventoryMainPage))
        self.backbutton.grid(sticky = "w", padx = 20, pady = 250)

        # self.entry2.focus_set()

    def enter_key_pressed(self,event):
        self.remove_button.invoke()
        print("Remove")


app = System()

app.mainloop()