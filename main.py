from Interface import App
from tkinter import messagebox
from bson.objectid import ObjectId
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["electric_meter"]
col = db["Counter"]

def start_app():
    App((1000, 500), col, save_price_data_func, insert_counter_data, delete_counter_data, get_latest_price)

# Збереження інформації з налаштувань у базу даних
def save_price_data_func(day_price, night_price, addition_day, addition_night):
    price_col = db["Prices"]
    document = {"day_price": day_price, 
                "night_price": night_price,
                "addition_day": addition_day,
                "addition_night": addition_night}
    
    price_col.insert_one(document)
    
    # Перевірка
    result = price_col.find_one(document)
    
    if result is not None:
        messagebox.showinfo("Збережено", "Налаштування успішно збережено!")
    else:
        messagebox.showerror("ПОМИЛКА", "Виникла помилка під час збереження")

# Отримання останніх внесених даних про ціну
def get_latest_price():
    price_col = db["Prices"]
    latest_price_doc = price_col.find_one(sort=[('_id', pymongo.DESCENDING)])
    return latest_price_doc

# Збереження інформації з форми у базу даних
def insert_counter_data(number, date, day, night):
    counter_col = db["Counter"]
    # Отримання останнього доданого документу лічильника для заданого номера
    latest_counter = get_latest_counter_data(number)
    
    # Якщо є останній документ з вказаним номером лічильника і поточні значення дня і ночі більші за останні, обчислюється різниця між поточними та останніми значеннями дня та ночі
    # В іншому випадку використовуються значення накрутки на день і накрутки на ніч з останнього доданого документа в колекції цін
    if latest_counter is not None and day > latest_counter['day'] and night > latest_counter['night']:
        day_diff = day - latest_counter['day']
        night_diff = night - latest_counter['night']
    elif latest_counter is not None and day > latest_counter['day'] and night == latest_counter['night']:
        day_diff = day - latest_counter['day']
        night_diff = night - latest_counter['night']
    elif latest_counter is not None and day == latest_counter['day'] and night > latest_counter['night']:
        day_diff = day - latest_counter['day']
        night_diff = night - latest_counter['night']
    elif latest_counter is not None and day == latest_counter['day'] and night == latest_counter['night']:
        day_diff = day - latest_counter['day']
        night_diff = night - latest_counter['night']
    else:
        latest_price = get_latest_price()
        day_diff = latest_price['addition_day']
        night_diff = latest_price['addition_night']
    
    # Підрахунок загальної к-сті кВт
    total = day_diff + night_diff
    
    # Підрахунок ціни
    latest_price = get_latest_price()
    day_price = latest_price['day_price']
    night_price = latest_price['night_price']
    price = day_diff * float(day_price) + night_diff * float(night_price)
    
    # Вставка документу в базу даних
    document = {"number": number,
                "day": day,
                "night": night,
                "total": total,
                "date": date,
                "price": price}
    
    counter_col.insert_one(document)
    
    # Перевірка
    result = counter_col.find_one(document)
    
    if result is not None:
        messagebox.showinfo("Збережено", "Дані успішно збережено!")
    else:
        messagebox.showerror("ПОМИЛКА", "Виникла помилка під час збереження")

# Отримання останніх внесених даних лічильника
def get_latest_counter_data(number):
    counter_col = db["Counter"]
    latest_counter_doc = counter_col.find_one(
        {"number": number},
        sort=[("_id", pymongo.DESCENDING)])
    return latest_counter_doc

# Видалення документу з колекції  
def delete_counter_data(item_id):
    counter_col = db["Counter"]
    counter_col.delete_one({"_id": ObjectId(item_id)})

# Запуск програми
if __name__ == '__main__':
    start_app()