# Iwo Szczepaniak
from db_functions import insert_into_categories, insert_into_recipes
from api_functions import recipes_API_beta, return_recipe
from time import sleep
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from translate import Translator
import platform



### GUI 
    #db request
def handle_db_request(db_name, include, exclude):
    p_include = ""
    for el in include:
        p_include += el + "\n"

    root = tk.Tk()
    root.title("Recipes")

    root.configure(bg="white")

    if platform.system() == 'Windows':
        root.state("zoomed")
    elif platform.system() == 'Linux':
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    else:
        root.geometry("1400x900")


    conn = sqlite3.connect(db_name)

    cursor = conn.execute("SELECT id FROM categories WHERE include = ? AND exclude = ?", 
                      (f"{include}", f"{exclude}"))
    category_id = cursor.fetchone()[0]

    cursor = conn.execute("SELECT * FROM recipes WHERE category_id = ?", 
                      (f"{category_id}",))
    

    
    recipe_label = tk.Label(root, text="")
    recipe_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
    recipe_label.config(bg="white")

    recipe_label_PL = tk.Label(root, text="")
    recipe_label_PL.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
    recipe_label_PL.config(bg="white")


    recipe_image = tk.Label(root)
    recipe_image.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    recipe_list = []
    for row in cursor:
        recipe_list.append(row)

    current_recipe_index = 0

    translator = Translator(to_lang='pl')

    def update_recipe():
        recipe_title = recipe_list[current_recipe_index][1]
        image_url = recipe_list[current_recipe_index][2]
        extra_include = recipe_list[current_recipe_index][3]
        nutrients = recipe_list[current_recipe_index][4]

        # download the image from the URL
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        # resize the image to fit in the window
        img = img.resize((300, 300), Image.ANTIALIAS)
        # convert the image to a tkinter-compatible format
        tk_img = ImageTk.PhotoImage(img)

        eng_version = f"\n\nENG\n\nRECIPE TITLE:\n{recipe_title}\n\nINCLUDED ingredients are:\n{p_include}\nEXTRA ingredients are:\n{extra_include}\nNUTRIENTS are:\n{nutrients}"
        recipe_label.config(text= eng_version)

        # due to translator limits 
        if ("MYMEMORY WARNING") in translator.translate(recipe_title):
            PL_recipe_title = recipe_title
            PL_p_include = p_include
            PL_extra_include = extra_include
            PL_nutrients = nutrients
        else:
            PL_recipe_title = translator.translate(recipe_title)
            PL_p_include = translator.translate(p_include)
            PL_extra_include = translator.translate(extra_include)
            PL_nutrients = translator.translate(nutrients)

        


        pl_version = f"\n\nPL\n\nTYTUŁ PRZEPISU:\n{PL_recipe_title}\n\nWSKAZANE składniki to:\n{PL_p_include}\nDODATKOWE składniki to:\n{PL_extra_include}\nWARTOŚCI ODŻYWCZE to:\n{PL_nutrients}"
        recipe_label_PL.config(text= pl_version)

        recipe_image.config(image=tk_img)
        recipe_image.image = tk_img 

    def prev_recipe():
        nonlocal current_recipe_index
        if current_recipe_index > 0:
            current_recipe_index -= 1
            update_recipe()

    def next_recipe():
        nonlocal current_recipe_index
        if current_recipe_index < len(recipe_list) - 1:
            current_recipe_index += 1
            update_recipe()

    # create buttons for navigating between recipes
    prev_button = tk.Button(root, text="<< Prev", command=prev_recipe)
    prev_button.grid(row=2, column=0, sticky="sw", padx=10, pady=10)

    next_button = tk.Button(root, text="Next >>", command=next_recipe)
    next_button.grid(row=2, column=2, sticky="se", padx=10, pady=10)

    update_recipe()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(1, weight=1)

    conn.close()

    root.mainloop()



    # api request
def handle_api_request(db_name, include, exclude):
    categ_id = insert_into_categories(db_name, include, exclude)
    recipes = recipes_API_beta(include, exclude)
    i = 0

    if recipes != None:
        for recipe in recipes:
            if i == 5: break
            title, image_url, extra_include, nutrients = return_recipe(recipe, include)
            insert_into_recipes(db_name, categ_id, title, image_url, extra_include, nutrients)
            i += 1

        handle_db_request(db_name, include, exclude)


### check if excluding is reasonable
def excluded_correctly(include, exclude):
    for el in exclude:
        if el[-1] == 's':
            el = el[:-1]
        if el in include:
            print("Any excluded element can't be included in a dish")
            return False
    return True



### console printing - in english only - !not used anymore!

    # printing all records in recipes table for include and exclude
def console_handle_db_request(db_name, include, exclude):
    print("IT IS IN DATABASE - LET'S DO QUERY!")
    conn = sqlite3.connect(db_name)

    cursor = conn.execute("SELECT id FROM categories WHERE include = ? AND exclude = ?", 
                      (f"{include}", f"{exclude}"))
    category_id = cursor.fetchone()[0]

    cursor = conn.execute("SELECT * FROM recipes WHERE category_id = ?", 
                      (f"{category_id}",))
    
    for row in cursor:
        sleep(2)
        print_recipe(include, exclude, row[1], row[2], row[3], row[4])

    conn.close()

    # printing all recipes for api request
def console_handle_api_request(db_name, include, exclude):
    categ_id = insert_into_categories(db_name, include, exclude)
    recipes = recipes_API_beta(include, exclude)
    i = 0
    for recipe in recipes:
        if i == 5: break
        title, image_url, extra_include, nutrients = return_recipe(recipe, include)
        insert_into_recipes(db_name, categ_id, title, image_url, extra_include, nutrients)
        if i > 0: sleep(3)
        print_recipe(include, exclude, title, image_url, extra_include, nutrients)
        i += 1


    # print recipe from variables
def print_recipe(include, exclude, title, image_url, extra_include, nutrients):

    print(f"\n\n\t\tRECIPE TITLE:", title)
    print(image_url)

    print("\n\tINCLUDED ingredients are:")
    for inc in include: print(inc)
    print("\tEXTRA ingredients are:")
    print(extra_include)
    print("\tNUTRIENTS are:")
    print(nutrients)