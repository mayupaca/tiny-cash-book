from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import csv
import matplotlib.pyplot as plt


class TinyCashBook(tb.Frame):
    def __init__(self, master):  # master is the widget is the parent of the Tkinter window.
        super().__init__(master, padding=(20, 20))
        self.pack(fill=BOTH, expand=YES)
        # self.master = master
        # self.style = tb.Style(theme='sandstone')
        # Title
        self.app_title = tb.Label(self, text="👛Tiny Cash Book👛", font=("Helvetica", 18), foreground="#d0d0d0")
        self.app_title.pack(padx=50, pady=(0, 5), anchor="w")
        self.separator = tb.Separator(self, style="light")
        self.separator.pack(fill="x", expand="yes", padx=20, pady=(0, 20))
        # Sample Data
        self.input_data = [
            ['2024/02/01', 'Gift from Grand mother', '', 20, ''],
            ['2024/02/04', 'Weekly allowance', '', 5, ''],
            ['2024/02/06', '', 'Gifts', '', 15],
            ['2024/02/07', '', 'Snacks', '', 3],
            ['2024/02/08', '', 'Books', '', 5],
            ['2024/02/10', 'Cleaning up dishes', '', 5, ''],
            ['2024/02/11', 'Weekly allowance', '', '5', ''],
            ['2024/02/13', '', 'Snacks', '', 5, ],
            ['2024/02/14', 'Sorted out recyclables', '', 5, ''],
        ]
        self.total_allowance = 0
        self.total_spending = 0
        self.savings = 0

        self.count_items = {"Snacks": 0, "Books": 0, "Game/Toy": 0, "Gifts": 0, "Clothing": 0}

        # ------ Methods -------------------------------
        # Get date
        def get_date():
            # Grab The Date
            self.date_label.config(text=f"You Picked:  {self.date.entry.get()}")

        # Add record
        def add_record():
            values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
                      self.amount_allowance_entry.get(), self.amount_expense_entry.get(),)
            self.record_tree.insert("", END, values=values)
            self.input_data.append(values)
            # Clear entry box
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_combo.delete(0, END)
            self.amount_expense_entry.delete(0, END)
            # Add to CSV file
            with open("record_data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(values)

        # Delete record
        def delete_record():
            delete_item = self.record_tree.selection()[0]
            self.record_tree.delete(delete_item)
            # Identify the index of the row that want to delete from the CSV file(delete_item output: I004)
            # "I" is excluded and only the numeric part is retrieved, subtracting 1 to convert to a 0-based index
            index_to_delete = int(delete_item[1:]) - 1
            # Delete the corresponding row from the self.input_data list
            del self.input_data[index_to_delete]
            # Overwrite CSV file with new data
            with open("record_data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.input_data)
            self.allowance_button.config(text="ADD", command=clear_entries)
            self.expense_button.config(text="ADD", command=clear_entries)
            # Clear entry box
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_combo.delete(0, END)
            self.amount_expense_entry.delete(0, END)

        # Clear entry box
        def clear_entries():
            self.allowance_button.config(text="ADD", command=clear_entries)
            self.expense_button.config(text="ADD", command=clear_entries)
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_combo.delete(0, END)
            self.amount_expense_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry box
            self.allowance_button.config(text="UPDATE", command=update_record)
            self.expense_button.config(text="UPDATE", command=update_record)
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_combo.delete(0, END)
            self.amount_expense_entry.delete(0, END)
            # Get record
            selected = self.record_tree.focus()
            self.values = self.record_tree.item(selected, "values")
            # output to entry boxes
            self.date.entry.insert(0, self.values[0])
            self.allowance_source_entry.insert(0, self.values[1])
            self.amount_allowance_entry.insert(0, self.values[3])
            self.expense_combo.insert(0, self.values[2])
            self.amount_expense_entry.insert(0, self.values[4])

        # Update record
        def update_record():
            selected = self.record_tree.focus()
            self.record_tree.item(selected, text="", values=(
            self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
            self.amount_allowance_entry.get(), self.amount_expense_entry.get(),))

            new_values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
                          self.amount_allowance_entry.get(), self.amount_expense_entry.get())
            # Index that want to update
            index_to_update = int(selected[1:]) - 1
            # Update self.input_data list with new
            self.input_data[index_to_update] = list(new_values)

            with open("record_data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.input_data)
            # Clear entry box
            self.allowance_button.config(text="ADD", command=update_record)
            self.expense_button.config(text="ADD", command=update_record)
            self.date.entry.delete(0, END)
            self.allowance_source_entry.delete(0, END)
            self.amount_allowance_entry.delete(0, END)
            self.expense_combo.delete(0, END)
            self.amount_expense_entry.delete(0, END)

        # Calculate
        def calc_cost():
            self.total_allowance = 0
            self.total_spending = 0
            self.savings = 0
            for item in self.input_data:
                if item[3] != '':
                    self.total_allowance += int(item[3])
                    self.savings += int(item[3])
                if item[4] != '':
                    self.total_spending += int(item[4])
                    self.savings -= int(item[4])

            self.remain_label.config(
                text=f"Total Allowance:  ${self.total_allowance}   Total Spending:  ${self.total_spending}   Savings:  ${self.savings}")

        def show_graphs():
            self.count_items = {"Snacks": 0, "Books": 0, "Game/Toy": 0, "Gifts": 0, "Clothing": 0}
            with open("record_data.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] != "":
                        if row[2] == "Snacks":
                            self.count_items["Snacks"] += 1
                        elif row[2] == "Books":
                            self.count_items["Books"] += 1
                        elif row[2] == "Game/Toy":
                            self.count_items["Game/Toy"] += 1
                        elif row[2] == "Gifts":
                            self.count_items["Gifts"] += 1
                        elif row[2] == "Clothing":
                            self.count_items["Clothing"] += 1

            numbers = list(self.count_items.values())
            items = list(self.count_items.keys())

            fig, ax = plt.subplots()
            ax.pie(numbers, labels=items, autopct='%1.1f%%')
            plt.show()

        ##### GUI ################################################
        self.main_frame = tb.Frame(self)
        self.main_frame.pack(padx=10)
        # ------ Date Entry -------------------------------
        self.date_entry = tb.LabelFrame(self.main_frame, text="📆Date📆", style='warning.TLabelframe')
        self.date_entry.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        self.date = tb.DateEntry(self.date_entry, bootstyle="warning", firstweekday=6, dateformat="%Y/%m/%d")
        self.date.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))

        self.date_button = tb.Button(self.date_entry, text='Get Date', style="warning", width=10, command=get_date)
        self.date_button.grid(row=0, column=2, padx=10, pady=(10, 20))

        self.date_label = tb.Label(self.date_entry, text="You Picked:  ")
        self.date_label.grid(row=0, column=3, padx=10, pady=(10, 20))

        # ------ Input frame ------------------------------
        # Allowance form
        self.allowance_frame = tb.LabelFrame(self.main_frame, text="💰Allowance💰", style='info.TLabelframe')
        self.allowance_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Source label
        self.allowance_source_label = tb.Label(self.allowance_frame, text="💡How did you get?          ")
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
        self.expense_item_label = tb.Label(self.expense_frame, text="🍟What did you use it for?")
        self.expense_item_label.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="w")
        # Expense entry
        # Dropdown options
        self.items = ["", "Snacks", "Books", "Game/Toy", "Gifts", "Clothing"]
        # Create Combobox
        self.expense_combo = tb.Combobox(self.expense_frame, style="danger", values=self.items)
        self.expense_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        # Set Combo Default
        self.expense_combo.current(0)

        # self.expense_item_entry = tb.Entry(self.expense_frame, style='danger')
        # self.expense_item_entry.grid(row=2, column=1, padx=10, pady=(10, 20))
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
        self.tree_frame = tb.LabelFrame(self.main_frame, text="💿History💿", style='success.TLabelframe')
        self.tree_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 0))
        self.columns = ("date", "source", "item", "allowance", "spending")

        # Create Treeview
        self.record_tree = tb.Treeview(self.tree_frame, style="success", selectmode="extended", columns=self.columns,
                                       show="headings")
        self.record_tree.pack(fill="x", expand="yes", padx=10, pady=10)
        # Format columns
        self.record_tree.column('date', width=80, anchor="w")
        self.record_tree.column('source', width=180, anchor="w")
        self.record_tree.column('item', width=180, anchor="w")
        self.record_tree.column('allowance', width=80, anchor="e")
        self.record_tree.column('spending', width=80, anchor="e")
        # Define headings
        self.record_tree.heading('date', text="Date", anchor="w")
        self.record_tree.heading('source', text="How did you get?", anchor="w")
        self.record_tree.heading('item', text="What did you use it for?", anchor="w")
        self.record_tree.heading('allowance', text="Allowance", anchor="e")
        self.record_tree.heading('spending', text="Spending", anchor="e")

        # Add sample data To Treeview
        for record in self.input_data:
            self.record_tree.insert('', END, values=record)

        # ------ Total remain allowance ----------------------------
        self.remain_frame = tb.LabelFrame(self.main_frame, text="🐖Balance🐖", style='success.TLabelframe')
        self.remain_frame.pack(anchor="w", expand="yes", padx=20, pady=(0, 10))

        self.remain_label = tb.Label(self.remain_frame,
                                     text=f"Total Allowance:  ${self.total_allowance}   Total Spending:  ${self.total_allowance}   Savings:  ${self.savings}")
        self.remain_label.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="e")

        self.reload_btn = tb.Button(self.remain_frame, text="RELOAD", width=10, style="success", command=calc_cost)
        self.reload_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

        # ------ Commands ----------------------------
        self.btn_frame = tb.LabelFrame(self.main_frame, text="🖋Commands🗑", style='light.TLabelframe')
        self.btn_frame.pack(anchor="w", padx=20, pady=(0, 20))
        # Update button
        self.graph_btn = tb.Button(self.btn_frame, text="SHOW GRAPHS", width=15, style="primary", command=show_graphs)
        self.graph_btn.grid(row=0, column=0, padx=20, pady=(10, 20))
        # Delete button
        self.delete_btn = tb.Button(self.btn_frame, text="DELETE", width=15, style="danger", command=delete_record)
        self.delete_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))
        # Clear button
        self.clear_btn = tb.Button(self.btn_frame, text="CLEAR", width=15, style="secondary", command=clear_entries)
        self.clear_btn.grid(row=0, column=2, padx=(0, 20), pady=(10, 20))

        # Bind the treeview
        self.record_tree.bind("<ButtonRelease-1>", select_record)

        # ------ Show Graphs ----------------------------
        self.graph_frame = tb.LabelFrame(self.main_frame, text="📈Graphs📊", style='info.TLabelframe')
        self.graph_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Pie chart label
        self.pie_label = tb.Label(self.graph_frame, text="Spending pie chart")
        self.pie_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="w")

        # Line graph label
        self.line_label = tb.Label(self.graph_frame, text="Spending line graph")
        self.line_label.grid(row=0, column=1, padx=10, pady=(10, 20), sticky="w")


if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "superhero")
    TinyCashBook(app)
    app.mainloop()
