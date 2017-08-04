""" Brandon, Eduardo, Sergio (sam13c) """

import tkinter as tk
import re, time, hashlib
from datetime import datetime
from tkinter import ttk

try:
    import cPickle as pickle
except:
    import pickle


LARGE_FONT = ("Verdana", 24)
MEDIUM_FONT = ("Verdana",18)
SMALL_FONT = ("Verdana", 12)


class Tree(object):
    def __init__(self, data):
        if len(data) == 3:
            self.size = str(data[0])
            self.worth = data[1]
            self.id = str(data[2])
            self.sold = False
            self.date_sold = "00/00/0000"



class System(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # full screen
        # tk.Tk.wm_state(self, 'zoomed')
        tk.Tk.wm_title(self, "Alpine Christmas Trees")
        # this variable will keep track of the current amount of trees
        self.counter = 0
        self.file = open("files/data.p", 'rb')
        self.stock = []

        self.currentUser = Employee()
        self.password_label = ttk.Label()

        self.u = pickle.Unpickler(self.file)
        while True:
            try:
                self.stock = self.u.load()
            except EOFError:
                break
        self.file.close()
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Add new pages here
        for F in (MainPage, EmployeePage, EmployeeRegisterPage, InventoryAddPage, InventoryMainPage, InventoryRemovePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)



    def show_frame(self, cont):
        frame = cont(self.container,self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.focus_set()
        frame.tkraise()



    def findValue(self, size, id):
        list = []
        for value in self.stock:
            if value.size == size:
                list.append(value.id)

        for value in list:
            if value == id:
                return True

        return False



    def addInventory(self, entry):
        data = entry.get()
        data = data.split(" ")
        if len(data) == 3 and self.findValue(data[0], data[2]) == False:
            # print("Added")
            data = entry.get()
            entry.delete(0, len(data))
            data = data.split(" ")
            tree = Tree(data)
            tree.sold = False
            self.stock.append(tree)
            self.file = open("files/data.p", 'wb')
            self.p = pickle.Pickler(self.file, 3)
            self.p.dump(self.stock)
            self.file.close()
        entry.delete(0, 100)
        sizes = self.getSizes()
        self.show_frame(InventoryAddPage)

        
    def removeInventory(self, entry):
        data = entry.get()
        data = data.split(" ")
        if len(data) == 3:
            data = entry.get()
            entry.delete(0, len(data))
            data = data.split(" ")
            for i in range(0, (len(self.stock))):
                if self.stock[i].size == str(data[0]) and self.stock[i].worth == str(data[1]) and self.stock[
                    i].id == str(data[2]):
                    self.stock[i].sold = True
                    self.stock[i].date_sold = time.strftime("%d/%m/%Y")
                    self.file = open("files/data.p", 'wb')
                    self.p = pickle.Pickler(self.file, 3)
                    self.p.dump(self.stock)
                    self.file.close()
        entry.delete(0, 100)
        sizes = self.getSizes()
        self.show_frame(InventoryRemovePage)



    def getSizes(self):
        sizes = []
        for value in self.stock:
            if value.size not in sizes:
                sizes.append(value.size)
        return sizes




    def getAmount(self, size, worth):
        counter = 0
        for value in self.stock:
            if value.size == size and value.worth == worth and value.sold == False:
                # print(value.sold)
                counter = counter + 1
        return counter



class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # When using grid, any extra space in the parent(self)is allocated
        # proportionate to the "weight" of a row and/or a column
        self.grid_columnconfigure(0, weight=1)

        self.tree_logo = tk.PhotoImage(file="images/1.png").subsample(4, 4)
        self.logo_label = ttk.Label(self, text="Welcome To Alpine Christmas Trees ", background="#2a2a2a", foreground="white",
                                    font=LARGE_FONT, image=self.tree_logo, compound="left", takefocus=False)
        self.logo_label.grid(row=0, sticky="nesw")


        self.inventory_logo = tk.PhotoImage(file="images/2.png").subsample(2, 2)
        self.inventory_btn = ttk.Button(self, text="Inventory", takefocus=False, image=self.inventory_logo, compound='right',
                                        command=lambda: controller.show_frame(InventoryMainPage))
        self.inventory_btn.grid(pady=20, padx=400, sticky="nesw")

        self.employee_logo = tk.PhotoImage(file="images/3.png").subsample(2, 2)
        self.employee_btn = ttk.Button(self, text="Employee", takefocus=False, image=self.employee_logo, compound='right',
                                        command=lambda: controller.show_frame(EmployeePage))
        self.employee_btn.grid(pady=20, padx=400, sticky="nesw")


        self.report_logo = tk.PhotoImage(file="images/4.png").subsample(2, 2)
        self.report_btn = ttk.Button(self, text="Report", takefocus=False, image=self.report_logo, compound='right',
                                        command=lambda: controller.show_frame(Report))
        self.report_btn.grid(pady=20, padx=400, sticky="nesw")



class Employee(object):
    def __init__(self, firstName='N/A', lastName='N/A', phoneNumber='N/A'):
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.loggedIn = False

        id = self.firstName + self.lastName + str(self.phoneNumber)
        hash_object = hashlib.md5(id.encode())
        
        self.id = str(hash_object.hexdigest())[:6]



class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        self.tree_logo = tk.PhotoImage(file='images/3.png').subsample(2, 2)
        self.logo_label = ttk.Label(self, text='Employee System', background="#2a2a2a", foreground="white",
                                    font=LARGE_FONT, image=self.tree_logo, compound='left', takefocus=False)
        self.logo_label.grid(column=0, row=0, sticky='nesw')

        self.employeeId_label = ttk.Label(self, text='Enter Your EmployeeID', font=LARGE_FONT, width=20)
        self.employeeId_label.grid(column=0, row=1, pady=20)

        self.entry_number = ttk.Entry(self, width=40)
        self.entry_number.grid(column=0, row=2, pady=20)

        self.status_label = ttk.Label()

        self.clockInOut_btn = ttk.Button(self, text='Clock In/Out', takefocus=False,
                                         command=lambda: self.displayStatus(controller,
                                                                            controller.currentUser.firstName,
                                                                            controller.currentUser.lastName,
                                                                            controller.currentUser.loggedIn,
                                                                            controller.currentUser.id,
                                                                            self.entry_number.get()))

        self.clockInOut_btn.grid(column=0, row=3, pady=20, padx=400, sticky='nesw')

        self.employee_status = self.displayStatus(controller,
                                                  controller.currentUser.firstName,
                                                  controller.currentUser.lastName,
                                                  controller.currentUser.loggedIn,
                                                  controller.currentUser.id,
                                                  self.entry_number.get())

        self.status_label = ttk.Label(self, text=self.employee_status, font=SMALL_FONT, width=10)
        self.status_label.grid(column=0, row=4, pady=20, padx=340, sticky='nesw')

        self.register_btn = ttk.Button(self, text='Register', takefocus=False,
                                       command=lambda: controller.show_frame(EmployeeRegisterPage))

        self.register_btn.grid(column=0, row=5, pady=20, padx=400, sticky='nesw')

        self.back_btn_logo = tk.PhotoImage(file='images/5.png').subsample(5, 5)
        self.back_btn = ttk.Button(self, text='Back', image=self.back_btn_logo, cursor='hand2',
                                   compound='top', takefocus=False, command=lambda: controller.show_frame(MainPage))

        self.back_btn.grid(column=0, row=7, sticky='w', pady=40, padx=40)



    def displayStatus(self, controller, firstName, lastName, clockedIn, realID, userID):
        status = " "
        if realID == userID and clockedIn:
            status = str(firstName) + ' ' + str(lastName) + ' Clocked in at ' + str(datetime.now())
            controller.currentUser.loggedIn = False

        elif realID == userID and not clockedIn:
            status = str(firstName) + ' ' + str(lastName) + ' Clocked out at ' + str(datetime.now())
            controller.currentUser.loggedIn = True

        elif firstName is 'N/A' and lastName is 'N/A':
            status = ' '
        else:
            status = 'EmployeeId not registered or Incorrect ID'

        self.status_label = ttk.Label(self, text=status, font=SMALL_FONT, width=10)
        self.status_label.grid(column=0, row=4, pady=20, padx=340, sticky='nesw')

        return status



class EmployeeRegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.tree_logo = tk.PhotoImage(file='images/3.png').subsample(2, 2)
        self.logo_label = ttk.Label(self, text='Employee System Registration', background='#2a2a2a', foreground='white',
                                    font=LARGE_FONT, image=self.tree_logo, compound='left', takefocus=False)

        self.logo_label.grid(column=0, row=0, sticky='nesw')

        self.firstName_label = ttk.Label(self, text='First Name', font=SMALL_FONT)
        self.firstName_label.grid(column=0, row=1, pady=10)

        self.firstName_entry = ttk.Entry(self, width=40)
        self.firstName_entry.grid(column=0, row=2, pady=10)

        self.lastName_label = ttk.Label(self, text='Last Name', font=SMALL_FONT)
        self.lastName_label.grid(column=0, row=3, pady=10)

        self.lastName_entry = ttk.Entry(self, width=40)
        self.lastName_entry.grid(column=0, row=4, pady=10)

        self.phoneNumber_label = ttk.Label(self, text='Phone Number', font=SMALL_FONT)
        self.phoneNumber_label.grid(column=0, row=5, pady=10)

        self.phoneNumber_entry = ttk.Entry(self, width=40)
        self.phoneNumber_entry.grid(column=0, row=6, pady=10)

        self.register_user_btn = ttk.Button(self, text='Enter', takefocus=False,
                                            command=lambda: self.register_user(controller))
        self.register_user_btn.grid(column=0, row=7, padx=400, sticky='nesw')

        self.back_btn_logo = tk.PhotoImage(file='images/5.png').subsample(5, 5)
        self.back_btn = ttk.Button(self, text='Back', image=self.back_btn_logo, cursor='hand2',
                                   compound='top', takefocus=False, command=lambda: controller.show_frame(EmployeePage))

        self.back_btn.grid(sticky='w', pady=40, padx=40)



    def register_user(self, controller):
        controller.currentUser = Employee(self.firstName_entry.get(),
                                          self.lastName_entry.get(),
                                          self.phoneNumber_entry.get())

        controller.currentUser.loggedIn = True
        controller.password_label = ttk.Label(self, text=controller.currentUser.id, font=SMALL_FONT)
        controller.password_label.grid(column=0, row=9, pady=15)



class Report(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.grid_columnconfigure(0, weight=1)
        
        self.report_logo = tk.PhotoImage(file= "images/4.png").subsample(4,4)
        self.logo_label = ttk.Label(self, text="Welcome To Alpine Christmas Trees ", background = "#2a2a2a", foreground="white",
                                    font=LARGE_FONT,image=self.report_logo, compound="left",takefocus = False)
        self.logo_label.grid(row=0, sticky="nesw")

        self.inventory_label = ttk.Label(self, text="Inventory to start", foreground="black",
                                            font=MEDIUM_FONT,takefocus = False)
        self.inventory_label.grid(pady=28)

        tree = ttk.Treeview(self)
        #ysb = ttk.Scrollbar(self, orient='vertical',command=tree.yview)
        #tree.configure(yscroll=ysb.set)
        #tree.grid()
        #ysb.grid(row=0,column=1,sticky='ns')

        #vsb = ttk.Scrollbar(self,orient='vertical',command=tree.yview)
        #vsb = pack(side='right',fill='y')
        #tree.configure(yscrollcommand=vsb.set)

        tree["columns"]=("premium","one","two")
        tree.heading("#0", text="Sizes", anchor='w')
        tree.column("#0",anchor='w')
        tree.heading("premium", text="Premium")
        tree.column("premium",anchor='center',width=100)
        tree.heading("one",text="#ONE")
        tree.column("one",anchor='center',width=100)
        tree.heading("two",text="#TWO")
        tree.column("two",anchor="center",width=100)
        #print(len(controller.stock))
        #for o in controller.stock:
        #    print(o.sold)
        s1 = 3
        s2 = 4
        #outer for loop will initialize the sizes on the side
        #while also initializing the rest of the table
        for num in range(10):
            tex = (str(s1)+"-"+str(s2))
            val = str(s1)+str(s2)
            precount = 0
            onecount = 0
            twocount = 0
            #based off what the current size description we are in, this
            #for loop will calculate the amount of different grades there are per current size.
            #each outer loop iteration if go as follows: 3-4,4-5,5-6,6-7,7-8,ect......
            for treeobj in controller.stock:
                if treeobj.size == val and treeobj.sold == False:
                    if treeobj.worth == "pre":
                        precount = precount + 1
                    if treeobj.worth == "one":
                        onecount = onecount + 1
                    if treeobj.worth == "two":
                        twocount = twocount + 1

            if s1 != 12:
                tree.insert('','end',text=tex, value=(precount,onecount,twocount))
            else:
                tree.insert('','end',text="12+up", value=(precount,onecount,twocount))
            s1 = s1+1
            s2 = s2+1

        tree.grid(sticky="enesw")
        ttk.Style().configure("Treeview",font=("Verdana", 10))
        ttk.Style().configure("Treeview.Heading",font=("Verdana", 10))

        #tree.configure(yscrollcommand=treeScroll.set)

        # RETURN BUTTON
        self.back_btn_logo = tk.PhotoImage(file="images/5.png").subsample(5, 5)
        self.back_btn =  ttk.Button(self, text="Back", image = self.back_btn_logo,cursor = "hand2",compound = "top",takefocus = False,
                                    command=lambda: controller.show_frame(MainPage))
        self.back_btn.grid(sticky = "w", padx = 20, pady = 250)




class InventoryMainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.inventory_logo = tk.PhotoImage(file="images/6.png").subsample(3, 3)
        self.inventory_label = ttk.Label(self, text="Inventory Main", font=LARGE_FONT, takefocus=False, background="gray",
                                            image=self.inventory_logo, compound="left")
        self.inventory_label.pack(fill="both")

        self.logo = tk.PhotoImage(file="images/10.png").subsample(12, 12)
        button1 = ttk.Button(self, text="Scan Item", takefocus=False, image=self.logo, compound="right",
                             command=lambda: controller.show_frame(InventoryAddPage))
        button1.pack(pady=40, padx=20)

        self.logo2 = tk.PhotoImage(file="images/11.png").subsample(4, 4)
        button2 = ttk.Button(self, text="Remove Item", takefocus=False, image=self.logo2, compound="right",
                             command=lambda: controller.show_frame(InventoryRemovePage))
        button2.pack()

        self.logo3 = tk.PhotoImage(file="images/5.png").subsample(5, 5)
        backbutton = ttk.Button(self, text="Back", image=self.logo3, cursor="hand2", compound="top", takefocus=False,
                                command=lambda: controller.show_frame(MainPage))
        backbutton.pack(pady=60, side="left", padx=20)


class InventoryAddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.focus_set()
        self.grid_columnconfigure(0, weight=1)
        self.tree_logo = tk.PhotoImage(file="images/2.png").subsample(1, 1)
        label = ttk.Label(self, text="Inventory", foreground="green", takefocus=False,
                          font=LARGE_FONT, image=self.tree_logo, compound="left")
        label.grid(row=0, sticky = "nw")
        for size in controller.getSizes():
            if controller.getAmount(size,"pre") > 0:
                name = "label" + str(size)
                name = tk.Label(self,text = "Size " +size + ":\n" +str(controller.getAmount(size,"pre")),font = LARGE_FONT,takefocus = False,background = "red", justify = "center" ).grid(row = 0, column = size, padx = 10)

        # label/entry/add_button inside frame1
        self.frame1 = tk.Frame(self, takefocus=False)
        self.frame1.grid(columnspan = 100)
        eLabel = ttk.Label(self.frame1, text="Entry", font=LARGE_FONT, takefocus=False)
        eLabel.grid(sticky="w")
        self.entry = ttk.Entry(self.frame1, font=LARGE_FONT, takefocus=True)
        self.entry.grid()
        # make sure to just pass self and acces the varibles with the dot operator
        self.add_button = ttk.Button(self.frame1, text="ADD +", takefocus=False,
                                     command=lambda: controller.addInventory(self.entry, ))
        self.add_button.grid(pady=10)
        self.entry.bind("<Return>", self.enter_key_pressed)
        # backbutton
        self.logo = tk.PhotoImage(file="images/5.png").subsample(5, 5)

        backbutton = ttk.Button(self, text="Back", image=self.logo, cursor="hand2", compound="top", takefocus=False,
                                command=lambda: controller.show_frame(InventoryMainPage))
        backbutton.grid(sticky="w", padx=20, pady=250)
        self.entry.focus()
        #
        # button2 = ttk.Button(self, text="Page One",
        #                      command=lambda: controller.show_frame(EmployeePage))
        # button2.pack()

    def enter_key_pressed(self, *args):
        self.add_button.invoke()
        # print("Add item")


class InventoryRemovePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.focus_set()
        self.grid_columnconfigure(0, weight=1)
        self.tree_logo = tk.PhotoImage(file="images/7.png").subsample(1, 1)
        label = ttk.Label(self, text="Inventory", foreground="green", takefocus=False,
                          font=LARGE_FONT, image=self.tree_logo, compound="left")
        label.grid(row=0, sticky="nw")
        for size in controller.getSizes():
            print(size)
            if controller.getAmount(size, "pre") > 0:
                name = "label" + str(size)
                name = tk.Label(self, text="Size " + size + ":\n" + str(controller.getAmount(size, "pre")), font=LARGE_FONT,
                            takefocus=False, background="red", justify="center").grid(row=0, column=size, padx=10)

        # label/entry/add_button inside frame1
        self.frame1 = tk.Frame(self)

        eLabel = ttk.Label(self.frame1, text="Entry", font=LARGE_FONT, takefocus=False)
        eLabel.grid(sticky="w")
        self.entry2 = ttk.Entry(self.frame1, font=LARGE_FONT, takefocus=True)

        self.entry2.grid()
        self.remove_button = ttk.Button(self.frame1, text="REMOVE -", takefocus=False,
                                        command=lambda: controller.removeInventory(self.entry2))
        self.remove_button.grid(pady=10)
        self.entry2.bind("<Return>", self.enter_key_pressed)
        self.frame1.grid(columnspan = 100)
        # backbutton
        self.logo = tk.PhotoImage(file="images/5.png").subsample(5, 5)
        self.backbutton = ttk.Button(self, text="Back", image=self.logo, cursor="hand2", compound="top",
                                     takefocus=False,
                                     command=lambda: controller.show_frame(InventoryMainPage))
        self.backbutton.grid(sticky="w", padx=20, pady=250)
        self.entry2.focus()
    

    def enter_key_pressed(self, event):
        self.remove_button.invoke()





app = System()
app.mainloop()