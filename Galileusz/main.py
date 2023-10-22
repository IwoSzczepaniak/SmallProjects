from classes import *
import os

if __name__ == "__main__":

    if not os.path.exists(db_name): 
        create_DB(db_name)
    
    start = WindowStart("Wybierz")
    start.vis()
