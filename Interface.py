import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import ttk, Scrollbar, messagebox
from datetime import datetime
from tkcalendar import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, size, col, save_price_data_func, insert_counter_data, delete_counter_data, get_latest_price):
        # Головні налаштування
        super().__init__()
        self.title("Двофазний лічильник")
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)    
        
        # Фрейми з віджетами
        self.current_settings = Current_settings(self, get_latest_price)
        self.settings = Settings(self, save_price_data_func, self.current_settings)
        self.table = Table(self, col, delete_counter_data)
        self.form = Form(self, insert_counter_data, self.table)
        
        # Запуск
        self.mainloop()

class Settings(ctk.CTkFrame):
    def __init__(self, master, save_price_data_func, current_settings):
        super().__init__(master)
        ctk.CTkLabel(self, text='Налаштування', font=("Script", 14)).pack(padx = 50, pady = 20) # налаштовує розміщення віджету в самому фреймі
        self.place(relx= 0.21, rely = 0.75, anchor = "e") # розміщує сам фрейм
        
        self.save_price_data_func = save_price_data_func
        self.current_settings = current_settings
        
        self.create_widgets()
        
    def create_widgets(self):
        self.dayEntry = ctk.CTkEntry(self, placeholder_text='Тариф на день', border_color="#3B8ED0")
        self.nihgtEntry = ctk.CTkEntry(self, placeholder_text='Тариф на ніч', border_color="#1F6AA5")
        self.add_DayEntry = ctk.CTkEntry(self, placeholder_text='Накрутка на день', border_color='#3B8ED0')
        self.add_NightEntry = ctk.CTkEntry(self, placeholder_text='Накрутка на ніч', border_color='#1F6AA5')
        self.saveBtn = ctk.CTkButton(self, text='Зберегти налаштування', command = self.save_price_data_to_db)
        
        self.create_layout()
        
    def create_layout(self):
        self.dayEntry.pack(pady=(0, 10))
        self.nihgtEntry.pack(pady=(0, 10))
        self.add_DayEntry.pack(pady=(0, 10))
        self.add_NightEntry.pack(pady=(0, 10))
        self.saveBtn.pack(pady=(0, 10))

    def save_price_data_to_db(self):
        day_price = self.dayEntry.get()
        night_price = self.nihgtEntry.get()
        addition_day = self.add_DayEntry.get()
        addition_night = self.add_NightEntry.get()
        
        # Перевірка вводу ціни
        try:
            day_price = float(day_price)
            night_price = float(night_price)
        except ValueError:
            messagebox.showerror("ПОМИЛКА", "Будь ласка, введіть число для ціни")
            return
        
        # Перевірка вводу накрутки
        try:
                addition_day = int(addition_day)
                addition_night = int(addition_night)
        except ValueError:
            messagebox.showerror("ПОМИЛКА", "Будь ласка, введіть ціле число для накрутки")
            return
        
        self.save_price_data_func(day_price, night_price, addition_day, addition_night)
        self.current_settings.update_labels()

class Current_settings(ctk.CTkFrame):
    def __init__(self, master, get_latest_price):
        super().__init__(master)
        ctk.CTkLabel(self, text='Налаштування, що використовуються', font=("Script", 14)).pack(padx = 50, pady = 20) # налаштовує розміщення віджету в самому фреймі
        self.place(relx= 0.59, rely = 0.75, anchor = "e") # розміщує сам фрейм
        
        self.get_latest_price = get_latest_price
        
        self.create_widgets()
        
    def create_widgets(self):
        latest_price = self.get_latest_price()
        
        self.day_price_label = ctk.CTkLabel(self, text=f"Тариф на день: {latest_price['day_price']}", font=("Courier", 14))
        self.night_price_label = ctk.CTkLabel(self, text=f"Тариф на ніч: {latest_price['night_price']}", font=("Courier", 14))
        self.addition_day_label = ctk.CTkLabel(self, text=f"Накрутка на день: {latest_price['addition_day']}", font=("Courier", 14))
        self.addition_night_label = ctk.CTkLabel(self, text=f"Накрутка на ніч: {latest_price['addition_night']}", font=("Courier", 14))
    
        self.create_layout()
        
    def create_layout(self):
        self.day_price_label.pack(pady=(0, 10))
        self.night_price_label.pack(pady=(0, 10))
        self.addition_day_label.pack(pady=(0, 10))
        self.addition_night_label.pack(pady=(0, 10))
        
    def update_labels(self):
        self.latest_price = self.get_latest_price()
        
        self.day_price_label.configure(text=f"Тариф на день: {self.latest_price['day_price']}")
        self.night_price_label.configure(text=f"Тариф на ніч: {self.latest_price['night_price']}")
        self.addition_day_label.configure(text=f"Накрутка на день: {self.latest_price['addition_day']}")
        self.addition_night_label.configure(text=f"Накрутка на ніч: {self.latest_price['addition_night']}")
        
