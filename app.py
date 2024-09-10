from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('calorie_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track_calories():
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, "%d-%m-%Y").date()
        food_items = request.form.getlist('food')
        quantities = request.form.getlist('quantity')
        calorie_per_units = request.form.getlist('calories')
        
        calorie_entries = []
        total_calories = 0
        
        for food, quantity, calorie_per_unit in zip(food_items, quantities, calorie_per_units):
            quantity = int(quantity)
            calorie_per_unit = int(calorie_per_unit)
            calories = quantity * calorie_per_unit
            total_calories += calories
            calorie_entries.append((date_str, food, quantity, calories))
        
        conn = get_db_connection()
        c = conn.cursor()
        c.executemany("INSERT INTO calorie_intake (date, food, quantity, calories) VALUES (?, ?, ?, ?)", calorie_entries)
        conn.commit()
        conn.close()
        
        return render_template('results.html', total_calories=total_calories, date=date_str)
    
    return render_template('track.html')

@app.route('/setup')
def setup_db():
    conn = get_db_connection()
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
    return redirect(url_for('setup_complete'))

@app.route('/setup_complete')
def setup_complete():
    return render_template('setup_complete.html')

if __name__ == '__main__':
    app.run(debug=True)
