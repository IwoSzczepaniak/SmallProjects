import tkinter as tk
from db_functions import *
from time import sleep
import datetime


db_name="korki.db"
current_date = datetime.date.today()
current_weekday = current_date.weekday()
current_month = current_date.month
window_size = "500x600"

def nr_to_day(day_number):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    if 0 <= day_number < len(days):
        return days[day_number]
    return "Invalid day number"




class Window:
    def __init__(self, title) -> None:
        self.window = tk.Tk()
        self.window_size = window_size
        self.window.title(title)
        self.window.geometry(self.window_size)


# extends Window
class WindowStart(Window):
    def __init__(self, title) -> None:
        Window.__init__(self, title)
        # self.window = title

    def win_ic_close(self):
        self.window.destroy()
        windowInputClients = WindowInputClients("Wprowadź nowego klienta")
        windowInputClients.vis()


    def win_input_lessons_start(self):
        self.window.destroy()
        windowInputLessons = WindowInputLessons("Wprowadź nową lekcję")
        windowInputLessons.vis()

    def vis(self):
        clients_label = tk.Label(self.window, text="Dodaj nowego klienta i zobacz ich podgląd:")
        clients_label.pack()

        add_clients_button = tk.Button(self.window, text="Nowy klient", command=self.win_ic_close)
        add_clients_button.pack()

        lessons_label = tk.Label(self.window, text="\nDodaj nową lekcję:")
        lessons_label.pack()

        add_lessons_button = tk.Button(self.window, text="Nowa lekcja", command=self.win_input_lessons_start)
        add_lessons_button.pack()


        self.window.mainloop()


class WindowInputLessons(Window):
    def __init__(self, title) -> None:
        super().__init__(title)

    def vis(self):
        # get all clients from the database
        clients = get_all_clients(db_name)
        client_names = [client[1] for client in clients]


        select_label = tk.Label(self.window, text="Wybierz klienta: ")
        select_label.pack()

        selected_client = tk.StringVar(self.window)
        selected_client.set("Tu wybierz imię") # set the default value to the first client in the list

        # create the option menu widget
        client_menu = tk.OptionMenu(self.window, selected_client, *client_names)
        client_menu.pack()

        self.window.mainloop()


class WindowInputClients(Window):
    def __init__(self, title) -> None:
        super().__init__(title)

    def vis(self):

        def update_client_preview():
            client_preview.delete(1.0, tk.END)  # Clear the text widget
            clients = get_all_clients(db_name)  # Fetch all clients from the database

            if clients:
                for client in clients:
                    client_preview.insert(tk.END, f"{client[1]} - {client[2]} - {nr_to_day(client[5])}\n")
            else:
                client_preview.insert(tk.END, "Brak klientów w bazie.")

        def save_name():
            name = name_block.get()

            if len(name) > 0:
                # TO DO
                # create a window to ask for adding lessons
                level = 0
                subject = "Fizyka"
                price = 50
                amount = 1 # default 1
                
                price *+ amount

                insert_into_clients(db_name, name, subject, level, price, int(current_weekday))
                clientID = search_sb(db_name, name, int(current_weekday))
                insert_into_lessons(db_name, current_month, clientID)

            sleep(0.01)
            update_client_preview()

        def reset_all():
            reset_DB()
            update_client_preview()

        # data
        name_label = tk.Label(self.window, text="Imię ucznia:")
        name_label.pack()

        name_block = tk.Entry(self.window)
        name_block.pack()
        # 

        # save btn
        save_button = tk.Button(self.window, text="Dodaj do bazy", command=save_name)
        save_button.pack()
        # 

        # preview
        client_preview = tk.Text(self.window, height=10, width=50)
        client_preview.pack()

        update_client_preview()
        # 

        # reset db
        reset_button = tk.Button(self.window, text="Resetuj bazę danych", command=reset_all)
        reset_button.pack()
        # 

        self.window.mainloop()