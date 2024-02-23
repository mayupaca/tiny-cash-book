import ttkbootstrap as tb
from gui import TinyCashBook

if __name__ == "__main__":
    # Create new app window for app
    app = tb.Window("TinyCashBook", "pulse")
    TinyCashBook(app)
    app.mainloop()
