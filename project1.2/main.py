from BigButtons import *
from label import *

if __name__ == "__main__":
    root = Tk()
    frame = Frame(root,)
    frame.pack(fill = BOTH)
    l1 = HeaderLabel(frame, "main menu","images/tree.png")
    b1 = BigButtons(frame, "Employee", "employeeImage.png")
    b2 = BigButtons(frame, "Inventory", "inventoryImage.png")
    b3 = BigButtons(frame, "Report", "reportImage.png")
    frame.config(background="#b3f9b1")
    root.mainloop()
