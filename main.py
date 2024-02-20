from tkinter import *
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
            date_label.config(text=f"You Picked:  {date.entry.get()}")

        # Add record
        def add_record():
            values = (date.entry.get(), allowance_source_entry.get(), expense_combo.get(),
                      amount_allowance_entry.get(), amount_expense_entry.get(),)
            record_tree.insert("", END, values=values)
            self.input_data.append(values)
            # Clear entry box
            date.entry.delete(0, END)
            allowance_source_entry.delete(0, END)
            amount_allowance_entry.delete(0, END)
            expense_combo.delete(0, END)
            amount_expense_entry.delete(0, END)
            # Add to CSV file
            with open("record_data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(values)

        # Delete record
        def delete_record():
            delete_item = record_tree.selection()[0]
            record_tree.delete(delete_item)
            # Identify the index of the row that want to delete from the CSV file(delete_item output: I004)
            # "I" is excluded and only the numeric part is retrieved, subtracting 1 to convert to a 0-based index
            index_to_delete = int(delete_item[1:]) - 1
            # Delete the corresponding row from the self.input_data list
            del self.input_data[index_to_delete]
            # Overwrite CSV file with new data
            with open("record_data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.input_data)
            allowance_button.config(text="ADD", command=clear_entries)
            expense_button.config(text="ADD", command=clear_entries)
            # Clear entry box
            date.entry.delete(0, END)
            allowance_source_entry.delete(0, END)
            amount_allowance_entry.delete(0, END)
            expense_combo.delete(0, END)
            amount_expense_entry.delete(0, END)

        # Clear entry box
        def clear_entries():
            allowance_button.config(text="ADD", command=clear_entries)
            expense_button.config(text="ADD", command=clear_entries)
            date.entry.delete(0, END)
            allowance_source_entry.delete(0, END)
            amount_allowance_entry.delete(0, END)
            expense_combo.delete(0, END)
            amount_expense_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry box
            allowance_button.config(text="UPDATE", command=update_record)
            expense_button.config(text="UPDATE", command=update_record)
            date.entry.delete(0, END)
            allowance_source_entry.delete(0, END)
            amount_allowance_entry.delete(0, END)
            expense_combo.delete(0, END)
            amount_expense_entry.delete(0, END)
            # Get record
            selected = record_tree.focus()
            values = record_tree.item(selected, "values")
            # output to entry boxes
            date.entry.insert(0, values[0])
            allowance_source_entry.insert(0, values[1])
            amount_allowance_entry.insert(0, values[3])
            expense_combo.insert(0, values[2])
            amount_expense_entry.insert(0, values[4])

        # Update record
        def update_record():
            selected = record_tree.focus()
            record_tree.item(selected, text="", values=(
            date.entry.get(), allowance_source_entry.get(), expense_combo.get(),
            amount_allowance_entry.get(), amount_expense_entry.get(),))

            new_values = (date.entry.get(), allowance_source_entry.get(), expense_combo.get(),
                          amount_allowance_entry.get(), amount_expense_entry.get())
            # Index that want to update
            index_to_update = int(selected[1:]) - 1
            # Update input_data list with new
            self.input_data[index_to_update] = list(new_values)

            with open("record_data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.input_data)
            # Clear entry box
            allowance_button.config(text="ADD", command=update_record)
            expense_button.config(text="ADD", command=update_record)
            date.entry.delete(0, END)
            allowance_source_entry.delete(0, END)
            amount_allowance_entry.delete(0, END)
            expense_combo.delete(0, END)
            amount_expense_entry.delete(0, END)

        # Calculate
        def calc_cost():
            total_allowance = 0
            total_spending = 0
            savings = 0
            for item in self.input_data:
                if item[3] != '':
                    total_allowance += int(item[3])
                    savings += int(item[3])
                if item[4] != '':
                    total_spending += int(item[4])
                    savings -= int(item[4])

            remain_label.config(
                text=f"Total Allowance:  ${total_allowance}   Total Spending:  ${total_spending}   Savings:  ${savings}")

        # Create pie chart
        def show_graph():
            count_items = {"Snacks": 0, "Books": 0, "Game/Toy": 0, "Gifts": 0, "Clothing": 0}
            with open("record_data.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] != "":
                        if row[2] == "Snacks":
                            count_items["Snacks"] += 1
                        elif row[2] == "Books":
                            count_items["Books"] += 1
                        elif row[2] == "Game/Toy":
                            count_items["Game/Toy"] += 1
                        elif row[2] == "Gifts":
                            count_items["Gifts"] += 1
                        elif row[2] == "Clothing":
                            count_items["Clothing"] += 1

            numbers = list(count_items.values())
            items = list(count_items.keys())

            fig, ax = plt.subplots()
            ax.pie(numbers, labels=items, autopct='%1.1f%%')
            ax.set_title('Spending pie chart')

            canvas = FigureCanvasTkAgg(fig, graph_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(10, 20), sticky="w")

        ##### GUI ################################################
        main_frame = tb.Frame(self)
        main_frame.pack(padx=10)
        # ------ Date Entry -------------------------------
        date_entry = tb.LabelFrame(main_frame, text="📆Date📆", style='warning.TLabelframe')
        date_entry.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        date = tb.DateEntry(date_entry, bootstyle="warning", firstweekday=6, dateformat="%Y/%m/%d")
        date.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))

        date_button = tb.Button(date_entry, text='Get Date', style="warning", width=10, command=get_date)
        date_button.grid(row=0, column=2, padx=10, pady=(10, 20))

        date_label = tb.Label(date_entry, text="You Picked:  ")
        date_label.grid(row=0, column=3, padx=10, pady=(10, 20))

        # ------ Input frame ------------------------------
        # Allowance form
        allowance_frame = tb.LabelFrame(main_frame, text="💰Allowance💰", style='info.TLabelframe')
        allowance_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Source label
        allowance_source_label = tb.Label(allowance_frame, text="💡How did you get?          ")
        allowance_source_label.grid(row=1, column=0, padx=10, pady=(10, 20), sticky="w")
        # Source entry
        allowance_source_entry = tb.Entry(allowance_frame, style='info')
        allowance_source_entry.grid(row=1, column=1, padx=10, pady=(10, 20))
        # Amount label
        amount_allowance_label = tb.Label(allowance_frame, text="💴Amount (How much?)")
        amount_allowance_label.grid(row=1, column=2, padx=10, pady=(10, 20), sticky="w")
        # Amount entry
        amount_allowance_entry = tb.Entry(allowance_frame, style='info')
        amount_allowance_entry.grid(row=1, column=3, padx=10, pady=(10, 20))
        # Allowance add button
        allowance_button = tb.Button(allowance_frame, text="ADD", width=10, style="info", command=add_record)
        allowance_button.grid(row=1, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        # ------ Expense form ----------------------------
        expense_frame = tb.LabelFrame(main_frame, text="💸Spending💸", style='danger.TLabelframe')
        expense_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Expense label
        expense_item_label = tb.Label(expense_frame, text="🍟What did you use it for?")
        expense_item_label.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="w")
        # Expense entry
        # Dropdown options
        items = ["", "Snacks", "Books", "Game/Toy", "Gifts", "Clothing"]
        # Create Combobox
        expense_combo = tb.Combobox(expense_frame, style="danger", values=items)
        expense_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        # Set Combo Default
        expense_combo.current(0)

        # expense_item_entry = tb.Entry(expense_frame, style='danger')
        # expense_item_entry.grid(row=2, column=1, padx=10, pady=(10, 20))
        # Amount label
        amount_expense_label = Label(expense_frame, text="💴Amount (How much?)")
        amount_expense_label.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="w")
        # Amount entry
        amount_expense_entry = tb.Entry(expense_frame, style='danger')
        amount_expense_entry.grid(row=2, column=3, padx=10, pady=(10, 20))
        # Expense add button
        expense_button = tb.Button(expense_frame, text="ADD", width=10, style="danger", command=add_record)
        expense_button.grid(row=2, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        # ------ Record treeview --------------------------
        tree_frame = tb.LabelFrame(main_frame, text="💿History💿", style='success.TLabelframe')
        tree_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 0))
        columns = ("date", "source", "item", "allowance", "spending")

        # Create Treeview
        record_tree = tb.Treeview(tree_frame, style="success", selectmode="extended", columns=columns,
                                       show="headings")
        record_tree.pack(fill="x", expand="yes", padx=10, pady=10)
        # Format columns
        record_tree.column('date', width=80, anchor="w")
        record_tree.column('source', width=180, anchor="w")
        record_tree.column('item', width=180, anchor="w")
        record_tree.column('allowance', width=80, anchor="e")
        record_tree.column('spending', width=80, anchor="e")
        # Define headings
        record_tree.heading('date', text="Date", anchor="w")
        record_tree.heading('source', text="How did you get?", anchor="w")
        record_tree.heading('item', text="What did you use it for?", anchor="w")
        record_tree.heading('allowance', text="Allowance", anchor="e")
        record_tree.heading('spending', text="Spending", anchor="e")

        # Add sample data To Treeview
        for record in self.input_data:
            record_tree.insert('', END, values=record)

        # ------ Total remain allowance ----------------------------
        remain_frame = tb.LabelFrame(main_frame, text="🐖Balance🐖", style='success.TLabelframe')
        remain_frame.pack(anchor="w", expand="yes", padx=20, pady=(0, 10))

        remain_label = tb.Label(remain_frame,
                                     text=f"Total Allowance:  ${self.total_allowance}   Total Spending:  ${self.total_allowance}   Savings:  ${self.savings}")
        remain_label.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="e")

        reload_btn = tb.Button(remain_frame, text="RELOAD", width=10, style="success", command=calc_cost)
        reload_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

        # ------ Commands ----------------------------
        btn_frame = tb.LabelFrame(main_frame, text="🖋Commands🗑", style='light.TLabelframe')
        btn_frame.pack(anchor="w", padx=20, pady=(0, 20))
        # Update button
        graph_btn = tb.Button(btn_frame, text="SHOW GRAPHS", width=15, style="primary", command=show_graph)
        graph_btn.grid(row=0, column=0, padx=20, pady=(10, 20))
        # Delete button
        delete_btn = tb.Button(btn_frame, text="DELETE", width=15, style="danger", command=delete_record)
        delete_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))
        # Clear button
        clear_btn = tb.Button(btn_frame, text="CLEAR", width=15, style="secondary", command=clear_entries)
        clear_btn.grid(row=0, column=2, padx=(0, 20), pady=(10, 20))

        # Bind the treeview
        record_tree.bind("<ButtonRelease-1>", select_record)

        # ------ Show Graphs ----------------------------
        graph_frame = tb.LabelFrame(main_frame, text="📈Graphs📊", style='info.TLabelframe')
        graph_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        # Pie chart label
        pie_label = tb.Label(graph_frame, text="Spending pie chart")
        pie_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="w")


if __name__ == "__main__":
    app = tb.Window("TinyCashBook", "superhero")
    TinyCashBook(app)
    app.mainloop()
