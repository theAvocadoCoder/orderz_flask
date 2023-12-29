import sqlite3

connection = sqlite3.connect('orderz.db')

with open('schema.sql', 'r') as f:
    sql_script = f.read()

connection.executescript(sql_script)

connection.commit()
connection.close()