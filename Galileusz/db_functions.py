import sqlite3

### creation of database
def create_DB(db_name:str):
    conn = sqlite3.connect(db_name)

    # creation of clients table
    conn.execute('''CREATE TABLE IF NOT EXISTS clients(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    subject TEXT,
                    level INTEGER,
                    rate INTEGER,
                    day INTEGER)''')
    
        # creation of lessons table
    conn.execute('''CREATE TABLE IF NOT EXISTS lessons(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month INTEGER,
                    client_id INTEGER,
                    FOREIGN KEY (client_id) REFERENCES clients(id))''')
    
    conn.commit()
    conn.close()

### inserting data
def insert_into_clients_DB(db_name:str, name:str, subject:str, level:int, rate:int, day:int):
    conn = sqlite3.connect(db_name)

    conn.execute("INSERT INTO clients (name, subject, level, rate, day) VALUES (?, ?, ?, ?, ?)", 
                    (f"{name}", f"{subject}", f"{level}", f"{rate}", f"{day}"))
    
    cursor = conn.execute("SELECT id FROM clients WHERE name = ? AND subject = ? AND level = ? AND rate = ? AND day = ?", 
                    (f"{name}", f"{subject}", f"{level}", f"{rate}", f"{day}"))
    client_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return client_id

def insert_into_lessons(db_name, month, client_id):
    conn = sqlite3.connect(db_name)

    conn.execute("INSERT INTO lessons (month, client_id) VALUES (?, ?)", 
                    (f"{month}", f"{client_id}"))
    conn.commit()
    conn.close()


### searching
def search_sb_DB(db_name, name, day):
    conn = sqlite3.connect(db_name)

    cursor = conn.execute("SELECT * FROM clients WHERE name = ? AND day = ?", 
                      (f"{name}", f"{day}"))
    
    flag = cursor.fetchone() 

    conn.close()
    
    if flag != None:
        return flag[0]
    else:
        return None
    
def reset_DB():
    conn = sqlite3.connect("korki.db")
    conn.execute("DELETE FROM clients")
    conn.execute("DELETE FROM lessons")
    conn.commit()
    conn.close()