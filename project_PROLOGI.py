import sys
import subprocess
import json
import os
import csv
import sqlite3
import datetime
import matplotlib.pyplot as plt
import statistics
from collections import Counter

required_modules = ["matplotlib", "sqlite3", "statistics"]

def install_modules():
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing missing module: {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_modules()

DATA_FILE_JSON = "expenses.json"
DATA_FILE_CSV = "expenses.csv"
DB_FILE = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        amount REAL,
                        date TEXT,
                        notes TEXT)''')
    conn.commit()
    conn.close()

def load_expenses():
    if os.path.exists(DATA_FILE_JSON):
        with open(DATA_FILE_JSON, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(DATA_FILE_JSON, "w") as file:
        json.dump(expenses, file, indent=4)

def save_expenses_csv(expenses):
    with open(DATA_FILE_CSV, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Amount", "Date", "Notes"])
        for exp in expenses:
            writer.writerow([exp["category"], exp["amount"], exp["date"], exp["notes"]])

def save_expense_sqlite(category, amount, date, notes):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date, notes) VALUES (?, ?, ?, ?)", (category, amount, date, notes))
    conn.commit()
    conn.close()

def expense_tracker():
    print("\n".join([line.center(72) for line in r"""
  ___                              _____            _           
 | __|_ ___ __  ___ _ _  ___ ___  |_   _| _ __ _ __| |_____ _ _ 
 | _|\ \ / '_ \/ -_) ' \(_-</ -_)   | || '_/ _` / _| / / -_) '_|
 |___/_\_\ .__/\___|_||_/__/\___|   |_||_| \__,_\__|_\_\___|_|  
         |_|                                                    
""".splitlines()]))
    print("=" * 72)
    category = input("Enter expense category (e.g., Food, Transport, Bills): ")
    amount = float(input("Enter expense amount: "))
    date = input("Enter the date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
    notes = input("Enter any additional notes: ")
    
    expense = {"category": category, "amount": amount, "date": date, "notes": notes}
    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    save_expenses_csv(expenses)
    save_expense_sqlite(category, amount, date, notes)
    
    print("\nExpense Recorded:".center(72))
    print(f"Category: {category}".center(72))
    print(f"Amount: ₱{amount}".center(72))
    print(f"Date: {date}".center(72))
    print(f"Notes: {notes}".center(72))

def view_summary():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n".join([line.center(50) for line in r"""
  ___                              ___                                
 | __|_ ___ __  ___ _ _  ___ ___  / __|_  _ _ __  _ __  __ _ _ _ _  _ 
 | _|\ \ / '_ \/ -_) ' \(_-</ -_) \__ \ || | '  \| '  \/ _` | '_| || |
 |___/_\_\ .__/\___|_||_/__/\___| |___/\_,_|_|_|_|_|_|_\__,_|_|  \_, |
         |_|                                                     |__/ 
""".splitlines()]))
    print("=" * 72)
    for exp in expenses:
        print(f"{exp['date']} | {exp['category']} | ₱{exp['amount']} | {exp['notes']}")

def report_on_budget():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    
    total_expense = sum(exp["amount"] for exp in expenses)
    avg_expense = statistics.mean(exp["amount"] for exp in expenses) if expenses else 0
    category_counts = Counter(exp["category"] for exp in expenses)
    
    print("\n".join([line.center(72) for line in r"""
  ___         _          _     ___                   _   
 | _ )_  _ __| |__ _ ___| |_  | _ \___ _ __  ___ _ _| |_ 
 | _ \ || / _` / _` / -/)  _| |   / -_) '_ \/ _ \ '_|  _|
 |___/\_,_\__,_\__, \___|\__| |_|_\___| .__/\___/_|  \__|
               |___/                  |_|                 
""".splitlines()]))
    print("=" * 72)
    print(f"Total Expenses: ₱{total_expense}".center(72))
    print(f"Average Expense: ₱{avg_expense}".center(72))
    print("\nCategory Breakdown:")
    for category, count in category_counts.items():
        print(f"{category}: {count} times")

def analyze_budget():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    
    categories = {}
    for exp in expenses:
        categories[exp["category"]] = categories.get(exp["category"], 0) + exp["amount"]
    
    plt.figure(figsize=(8, 6))
    plt.bar(categories.keys(), categories.values(), color='skyblue')
    plt.xlabel("Category")
    plt.ylabel("Amount (₱)")
    plt.title("Expense Analysis by Category")
    plt.xticks(rotation=45)
    plt.show()

def help_section():
    print("\n".join([line.center(72) for line in r"""
  _  _     _        ___         _   _          
 | || |___| |_ __  / __| ___ __| |_(_)___ _ _  
 | __ / -_) | '_ \ \__ \/ -_) _|  _| / _ \ ' \ 
 |_||_\___|_| .__/ |___/\___\__|\__|_\___/_||_|
            |_|                                 
""".splitlines()]))
    print("=" * 72)
    print("1. Enter Expense - Record a new expense.")
    print("2. View Summary - View all recorded expenses.")
    print("3. Analyze Budget - View expense distribution graph.")
    print("4. Report on Budget - Get a summary report of your spending habits.")
    print("5. Help Section - Learn about the program.")
    print("6. Exit - Close the program.")

def main():
    init_db()
    while True:
        print("=" * 72)
        print(r"""
  ___ _                          ___      _         _      _           
 | __(_)_ _  __ _ _ _  __ ___   / __|__ _| |__ _  _| |__ _| |_ ___ _ _ 
 | _|| | ' \/ _` | ' \/ _/ -_) | (__/ _` | / _| || | / _` |  _/ _ \ '_|
 |_| |_|_||_\__,_|_||_\__\___|  \___\__,_|_\__|\_,_|_\__,_|\__\___/_|  
            """)
        print("=" * 72)
        print("1. Enter Expense".center(72))
        print("2. View Summary".center(72))
        print("3. Analyze Budget".center(72))
        print("4. Report on Budget".center(72))
        print("5. Help Section".center(72))
        print("6. Exit".center(72))
        print("=" * 72)
        
        choice = input("\nChoose an option (1-6): ")
        
        if choice == '1':
            expense_tracker()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            analyze_budget()
        elif choice == '4':
            report_on_budget()
        elif choice == '5':
            help_section()
        elif choice == '6':
            print("\n".join([line.center(72) for line in r"""
   ___              _ _             _ 
  / __|___  ___  __| | |__ _  _ ___| |
 | (_ / _ \/ _ \/ _` | '_ \ || / -_)_|
  \___\___/\___/\__,_|_.__/\_, \___(_)
                           |__/        
            """.splitlines()]))
            break
        else:
            print("\n" + "Invalid choice. Please select a valid option.".center(72))

if __name__ == "__main__":
    main()
