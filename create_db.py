import sqlite3

# This script's only job is to create and set up the database table.
# Render will run this once during the build process.

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