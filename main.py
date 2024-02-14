from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import csv
from datetime import date

class TinyCashBook(tb.Frame):
    def __init__(self, master):  # master is the widget is the parent of the Tkinter window.
        super().__init__(master, padding=(20, 20))
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        # self.iconbitmap("")


        self.style = tb.Style(theme='united')
        # self.style.configure('custom_info.TEntry', foreground="black", fieldbackground="gray", bordercolor="blue")

        # Title
        self.app_title = Label(self, text="👛Tiny Cash Book👛", font=("Helvetica", 25), foreground="gray")
        self.app_title.pack(pady=(20))

        self.colors = app.style.colors

        # Hello [user name]

        # choose date

# Frames for input forms
        self.usr_input_frame = Frame(self)
        self.usr_input_frame.pack()

    # allowance form
        self.allowance_frame = tb.LabelFrame(self.usr_input_frame, text="💰Allowance💰", style='info.TLabelframe')

        self.allowance_source_label = tb.Label(self.allowance_frame, text="💡Source (How did you get the allowance?)")
        self.allowance_source_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.allowance_source_entry = tb.Entry(self.allowance_frame, style='info')
        self.allowance_source_entry.grid(row=0, column=1, padx=20, pady=20)

        self.amount_allowance_label = tb.Label(self.allowance_frame, text="💴Amount (How much?)")
        self.amount_allowance_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.amount_allowance_entry = tb.Entry(self.allowance_frame, style='info', background="red",foreground='green')
        self.amount_allowance_entry.grid(row=1, column=1, padx=20, pady=20)

        self.allowance_frame.pack(side=LEFT, padx=30)

        # button
        self.allowance_button = tb.Button(self.allowance_frame, text="ADD", style="info outline", width=20)
        self.allowance_button.grid(row=2, column=0, columnspan=2, padx=20,pady=10, sticky="news")

    # expense form
        self.expense_frame = tb.LabelFrame(self.usr_input_frame, text="💸Spending💸", style='danger.TLabelframe')

        self.expense_item_label = tb.Label(self.expense_frame, text="🍟Item (What did you use?)")
        self.expense_item_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.expense_item_entry = tb.Entry(self.expense_frame, style='danger')
        self.expense_item_entry.grid(row=0, column=1, padx=20, pady=20)

        self.amount_expense_label = Label(self.expense_frame, text="💴Amount (How much?)")
        self.amount_expense_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.amount_expense_entry = tb.Entry(self.expense_frame, style='danger', background='gray')
        self.amount_expense_entry.grid(row=1, column=1, padx=20, pady=20)

        self.expense_frame.pack(side=LEFT, padx=30)
        # button
        self.expense_button = tb.Button(self.expense_frame, text="ADD", style="danger outline", width=20)
        self.expense_button.grid(row=2, column=0, columnspan=2, padx=20,pady=10, sticky="news")

    # record list
        self.coldata = [
            {"text": "Date", "stretch": False},
            {"text": "Source or Item", "stretch": True},
            {"text": "Amount", "stretch": True},
        ]

        self.rowdata = [
            ('A123', 'IzzyCo', 12),
            ('A136', 'Kimdee Inc.', 45),
            ('A158', 'Farmadding Cofthjkll;;aaaaaaaaa;.', 36)
        ]

        self.dt = Tableview(
            # master=app,
            coldata=self.coldata,
            rowdata=self.rowdata,
            searchable=True,
            bootstyle=WARNING,
            stripecolor=(self.colors.light, None),

        )
        self.dt.pack(fill=BOTH, padx=(50, 50), pady=(20, 50), anchor="w")


if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "united")
    TinyCashBook(app)
    app.mainloop()
