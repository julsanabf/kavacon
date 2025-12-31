import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    name TEXT
)''')
c.execute('''CREATE TABLE IF NOT EXISTS follows (
    id INTEGER PRIMARY KEY,
    follower_id INTEGER,
    followed_id INTEGER
)''')
conn.commit()
conn.close()
print("[+] Base de datos inicializada.")

