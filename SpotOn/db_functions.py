# Iwo Szczepaniak
import sqlite3

### creation of database
def create_database(db_name):
    conn = sqlite3.connect(db_name)

    # creation of categories table
    conn.execute('''CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    include TEXT,
                    exclude TEXT)''')
    
    # creation of recipes table
    conn.execute('''CREATE TABLE IF NOT EXISTS recipes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    image_url TEXT,
                    extra_include TEXT,
                    nutrients TEXT,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(id))''')
    
    conn.commit()
    conn.close()



### inserting data
    # category insert
def insert_into_categories(db_name, include, exclude):
    conn = sqlite3.connect(db_name)

    conn.execute("INSERT INTO categories (include, exclude) VALUES (?, ?)", 
                    (f"{include}", f"{exclude}"))
    
    cursor = conn.execute("SELECT id FROM categories WHERE include = ? AND exclude = ?", 
                      (f"{include}", f"{exclude}"))
    category_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return category_id



    # recipe insert
def insert_into_recipes(db_name, category_id, title, image_url, extra_include, nutrients):
    conn = sqlite3.connect(db_name)

    conn.execute("INSERT INTO recipes (title, image_url, extra_include, nutrients, category_id) VALUES (?, ?, ?, ?, ?)", 
                    (f"{title}", f"{image_url}", f"{extra_include}", f"{nutrients}", f"{category_id}"))
    conn.commit()
    conn.close()


### searching
def search_data_in_database(db_name, include, exclude):
    conn = sqlite3.connect(db_name)

    cursor = conn.execute("SELECT * FROM categories WHERE include = ? AND exclude = ?", 
                      (f"{include}", f"{exclude}"))
    
    flag = cursor.fetchone() 

    conn.close()
    
    if flag != None:
        return True
    else:
        return False
    