class Table(ctk.CTkFrame):
    def __init__(self, master, col, delete_counter_data):
        super().__init__(master)
        
        self.col = col
        self.delete_counter_data = delete_counter_data
        
        self.place(relx= 0.01, rely = 0.25, anchor = "w") # Розміщення самого фрейму
        # Створення скролбару
        self.yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.on_vertical_scroll)
        # Створення таблиці
        self.table = ttk.Treeview(self, columns=('ID', 'Counter', 'Date', 'Day', 'Night', 'Total', 'Price'), show='headings')
        # Заголовки
        self.table.heading('Counter', text='Лічильник')
        self.table.heading('Date', text='Дата')
        self.table.heading('Day', text='День')
        self.table.heading('Night', text='Ніч')
        self.table.heading('Total', text='Загальний')
        self.table.heading('Price', text='Ціна')
        # Прихований стовпчик з ID
        self.table.column('ID', width=0, stretch=NO)
        
        self.yscrollbar.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        
        self.style_table()

        self.populate_table()
        
        # Дія на правий клік
        self.table.bind("<Button-3>", self.show_popup_menu)
        # Дія на лівий клік
        self.table.bind('<Button-1>', self.handle_click)

    # Відключення зміни ширини стовпців мишкою
    def handle_click(self, event):
        if self.table.identify_region(event.x, event.y) == "separator":
            return "break"
    
    # Створення випадаючого меню
    def show_popup_menu(self, event):
        popup_menu = tk.Menu(self, tearoff=False)
        popup_menu.add_command(label="Видалити", command=self.delete_item)
        
        # Відображення меню у місті кліку
        popup_menu.post(event.x_root, event.y_root)
        

    # Заповнення таблиці
    def populate_table(self):
        for item in self.col.find():
            self.table.insert('', 'end', values=(str(item['_id']),
                                                 item['number'], 
                                                 item['date'], 
                                                 item['day'], 
                                                 item['night'], 
                                                 item['total'],
                                                 item['price']))
    
    # Оновлення таблиці
    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        
        self.populate_table()
    
    # Видалення елементу із таблиці та бази даних
    def delete_item(self):
        selected_items = self.table.selection()
        
        if not selected_items:
            messagebox.showinfo("Info", "Не вибрано елементу")
            return
        
        selected_item = selected_items[0]
        
        item_data = self.table.item(selected_item)
        item_id = item_data['values'][0]
        
        self.table.delete(selected_item)
        self.delete_counter_data(item_id)
        
    
    # Метод роботи скролбара
    def on_vertical_scroll(self, *args):
        self.table.yview(*args)
    
    # Cтилізація
    def style_table(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        font =('Courier', 12))
        style.map("Treeview.Heading",
                background=[('active', '#3484F0')])
        
        style.configure("Vertical.TScrollbar",
                        background = "#565b5e",
                        bordercolor="#343638",
                        troughcolor="gray",
                        )
        
        style.map("Vertical.TScrollbar",
                  background=[("active", "#3B8ED0")])
    
class Form(ctk.CTkFrame):
    def __init__(self, master, insert_counter_data, table):
        super().__init__(master)
        
        self.table = table
        
        self.insert_counter_data = insert_counter_data
        
        self.place(relx= 0.6, rely = 0.75, anchor = "w")
        ctk.CTkLabel(self, text='Форма для заповнення', font=("Script", 14)).pack(padx = 50, pady = 15)
        
        
        self.create_widgets()
    
    def create_widgets(self):
        self.myCal = Calendar(self, 
                              setmode = 'day', 
                              date_pattern = 'y-mm-dd', 
                              background = '#1F6AA5', 
                              foreground='white', 
                              headersforeground='white',
                              tooltipforeground='white')
        
        self.date = ctk.StringVar(value="")
        
        self.myCal.bind("<<CalendarSelected>>", self.on_date_selected)
        
        self.dateEntry = ctk.CTkEntry(self, placeholder_text='Дата', border_color="#3B8ED0")
        self.counterNum = ctk.CTkEntry(self, placeholder_text='Номер лічильника', border_color="#3B8ED0")
        self.day_kWtEntry = ctk.CTkEntry(self, placeholder_text='кВт за день', border_color="#3B8ED0")
        self.night_kWtEntry = ctk.CTkEntry(self, placeholder_text='кВт за ніч', border_color="#3B8ED0")
        self.enterBtn = ctk.CTkButton(self, text = "Зберегти дані", command=self.save_counter_data)
        
        
        self.create_layout()
    
    # Заповнення поля вводу дати через вибір дати у календарі
    def on_date_selected(self, event):
        # Оновлення StringVar вибраною датою
        self.date.set(self.myCal.get_date())
        
        self.dateEntry.delete(0, 'end')
        self.dateEntry.insert(0, self.date.get())
        
    def create_layout(self):
        self.myCal.pack(padx = 20, side='right')
        self.dateEntry.pack(padx=(10, 0), pady=(6, 10))
        self.counterNum.pack(padx=(10, 0), pady=(0, 10))
        self.day_kWtEntry.pack(padx=(10, 0), pady=(0, 10))
        self.night_kWtEntry.pack(padx=(10, 0), pady=(0, 10))
        self.enterBtn.pack(padx=(10, 0), pady=(0, 5))

    # Перевірка даних і збереження інформації у базу даних
    def save_counter_data(self):
        date = self.dateEntry.get()
        number = self.counterNum.get()
        day = self.day_kWtEntry.get()
        night = self.night_kWtEntry.get()
        
        try:
            day = float(day)
            night = float(night)
        except ValueError:
            messagebox.showerror("ПОМИЛКА", "Будь ласка, введіть число для к-сті кВТ")
            return
        
        try:
            number = int(number)
        except ValueError:
            messagebox.showerror("ПОМИЛКА", "Будь ласка, введіть ціле число для № лічильника")
            return
        
        try:
             datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("ПОМИЛКА", "Будь ласка, введіть дату у форматі РРРР-MM-ДД")
            return
        
        self.insert_counter_data(number, date, day, night)
        self.table.refresh_table()