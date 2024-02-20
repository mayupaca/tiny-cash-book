# gui.py
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from methods import get_date, add_record, delete_record, clear_entries, select_record, update_record, calc_cost, show_graph
from ttkbootstrap import *


class TinyCashBook(tb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 20))
        self.pack(fill=BOTH, expand=YES)

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

        self.create_widgets()

    def create_widgets(self):
        self.app_title = tb.Label(self, text="👛Tiny Cash Book👛", font=("Helvetica", 18), foreground="#d0d0d0")
        self.app_title.pack(padx=50, pady=(0, 5), anchor="w")
        self.separator = tb.Separator(self, style="light")
        self.separator.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        self.main_frame = tb.Frame(self)
        self.main_frame.pack(padx=10)

        self.date_entry = self.create_date_entry(self.main_frame)
        self.allowance_frame = self.create_allowance_frame(self.main_frame)
        self.expense_frame = self.create_expense_frame(self.main_frame)
        self.tree_frame = self.create_tree_frame(self.main_frame)
        self.remain_frame = self.create_remain_frame(self.main_frame)
        self.btn_frame = self.create_btn_frame(self.main_frame)
        self.graph_frame = self.create_graph_frame(self.main_frame)

    def create_date_entry(self, parent):
        date_entry = tb.LabelFrame(parent, text="📆Date📆", style='warning.TLabelframe')
        date_entry.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        self.date = tb.DateEntry(date_entry, bootstyle="warning", firstweekday=6, dateformat="%Y/%m/%d")
        self.date.grid(row=0, column=0, padx=(20, 0), pady=(10, 20))

        date_button = tb.Button(date_entry, text='Get Date', style="warning", width=10, command=lambda: get_date(self))
        date_button.grid(row=0, column=2, padx=10, pady=(10, 20))

        self.date_label = tb.Label(date_entry, text="You Picked:  ")
        self.date_label.grid(row=0, column=3, padx=10, pady=(10, 20))

        return date_entry

    def create_allowance_frame(self, parent):
        allowance_frame = tb.LabelFrame(parent, text="💰Allowance💰", style='info.TLabelframe')
        allowance_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        allowance_source_label = tb.Label(allowance_frame, text="💡How did you get?          ")
        allowance_source_label.grid(row=1, column=0, padx=10, pady=(10, 20), sticky="w")

        self.allowance_source_entry = tb.Entry(allowance_frame, style='info')
        self.allowance_source_entry.grid(row=1, column=1, padx=10, pady=(10, 20))

        amount_allowance_label = tb.Label(allowance_frame, text="💴Amount (How much?)")
        amount_allowance_label.grid(row=1, column=2, padx=10, pady=(10, 20), sticky="w")

        self.amount_allowance_entry = tb.Entry(allowance_frame, style='info')
        self.amount_allowance_entry.grid(row=1, column=3, padx=10, pady=(10, 20))

        allowance_button = tb.Button(allowance_frame, text="ADD", width=10, style="info", command=lambda: add_record(self))
        allowance_button.grid(row=1, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        return allowance_frame

    def create_expense_frame(self, parent):
        expense_frame = tb.LabelFrame(parent, text="💸Spending💸", style='danger.TLabelframe')
        expense_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

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

        expense_button = tb.Button(expense_frame, text="ADD", width=10, style="danger", command=lambda: add_record(self))
        expense_button.grid(row=2, column=4, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        return expense_frame

    def create_tree_frame(self, parent):
        tree_frame = tb.LabelFrame(parent, text="💿History💿", style='success.TLabelframe')
        tree_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 0))
        columns = ("date", "source", "item", "allowance", "spending")

        self.record_tree = tb.Treeview(tree_frame, style="success", selectmode="extended", columns=columns, show="headings")
        self.record_tree.pack(fill="x", expand="yes", padx=10, pady=10)

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

        for record in self.input_data:
            self.record_tree.insert('', END, values=record)

        self.record_tree.bind("<ButtonRelease-1>", lambda event: select_record(self, event))

        return tree_frame

    def create_remain_frame(self, parent):
        remain_frame = tb.LabelFrame(parent, text="🐖Balance🐖", style='success.TLabelframe')
        remain_frame.pack(anchor="w", expand="yes", padx=20, pady=(0, 10))

        self.remain_label = tb.Label(remain_frame, text="Total Allowance:  $0   Total Spending:  $0   Savings:  $0")
        self.remain_label.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="e")

        reload_btn = tb.Button(remain_frame, text="RELOAD", width=10, style="success", command=lambda: calc_cost(self))
        reload_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

        return remain_frame

    def create_btn_frame(self, parent):
        btn_frame = tb.LabelFrame(parent, text="🖋Commands🗑", style='light.TLabelframe')
        btn_frame.pack(anchor="w", padx=20, pady=(0, 20))

        graph_btn = tb.Button(btn_frame, text="SHOW GRAPHS", width=15, style="primary", command=lambda: show_graph(self))
        graph_btn.grid(row=0, column=0, padx=20, pady=(10, 20))

        delete_btn = tb.Button(btn_frame, text="DELETE", width=15, style="danger", command=lambda: delete_record(self))
        delete_btn.grid(row=0, column=1, padx=(0, 20), pady=(10, 20))

        clear_btn = tb.Button(btn_frame, text="CLEAR", width=15, style="secondary", command=lambda: clear_entries(self))
        clear_btn.grid(row=0, column=2, padx=(0, 20), pady=(10, 20))

        return btn_frame

    def create_graph_frame(self, parent):
        graph_frame = tb.LabelFrame(parent, text="📈Graphs📊", style='info.TLabelframe')
        graph_frame.pack(fill="x", expand="yes", padx=20, pady=(0, 20))

        pie_label = tb.Label(graph_frame, text="Spending pie chart")
        pie_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="w")

        return graph_frame
