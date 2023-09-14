# Iwo Szczepaniak
from db_functions import create_database, search_data_in_database
from search_functions import handle_api_request, handle_db_request, excluded_correctly
from tkinter import Label, Entry, Button, Tk, BOTTOM


def find_food(include, exclude = "plums"):
    db_name = "database.db"
    create_database(db_name)

    if not excluded_correctly(include, exclude): return

    print(f"\nSearching for food with included: {include} and excluded: {exclude}\n")

    # if search already in the clatalogue, do the database query and print result
    if search_data_in_database(db_name,include, exclude):
        handle_db_request(db_name,include, exclude)

    #else ask api for the result, save it and print
    else:
        handle_api_request(db_name, include, exclude)


def start():
    def search():
        include = entry_include.get().split(", ")
        exclude = entry_exclude.get().split(", ")
        root.destroy()
        if exclude == [""]:
            find_food(sorted(include))
        else: 
            find_food(sorted(include), sorted(exclude))


    root = Tk()
    root.title("Type in your products")

    root.geometry("500x300")

    label_include = Label(root, text="\nIngredients should be separated by comma\nExcluding is not necessary - by default plums are excluded\n")
    label_include.pack()

    label_include = Label(root, text="\nEnter products you have:")
    label_include.pack()

    entry_include = Entry(root)
    entry_include.pack()

    label_exclude = Label(root, text="\nEnter products you don't want to eat\n Not necessary - by default plums:")
    label_exclude.pack()

    entry_exclude = Entry(root)
    entry_exclude.pack()

    button_search = Button(root, text="Search", command=search)
    button_search.pack(side=BOTTOM)

    root.mainloop()


if __name__ == "__main__":
    # include = ["chicken", "salad"]
    # exclude = ["ginger"]
    # find_food(include, exclude)

    ### GUI
    start()
  
