import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

DATA_FILE = "data.json"


class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("700x500")

        # Переменные для фильтров
        self.filter_type_var = tk.StringVar()
        self.filter_date_var = tk.StringVar()

        self.create_widgets()
        self.load_data()
        self.update_table()

    def create_widgets(self):
        # --- Поля ввода ---
        frame_input = tk.LabelFrame(self.root, text="Добавить тренировку", padx=10, pady=10)
        frame_input.pack(pady=10, fill="x")

        tk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = tk.Entry(frame_input)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Тип:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.type_combobox = ttk.Combobox(frame_input, values=["Кардио", "Сила", "Гибкость"])
        self.type_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.duration_entry = tk.Entry(frame_input)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame_input, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0,
                                                                                           columnspan=2, pady=10)

        # --- Фильтры ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтр", padx=10, pady=10)
        frame_filter.pack(pady=10, fill="x")

        ttk.Combobox(frame_filter, textvariable=self.filter_type_var, values=["Все", "Кардио", "Сила", "Гибкость"],
                     state="readonly").grid(row=0, column=0, padx=5)
        tk.Entry(frame_filter, textvariable=self.filter_date_var).grid(row=0, column=1, padx=5)
        tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=2, padx=5)

        # --- Таблица ---
        columns = ("Дата", "Тип", "Длительность")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both", padx=10)

        # --- Кнопки действий ---
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Сохранить в JSON", command=self.save_data).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Загрузить из JSON", command=self.load_and_update).pack(side="left", padx=5)

    def is_valid_date(self, date):
        return bool(re.match(r"\d{2}.\d{2}.\d{4}", date))

    def is_valid_duration(self, duration):
        return duration.isdigit() and int(duration) > 0

    def add_training(self):
        date = self.date_entry.get()
        type_ = self.type_combobox.get()
        duration = self.duration_entry.get()

        if not date or not type_ or not duration:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        if not self.is_valid_date(date):
            messagebox.showerror("Ошибка", "Дата должна быть в формате ДД.ММ.ГГГГ")
            return

        if not self.is_valid_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        self.data.append({"date": date, "type": type_, "duration": int(duration)})

        self.date_entry.delete(0, 'end')
        self.duration_entry.delete(0, 'end')

        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in self.data:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def apply_filter(self):
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_var.get()

        filtered_data = []

        for item in self.data:
            type_match = (filter_type == "Все") or (item["type"] == filter_type)
            date_match = (filter_date == "") or (item["date"] == filter_date)

            if type_match and date_match:
                filtered_data.append(item)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in filtered_data:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []

    def load_and_update(self):
        self.load_data()
        self.update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()