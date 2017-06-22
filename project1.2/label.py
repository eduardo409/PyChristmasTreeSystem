from tkinter import *
from tkinter import ttk

class HeaderLabel(object):

    def __init__(self,root, title,image):
        self.label = ttk.Label(root, text=title)
        self.label.pack(fill=X)
        self.label.config(background="white")
        self.label.config(font=('Courier', 18, 'bold'))

        self.logo = PhotoImage(file=image)
        self.label.config(image=self.logo)
        self.label.config(compound='text')
        self.label.config(compound='center')
        self.label.config(compound='left')

