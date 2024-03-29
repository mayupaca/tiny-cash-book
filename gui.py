from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap import *
from functions import get_date, add_record, delete_record, clear_entries, select_record, update_record, calc_cost, show_graph
from data import sample_data


class TinyCashBook(tb.Frame):
    def __init__(self, master):
        # Calling the constructor of the parent class(tb.Frame)
        super().__init__(master, padding=(20, 20))
        self.pack(fill=BOTH, expand=YES)

        self.sample_data = sample_data()
        self.widgets()

    # Create widgets
    def widgets(self):
        self.app_title = tb.Label(self, text="👛Tiny Cash Book👛", font=("Helvetica", 18), foreground="#d0d0d0")
        self.app_title.pack(padx=50, pady=(0, 5), anchor="w")
        self.separator = tb.Separator(self, style="light")
        self.separator.pack(fill="x", padx=20, pady=(0, 20))

        self.main_frame = tb.Frame(self)
        self.main_frame.pack(padx=10)

        self.date_entry = self.date_entry(self.main_frame)
        self.allowance_frame = self.allowance_frame(self.main_frame)
        self.expense_frame = self.expense_frame(self.main_frame)
        self.tree_frame = self.tree_frame(self.main_frame)
        self.remain_frame = self.remain_frame(self.main_frame)
        self.btn_frame = self.btn_frame(self.main_frame)
        self.graph_frame = self.graph_frame(self.main_frame)

    # Create date entry frame
    def date_entry(self, parent): # Taking a parent argument, I can pecify which parent widget the method belongs to for the widget it generates (in this case, an entry widget for entering a date).
        date_entry = tb.LabelFrame(parent, text="📆Date📆", style='warning')
        date_entry.pack(fill="x", padx=20, pady=(0, 20))

        self.date = tb.DateEntry(date_entry, bootstyle="warning", firstweekday=6, dateformat="%Y/%m/%d")
        self.date.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))
        # lambdaがないと関数が勝手に呼ばれて実行される
        date_button = tb.Button(date_entry, text='Get Date', style="warning", width=10, command=lambda: get_date(self))
        date_button.grid(row=0, column=2, padx=10, pady=(10, 20))

        self.date_label = tb.Label(date_entry, text="You Picked:  ")
        self.date_label.grid(row=0, column=3, padx=10, pady=(10, 20))

        return date_entry

    # Create allowance frame
    def allowance_frame(self, parent):
        allowance_frame = tb.LabelFrame(parent, text="💰Allowance💰", style='info')
        allowance_frame.pack(fill="x", padx=20, pady=(0, 20))

        allowance_source_label = tb.Label(allowance_frame, text="💡How did you get?          ")
        allowance_source_label.grid(row=1, column=0, padx=10, pady=(10, 20), sticky="w")

        self.allowance_source_entry = tb.Entry(allowance_frame, style='info')
        self.allowance_source_entry.grid(row=1, column=1, padx=10, pady=(10, 20))

        amount_allowance_label = tb.Label(allowance_frame, text="💴Amount (How much?)")
        amount_allowance_label.grid(row=1, column=2, padx=10, pady=(10, 20), sticky="w")

        self.amount_allowance_entry = tb.Entry(allowance_frame, style='info')
        self.amount_allowance_entry.grid(row=1, column=3, padx=10, pady=(10, 20))

        self.allowance_button = tb.Button(allowance_frame, text="ADD", width=10, style="info", command=lambda: add_record(self))
        self.allowance_button.grid(row=1, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        return allowance_frame

    # Create expense frame
    def expense_frame(self, parent):
        expense_frame = tb.LabelFrame(parent, text="💸Spending💸", style='danger')
        expense_frame.pack(fill="x", padx=20, pady=(0, 20))

        expense_item_label = tb.Label(expense_frame, text="🍟What did you use it for?")
        expense_item_label.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="w")

        items = ["", "Snacks", "Books", "Game/Toy", "Gifts", "Clothing"]
        self.expense_combo = tb.Combobox(expense_frame, style="danger", values=items)
        self.expense_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.expense_combo.current(0)

        amount_expense_label = Label(expense_frame, text="💴Amount (How much?)")
        amount_expense_label.grid(row=2, column=2, padx=10, pady=(10, 20), sticky="w")

        self.amount_expense_entry = tb.Entry(expense_frame, style='danger')
        self.amount_expense_entry.grid(row=2, column=3, padx=10, pady=(10, 20))

        self.expense_button = tb.Button(expense_frame, text="ADD", width=10, style="danger", command=lambda: add_record(self))
        self.expense_button.grid(row=2, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        return expense_frame

    # Create treeview frame
    def tree_frame(self, parent):
        tree_frame = tb.LabelFrame(parent, text="💿History💿", style='success')
        tree_frame.pack(fill="x", padx=20, pady=(0, 0))
        columns = ("date", "source", "item", "allowance", "spending")
        # Inserts each record (row of data) into the tree view.
        self.record_tree = tb.Treeview(tree_frame, style="success", selectmode="extended", columns=columns, show="headings")
        self.record_tree.pack(fill="x", padx=10, pady=10)

        self.record_tree.column('date', width=80, anchor="w")
        self.record_tree.column('source', width=180, anchor="w")
        self.record_tree.column('item', width=180, anchor="w")
        self.record_tree.column('allowance', width=80, anchor="e")
        self.record_tree.column('spending', width=80, anchor="e")

        self.record_tree.heading('date', text="Date", anchor="w")
        self.record_tree.heading('source', text="How did you get?", anchor="w")
        self.record_tree.heading('item', text="What did you use it for?", anchor="w")
        self.record_tree.heading('allowance', text="Allowance", anchor="e")
        self.record_tree.heading('spending', text="Spending", anchor="e")
        # Inserts each record (row of data) into the tree view.
        for record in self.sample_data:
            self.record_tree.insert('', END, values=record) # insert at the end of the list
        # To trigger a specific action when the user clicks the mouse on an item in the treeview.
        self.record_tree.bind("<ButtonRelease-1>", lambda event: select_record(self, event))
        # This event binding allows the system to detect which row in the treeview the user has selected and to perform some action based on the selected row.
        return tree_frame

    # Create remain frame
    def remain_frame(self, parent):
        remain_frame = tb.LabelFrame(parent, text="🐖Balance🐖", style='success')
        remain_frame.pack(anchor="w", padx=20, pady=(0, 10))

        self.remain_label = tb.Label(remain_frame, text="Total Allowance:  $0   Total Spending:  $0   Savings:  $0")
        self.remain_label.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="e")

        reload_btn = tb.Button(remain_frame, text="RELOAD", width=10, style="success", command=lambda: calc_cost(self))
        reload_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

        return remain_frame

    # Create button frame
    def btn_frame(self, parent):
        btn_frame = tb.LabelFrame(parent, text="🖋Commands🗑", style='dark')
        btn_frame.pack(anchor="w", padx=20, pady=(0, 20))

        delete_btn = tb.Button(btn_frame, text="DELETE", width=15, style="danger", command=lambda: delete_record(self))
        delete_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

        clear_btn = tb.Button(btn_frame, text="CLEAR", width=15, style="secondary", command=lambda: clear_entries(self))
        clear_btn.grid(row=0, column=2, padx=(0, 20), pady=(10, 20))

        graph_btn = tb.Button(btn_frame, text="SHOW GRAPHS", width=15, style="primary", command=lambda: show_graph(self))
        graph_btn.grid(row=0, column=0, padx=20, pady=(10, 20))

        return btn_frame

    # Create graph frame
    def graph_frame(self, parent):
        graph_frame = tb.LabelFrame(parent, text="📈Graphs📊", style='info')
        graph_frame.pack(padx=20, pady=(0, 20), anchor="w")

        pie_label = tb.Label(graph_frame, text="")
        pie_label.grid(row=0, column=0)

        return graph_frame

