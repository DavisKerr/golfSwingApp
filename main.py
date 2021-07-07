from Controller.controller import Controller
from View.capture_screen import Capture_Screen
from tkinter import *
from View.double_slider import Double_Slider

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    controller = Controller(root)
    root.mainloop()