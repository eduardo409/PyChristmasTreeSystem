from tkinter import *
from tkinter import ttk


class BigButtons(object):

    def __init__(self, root, title, file):
        button = ttk.Button(root, text=title, cursor="hand2")
        button.pack(fill=BOTH, padx=500, pady=25)
        self.logo = PhotoImage(file="images/"+file).subsample(2, 2)
        button.config(image=self.logo, compound=RIGHT)

