import sqlite3

conn = sqlite3.connect('./data/highscores.db')
cursor = conn.cursor()

print("Opened database successfully")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
''')

print("Table created successfully")

conn.close()