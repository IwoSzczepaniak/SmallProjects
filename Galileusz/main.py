import tkinter as tk
from db_functions import *
from time import sleep
import datetime

db_name="korki.db"
current_date = datetime.date.today()
current_weekday = current_date.weekday()
current_month = current_date.month


def save_name():
    global name_var
    name_var.set(entry.get())
    name = name_var.get()

    if len(name) > 0:
        clientID = search_sb_DB(db_name, name, int(current_weekday))
        if clientID is not None:
            insert_into_lessons(db_name, current_month, clientID)
            print("Added lesson to:", name)
        else:
            # TO DO
            # create a window to ask for a subject and price
            level = 0
            subject = "Fizyka"
            price = 50

            insert_into_clients_DB(db_name, name, subject, level, price, int(current_weekday))
            clientID = search_sb_DB(db_name, name, int(current_weekday))
            insert_into_lessons(db_name, current_month, clientID)
            print("Saved Name:", name)
        sleep(0.1)
        window.destroy()

window = tk.Tk()
window.title("Korepetycje")
create_DB(db_name)

window.geometry("400x100")

label = tk.Label(window, text="Imię ucznia:")
label.pack()

name_var = tk.StringVar()

entry = tk.Entry(window, textvariable=name_var)
entry.pack()

save_button = tk.Button(window, text="Wyszukaj w bazie", command=save_name)
save_button.pack()

reset_button = tk.Button(window, text="Resetuj bazę danych", command=reset_DB)
reset_button.pack()

window.mainloop()


