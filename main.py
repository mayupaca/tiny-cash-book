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
        self.app_title.pack(padx=50, pady=(0, 10), anchor="w")
        # Sample Data
        self.input_data = [
            ['2024/1/1', 'Did some weeding in the garden', '', 10, '', ],
            ['2024/1/5', '', 'Bought snacks', '', 5, ],
            ['2024/1/10', 'Assisted in cleaning up dishes', '', 5, ''],
            ['2024/1/14', 'Sorted out recyclables in the house.', '', 5, ''],
        ]

        # Get date
        def get_date():
            # Grab The Date
            self.date_label.config(text=f"You Picked: {self.date.entry.get()}")

        # Add record
        def add_record():
            values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_item_entry.get(),
            self.amount_allowance_entry.get(), self.amount_expense_entry.get(),)
            self.record_tree.insert("", END, values=values)
            self.input_data.append(values)
            # Clear entry box
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_item_entry.delete(0, END)
            self.amount_expense_entry.delete(0, END)

        # Delete record
        def delete_record():
            delete_item = self.record_tree.selection()[0]
            self.record_tree.delete(delete_item)

        # Clear entry box
        def clear_entries():
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_item_entry.delete(0, END)
            self.amount_expense_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry box
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_item_entry.delete(0, END)
            self.amount_expense_entry.delete(0, END)
            # Get record
            selected = self.record_tree.focus()
            self.values = self.record_tree.item(selected, "values")
            # output to entry boxes
            self.date.entry.insert(0, self.values[0])
            self.allowance_source_entry.insert(0, self.values[1])
            self.amount_allowance_entry.insert(0, self.values[3])
            self.expense_item_entry.insert(0, self.values[2])
            self.amount_expense_entry.insert(0, self.values[4])

        # Update record
        def update_record():
            selected = self.record_tree.focus()
            self.record_tree.item(selected, text="", values=(self.date.entry.get(), self.allowance_source_entry.get(), self.expense_item_entry.get(), self.amount_allowance_entry.get(),  self.amount_expense_entry.get(),))
            # Clear entry box
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_item_entry.delete(0, END)
            self.amount_expense_entry.delete(0, END)

    # ------ Calculate -------------------------------
        def calc_cost():
            total_allowance = 0
            total_spending = 0
            remaining = 0
            for item in self.input_data:
                if item[3] != '':
                    total_allowance += int(item[3])
                if item[4] != '':
                    total_spending += int(item[4])
                if item[3] != '':
                    remaining += int(item[3])
                elif item[4] != '':
                    remaining -= int(item[4])
            self.remain_label.config(text=f"Total Allowance:  ${total_allowance}   Total Spending:  ${total_spending}   Remaining Allowance:  ${remaining}")

    ##### GUI ################################################
        self.main_frame = tb.Frame(self)
        self.main_frame.pack(padx=10)
    # ------ Date Entry -------------------------------
        self.date_entry = tb.LabelFrame(self.main_frame, text="📆Date📆", style='primary.TLabelframe')
        self.date_entry.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        self.date = tb.DateEntry(self.date_entry, bootstyle="primary", firstweekday=6, dateformat="%Y/%m/%d")
        self.date.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))

        self.date_button = tb.Button(self.date_entry, text='Get Date', style="primary", width=10, command=get_date)
        self.date_button.grid(row=0, column=2, padx=10, pady=(10, 20))

        self.date_label = tb.Label(self.date_entry, text="You Picked: ")
        self.date_label.grid(row=0, column=3, padx=10, pady=(10, 20))

    # ------ Input frame ------------------------------
        # Allowance form
        self.allowance_frame = tb.LabelFrame(self.main_frame, text="💰Allowance💰", style='info.TLabelframe')
        self.allowance_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Source label
        self.allowance_source_label = tb.Label(self.allowance_frame, text="💡Who or How did you get? ")
        self.allowance_source_label.grid(row=1, column=0, padx=10, pady=(10, 20), sticky="w")
        # Source entry
        self.allowance_source_entry = tb.Entry(self.allowance_frame, style='info')
        self.allowance_source_entry.grid(row=1, column=1, padx=10, pady=(10, 20))
        # Amount label
        self.amount_allowance_label = tb.Label(self.allowance_frame, text="💴Amount (How much?)")
        self.amount_allowance_label.grid(row=1, column=2, padx=10, pady=(10, 20), sticky="w")
        # Amount entry
        self.amount_allowance_entry = tb.Entry(self.allowance_frame, style='info')
        self.amount_allowance_entry.grid(row=1, column=3, padx=10, pady=(10, 20))
        # Allowance add button
        self.allowance_button = tb.Button(self.allowance_frame, text="ADD", width=10, style="info", command=add_record)
        self.allowance_button.grid(row=1, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

    # ------ Expense form ----------------------------
        self.expense_frame = tb.LabelFrame(self.main_frame, text="💸Spending💸", style='danger.TLabelframe')
        self.expense_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Expense label
        self.expense_item_label = tb.Label(self.expense_frame, text="🍟Why did you use for?        ")
        self.expense_item_label.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="w")
        # Expense entry
        self.expense_item_entry = tb.Entry(self.expense_frame, style='danger')
        self.expense_item_entry.grid(row=2, column=1, padx=10, pady=(10, 20))
        # Amount label
        self.amount_expense_label = Label(self.expense_frame, text="💴Amount (How much?)")
        self.amount_expense_label.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="w")
        # Amount entry
        self.amount_expense_entry = tb.Entry(self.expense_frame, style='danger')
        self.amount_expense_entry.grid(row=2, column=3, padx=10, pady=(10, 20))
        # Expense add button
        self.expense_button = tb.Button(self.expense_frame, text="ADD", width=10, style="danger", command=add_record)
        self.expense_button.grid(row=2, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

    # ------ Record treeview --------------------------
        self.tree_frame = tb.LabelFrame(self.main_frame, text="💿Record💿", style='success.TLabelframe')
        self.tree_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 0))
        self.columns = ("date", "source", "item", "allowance", "spending")

        # Create Treeview
        self.record_tree = tb.Treeview(self.tree_frame, style="success", selectmode="extended", columns=self.columns, show="headings")
        self.record_tree.pack(fill="x", expand="yes", padx=10, pady=10)
        # Format columns
        self.record_tree.column('date', width=80, anchor=W)
        self.record_tree.column('source', width=180, anchor=W)
        self.record_tree.column('item', width=180, anchor=W)
        self.record_tree.column('allowance', width=80, anchor=E)
        self.record_tree.column('spending', width=80, anchor=E)
        # Define headings
        self.record_tree.heading('date', text="Date", anchor=W)
        self.record_tree.heading('source', text="Who or How", anchor=W)
        self.record_tree.heading('item', text="Purchased Item", anchor=W)
        self.record_tree.heading('allowance', text="Allowance", anchor=E)
        self.record_tree.heading('spending', text="Spending", anchor=E)

        # Add sample data To Treeview
        for record in self.input_data:
            self.record_tree.insert('', END, values=record)

    # ------ Total remain allowance ----------------------------
        self.remain_frame = tb.LabelFrame(self.main_frame, text="🐖Record Total and Remaining🐖", style='success.TLabelframe')
        self.remain_frame.pack(anchor="e", expand="yes", padx=20, pady=(0, 10))

        self.remain_label = tb.Label(self.remain_frame, text="Total Allowance:   Total Spending:   Remaining Allowance:  ")
        self.remain_label.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="e")

        self.reload_btn = tb.Button(self.remain_frame, text="RELOAD", width=10, style="success", command=calc_cost)
        self.reload_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

    # ------ Update and delete ----------------------------
        self.btn_frame = tb.LabelFrame(self.main_frame, text="🖋Record Commands🗑", style='warning.TLabelframe')
        self.btn_frame.pack(anchor="e", padx=20, pady=(0, 20))
        # Update button
        self.update_btn = tb.Button(self.btn_frame, text="UPDATE", width=10, style="warning", command=update_record)
        self.update_btn.grid(row=0, column=0, padx=20, pady=(10, 20))
        # Delete button
        self.delete_btn = tb.Button(self.btn_frame, text="DELETE", width=10, style="danger", command=delete_record)
        self.delete_btn.grid(row=0, column=1, padx=(0,20), pady=(10, 20))
        # Clear button
        self.clear_btn = tb.Button(self.btn_frame, text="CLEAR", width=10, style="secondary", command=clear_entries)
        self.clear_btn.grid(row=0, column=2, padx=(0,20), pady=(10, 20))

        # Bind the treeview
        self.record_tree.bind("<ButtonRelease-1>", select_record)

if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "sandstone")
    TinyCashBook(app)
    app.mainloop()