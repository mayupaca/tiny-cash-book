from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import csv


class TinyCashBook(tb.Frame):
    def __init__(self, master):  # master is the widget is the parent of the Tkinter window.
        super().__init__(master, padding=(20, 20))
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        self.style = tb.Style(theme='sandstone')
        # Title
        self.app_title = tb.Label(self, text="👛Tiny Cash Book👛", font=("Helvetica", 20), foreground="#3D5361", )
        self.app_title.pack(padx=50, pady=(0, 30), anchor="w")

        # Hello [user name]

        ########## Date Entry ###########################################
        def get_date():
            # Grab The Date
            self.date_label.config(text=f"You Picked: {self.date.entry.get()}")

        self.date_entry = tb.Frame(self)
        self.date_entry.pack(anchor="w")

        self.date = tb.DateEntry(self.date_entry, bootstyle="primary", firstweekday=6, dateformat="%Y/%m/%d")
        self.date.grid(row=0, column=0, padx=(30, 0))

        self.date_button = tb.Button(self.date_entry, text='Get Date', style="primary", command=get_date)
        self.date_button.grid(row=0, column=2, padx=10)

        self.date_label = tb.Label(self.date_entry, text="You Picked: ")
        self.date_label.grid(row=0, column=3)

        ############# Input frame #######################################
        self.input_frame = tb.Frame(self)
        self.input_frame.pack()
        # Allowance form -------------------------------------------------
        self.allowance_frame = tb.LabelFrame(self.input_frame, text="💰Allowance💰", style='info.TLabelframe')
        self.allowance_frame.grid(row=1, column=0, padx=30)
        # Source label
        self.allowance_source_label = tb.Label(self.allowance_frame, text="💡Source (How did you get?)")
        self.allowance_source_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # Source entry
        self.allowance_source_entry = tb.Entry(self.allowance_frame, style='info')
        self.allowance_source_entry.grid(row=1, column=1, padx=10, pady=10)
        # Amount label
        self.amount_allowance_label = tb.Label(self.allowance_frame, text="💴Amount (How much?)")
        self.amount_allowance_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        # Amount entry
        self.amount_allowance_entry = tb.Entry(self.allowance_frame, style='info', background="red", foreground='green')
        self.amount_allowance_entry.grid(row=2, column=1, padx=10, pady=10)
        # Allowance add button
        self.allowance_button = tb.Button(self.allowance_frame, text="ADD", width=10, style="info outline")
        self.allowance_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="news")

        # Expense form ----------------------------------------------------
        self.expense_frame = tb.LabelFrame(self.input_frame, text="💸Spending💸", style='warning.TLabelframe')
        self.expense_frame.grid(row=1, column=1, padx=30, pady=30)
        # Expense label
        self.expense_item_label = tb.Label(self.expense_frame, text="🍟Reason (What did you use?)")
        self.expense_item_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # Expense entry
        self.expense_item_entry = tb.Entry(self.expense_frame, style='warning')
        self.expense_item_entry.grid(row=1, column=1, padx=10, pady=10)
        # Amount label
        self.amount_expense_label = Label(self.expense_frame, text="💴Amount (How much?)")
        self.amount_expense_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        # Amount entry
        self.amount_expense_entry = tb.Entry(self.expense_frame, style='warning')
        self.amount_expense_entry.grid(row=2, column=1, padx=10, pady=10)
        # Expense add button
        self.expense_button = tb.Button(self.expense_frame, text="ADD", width=10, style="warning outline")
        self.expense_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="news")

        ########### Record treeview ###########################################
        self.record_frame = tb.Frame(self)
        self.record_frame.pack()
        self.columns = ("date", "source_or_item", "allowance", "spending")
        # Create Treeview
        self.record_tree = tb.Treeview(style="success", columns=self.columns, show="headings")
        self.record_tree.pack(padx=50, pady=(0, 50), anchor="w")
        # Format columns
        self.record_tree.column('date', width=150, anchor=W)
        self.record_tree.column('source_or_item', width=350, anchor=W)
        self.record_tree.column('allowance', width=150, anchor=E)
        self.record_tree.column('spending', width=150, anchor=E)
        # Define headings
        self.record_tree.heading('date', text="Date", anchor=W)
        self.record_tree.heading('source_or_item', text="Source or Item", anchor=W)
        self.record_tree.heading('allowance', text="Allowance", anchor=E)
        self.record_tree.heading('spending', text="Spending", anchor=E)
        # Sample Data
        self.input_data = [
            ('2024/1/1', 'Did some weeding in the garden', 10, " - "),
            ('2024/1/5', 'Bought snacks', " - ", 5),
            ('2024/1/10', 'Assisted in cleaning up dishes', 5, " - "),
            ('2024/1/14', 'Sorted out recyclables in the house.', 5, " - "),
        ]
        # Add Data To Treeview
        for record in self.input_data:
            self.record_tree.insert('', END, values=record)

        ########### Edit and delete  ###########################################
        self.button_frame = tb.Frame(self)
        self.button_frame.pack(anchor='w', padx=(10, 0))
        # Delete button
        self.edit_btn = tb.Button(self.button_frame, text="EDIT", width=10, style="success")
        self.edit_btn.grid(row=0, column=0, padx=20)
        # Delete button
        self.delete_btn = tb.Button(self.button_frame, text="DELETE", width=10, style="danger")
        self.delete_btn.grid(row=0, column=1, padx=20)


if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "sandstone")
    TinyCashBook(app)
    app.mainloop()
