import sqlite3

try:
    connection = sqlite3.connect("Sqldatabase/mars")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER,user VARCHAR(50),password VARCHAR(50))")
    cursor.execute("CREATE TABLE post (id INTEGER,descrp VARCHAR(250),p_username VARCHAR(50))")
except Exception as ex:
    print(ex)
