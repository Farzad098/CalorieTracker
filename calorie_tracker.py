import sqlite3
from datetime import datetime

# Function to create the SQLite table if it doesn't exist
def create_table():
    conn = sqlite3.connect('calories.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calorie_intake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                food TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                calories INTEGER NOT NULL
            )''')
    conn.commit()
    conn.close()

# Function to get the calories for a specific food item
def get_calories(food):
    while True:
        try:
            quantity = int(input(f"How many {food} did you eat?: "))
            if quantity < 0:
                print("Quantity cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            calories_per_unit = int(input(f"Enter calories per {food}: "))
            if calories_per_unit < 0:
                print("Calories cannot be negative. Please try again.")
            else:
                return quantity * calories_per_unit
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to track calories consumed for a specific date
def track_calories():
    total_calories = 0
    calorie_entries = []
    
    while True:
        try:
            date_str = input("Enter the date (DD-MM-YYYY): ")
            date = datetime.strptime(date_str, "%d-%m-%Y").date()
            if date.year < datetime.now().year:
                print("Please enter a date from this year onwards.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please enter date in DD-MM-YYYY format.")
    
    print(f"Enter food items for {date_str}. Enter 'done' when finished.")
    while True:
        food = input("Enter food item (or 'done' to finish): ")
        if food.lower() == "done":
            break
        calories = get_calories(food)
        total_calories += calories
        quantity = None  # You can modify this if you want to track quantity in the database
        calorie_entries.append((date_str, food, quantity, calories))
    
    if calorie_entries:
        save_to_database(calorie_entries)
    
    print(f"Total calories consumed on {date.strftime('%d-%m-%Y')}: {total_calories}")

# Function to save calorie entries to the SQLite database
def save_to_database(calorie_entries):
    try:
        conn = sqlite3.connect('calories.db')
        c = conn.cursor()
        c.executemany("INSERT INTO calorie_intake (date, food, quantity, calories) VALUES (?, ?, ?, ?)", calorie_entries)
        conn.commit()
        conn.close()
        print(f"Successfully saved {len(calorie_entries)} entries to the database.")
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")

# Main program flow
if __name__ == "__main__":
    create_table()
    track_calories()
