import sqlite3

def create_table():
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calorie_intake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                food TEXT NOT NULL,
                quantity INTEGER,
                calories INTEGER NOT NULL
            )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
