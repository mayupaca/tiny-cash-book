import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_date(self):
    self.date_label.config(text=f"You Picked:  {self.date.entry.get()}")


def add_record(self):
    values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
              self.amount_allowance_entry.get(), self.amount_expense_entry.get(),)
    self.record_tree.insert("", "end", values=values)
    self.input_data.append(values)
    # Clear entry box
    clear_entries(self)
    # Add to CSV file
    with open("record_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(values)


def delete_record(self):
    try:
        selected_item = self.record_tree.selection()[0]
        self.record_tree.delete(selected_item)
        # Identify the index of the row that want to delete
        # from the CSV file(delete_item output: I004)
        # "I" is excluded and only the numeric part is retrieved,
        # subtracting 1 to convert to a 0-based index
        index_to_delete = int(selected_item[1:]) - 1
        # Delete the corresponding row from the self.input_data list
        del self.input_data[index_to_delete]
        # Overwrite CSV file with new data
        with open("record_data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.input_data)
        # Clear entry box
        clear_entries(self)
    except IndexError:
        pass


def clear_entries(self):
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
    selected = self.record_tree.focus()
    values = self.record_tree.item(selected, "values")
    self.allowance_button.config(text="UPDATE", command=lambda: update_record(self))
    self.expense_button.config(text="UPDATE", command=lambda: update_record(self))
    # output to entry boxes
    self.date.entry.insert(0, values[0])
    self.allowance_source_entry.insert(0, values[1])
    self.amount_allowance_entry.insert(0, values[3])
    self.expense_combo.set(values[2])
    self.amount_expense_entry.insert(0, values[4])


def update_record(self):
    selected = self.record_tree.focus()
    new_values = (self.date.entry.get(), self.allowance_source_entry.get(), self.expense_combo.get(),
                  self.amount_allowance_entry.get(), self.amount_expense_entry.get())
    self.record_tree.item(selected, values=new_values)
    # Index that want to update
    index_to_update = int(selected[1:]) - 1
    # Update self.input_data list with new
    self.input_data[index_to_update] = list(new_values)
    with open("record_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(self.input_data)
    self.allowance_button.config(text="ADD", command=lambda: add_record(self))
    self.expense_button.config(text="ADD", command=lambda: add_record(self))
    # Clear entry box
    clear_entries(self)


def calc_cost(self):
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
    self.remain_label.config(text=f"Total Allowance:  ${total_allowance}   Total Spending:  ${total_spending}   Savings:  ${savings}")


def show_graph(self):
    # 0%のアイテムを除外するために、カウントが0より大きいアイテムのみをフィルタリング
    count_items = {"Snacks": 0, "Books": 0, "Game/Toy": 0, "Gifts": 0, "Clothing": 0}
    for item in self.input_data:
        if item[2] in count_items:
            count_items[item[2]] += 1

    # Dictionary only items grater than 0
    filtered_items = {}
    for key, value in count_items.items():
        if value > 0:
            filtered_items[key] = value

    numbers = list(filtered_items.values())
    items = list(filtered_items.keys())

    fig, ax = plt.subplots(figsize=(3, 3))
    if numbers:  # 数値リストが空でない場合のみ描画
        ax.pie(numbers, labels=items, autopct='%1.1f%%')
        ax.set_title('Pie Chart')
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
    else:
        print("No data to display")

