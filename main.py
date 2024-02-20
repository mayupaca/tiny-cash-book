from tkinter import *
import tkinter as tk
import ttkbootstrap as tb
from gui import TinyCashBook

if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "superhero")
    TinyCashBook(app)
    app.mainloop()
