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
        # Title
        self.app_title = tb.Label(self, text="👛Tiny Cash Book👛", font=("Helvetica", 20), foreground="#3D5361", )
        self.app_title.pack(padx=50, pady=(20, 30), anchor="w")


        # Hello [user name]

        # choose date

        self.main_frame = Frame(self)
        self.main_frame.pack()

        ####### Frames for input forms #######################################
        # Allowance form -------------------------------------------------
        self.allowance_frame = tb.LabelFrame(self.main_frame, text="💰Allowance💰", style='info.TLabelframe')

        # Source label
        self.allowance_source_label = tb.Label(self.allowance_frame, text="💡Source (How did you get the allowance?)")
        self.allowance_source_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Source entry
        self.allowance_source_entry = tb.Entry(self.allowance_frame, style='info')
        self.allowance_source_entry.grid(row=0, column=1, padx=10, pady=10)
        # Amount label
        self.amount_allowance_label = tb.Label(self.allowance_frame, text="💴Amount (How much?)")
        self.amount_allowance_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # Amount entry
        self.amount_allowance_entry = tb.Entry(self.allowance_frame, style='info', background="red", foreground='green')
        self.amount_allowance_entry.grid(row=1, column=1, padx=10, pady=10)

        self.allowance_frame.pack(side=LEFT, padx=30)

        # Allowance add button
        self.allowance_button = tb.Button(self.allowance_frame, text="ADD", style="info outline")
        self.allowance_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="news")

        # Expense form ----------------------------------------------------
        self.expense_frame = tb.LabelFrame(self.main_frame, text="💸Spending💸", style='danger.TLabelframe')

        # Expense label
        self.expense_item_label = tb.Label(self.expense_frame, text="🍟Reason (What did you use?)")
        self.expense_item_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Expense entry
        self.expense_item_entry = tb.Entry(self.expense_frame, style='danger')
        self.expense_item_entry.grid(row=0, column=1, padx=10, pady=10)
        # Amount label
        self.amount_expense_label = Label(self.expense_frame, text="💴Amount (How much?)")
        self.amount_expense_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # Amount entry
        self.amount_expense_entry = tb.Entry(self.expense_frame, style='danger', background='gray')
        self.amount_expense_entry.grid(row=1, column=1, padx=10, pady=10)

        self.expense_frame.pack(side=LEFT, padx=30)

        # Expense add button
        self.expense_button = tb.Button(self.expense_frame, text="ADD", style="danger outline")
        self.expense_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="news")

        ####### Record table ###########################################
        self.record = tb.LabelFrame(self.main_frame, text="Record", style='warning.TLabelframe')

        self.columns = ("date", "source_or_item", "amount")
        # Create Treeview
        self.record_tree = tb.Treeview(style="warning", columns=self.columns, show="headings")
        self.record_tree.pack(padx=(50), pady=(10, 50), anchor="w")
        # Format columns
        self.record_tree.column('date', width=200, anchor=W)
        self.record_tree.column('source_or_item', width=400, anchor=W)
        self.record_tree.column('amount', width=200, anchor=E)
        # Define headings
        self.record_tree.heading('date', text="Date", anchor=W)
        self.record_tree.heading('source_or_item', text="Source or Item", anchor=W)
        self.record_tree.heading('amount', text="Amount", anchor=E)
        # Sample Data
        self.input_data = [
            ('1/Jan/2024', 'Did some weeding in the garden', 10),
            ('5/Jan/2024', 'Bought snacks', -5),
            ('10/Jan/2024', 'Assisted in cleaning up dishes', 5),
            ('14/Jan/2024', 'Sorted out recyclables in the house.', 5),
        ]
        # Add Data To Treeview
        for record in self.input_data:
            self.record_tree.insert('', END, values=record)

        self.record.pack(side=LEFT, padx=30)

if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "united")
    TinyCashBook(app)
    app.mainloop()
