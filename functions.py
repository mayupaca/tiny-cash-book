import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_date(self):
    self.date_label.config(text=f"You Picked:  {self.date.entry.get()}")


def clear_entries(self):
    # 0 is the start position of the text,
    self.date.entry.delete(0, "end")
    self.allowance_source_entry.delete(0, "end")
    self.amount_allowance_entry.delete(0, "end")
    self.expense_combo.set("")
    self.amount_expense_entry.delete(0, "end")
    self.allowance_button.config(text="ADD", command=lambda: add_record(self))
    self.expense_button.config(text="ADD", command=lambda: add_record(self))


def select_record(self, event):
    # Clear entry box
    clear_entries(self)
    # Get record
    selected = self.record_tree.focus() # Returns the ID of the currently focused item (selected item) in the tree view.
    print(selected)
    values = self.record_tree.item(selected, "values")
    # Obtains the treeview item data corresponding to the specified item ID (selected).
    # The "values" argument here specifies that the column data for the item is to be retrieved.
    self.allowance_button.config(text="UPDATE", command=lambda: update_record(self))
    self.expense_button.config(text="UPDATE", command=lambda: update_record(self))
    # output to entry boxes
    self.date.entry.insert(0, values[0])
    self.allowance_source_entry.insert(0, values[1])
    self.amount_allowance_entry.insert(0, values[3])
    self.expense_combo.set(values[2])
    self.amount_expense_entry.insert(0, values[4])
    # .insert(index, string) - Used to insert text into an entry widget,
    # where index specifies the position to insert and string is the text to be inserted.
    # values[0] is the data in the first column (in this case date) of the selected treeview item.


def add_record(self):
    values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
              self.amount_allowance_entry.get(), self.amount_expense_entry.get(),)
    self.record_tree.insert("", "end", values=values)
    self.sample_data.append(values)
    # Clear entry box
    clear_entries(self)
    # Add to CSV file
    with open("record_data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(values)


def delete_record(self):
    selected = self.record_tree.focus()
    self.record_tree.delete(selected)
    # The item IDs in Tkinter's treeview are usually in the form I001...,
    # with the 'I' followed by a number. The [1:] is used to extract only the numeric part of it.
    # Tkinter item ID counts starting from 1. Indexes start at 0, so subtract 1.
    index_to_delete = int(selected[1:]) - 1
    # Delete the corresponding row from the self.sample_data list
    del self.sample_data[index_to_delete]
    # Overwrite CSV file with new data
    with open("record_data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(self.sample_data)
    # Clear entry box
    clear_entries(self)


def update_record(self):
    selected = self.record_tree.focus()
    new_values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
                  self.amount_allowance_entry.get(), self.amount_expense_entry.get())
    self.record_tree.item(selected, values=new_values)
    # Index that want to update
    index_to_update = int(selected[1:]) - 1
    # Update self.sample_data list with new
    self.sample_data[index_to_update] = list(new_values)
    with open("record_data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(self.sample_data)
    self.allowance_button.config(text="ADD", command=lambda: add_record(self))
    self.expense_button.config(text="ADD", command=lambda: add_record(self))
    # Clear entry box
    clear_entries(self)


def calc_cost(self):
    total_allowance = 0
    total_spending = 0
    savings = 0
    for item in self.sample_data:
        if item[3] != '':
            total_allowance += int(item[3])
            savings += int(item[3])
        if item[4] != '':
            total_spending += int(item[4])
            savings -= int(item[4])
    self.remain_label.config(text=f"Total Allowance:  ${total_allowance}   Total Spending:  ${total_spending}   Savings:  ${savings}")


def show_graph(self):
    # 0%のアイテムを除外するために、カウントが0より大きいアイテムのみをフィルタリング
    count_items = {"Snacks": 0, "Clothing": 0, "Game/Toy": 0, "Gifts": 0, "Books": 0}
    for item in self.sample_data:
        if item[2] in count_items:
            count_items[item[2]] += 1

    # Dictionary only items greater than 0
    filtered_items = {}
    for key, value in count_items.items():
        if value > 0:
            filtered_items[key] = value

    counts = list(filtered_items.values())
    items = list(filtered_items.keys())

    fig, ax = plt.subplots(figsize=(3.5, 3))
    if counts:  # 数値リストが空でない場合のみ描画
        ax.pie(counts, labels=items, autopct='%1.1f%%')
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

