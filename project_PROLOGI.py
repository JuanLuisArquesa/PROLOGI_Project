import json
import os
import datetime
import matplotlib.pyplot as plt

data_file = "expenses.json"

def load_expenses():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(data_file, "w") as file:
        json.dump(expenses, file, indent=4)

def expense_tracker():
    print("\n" + "=== Expense Tracker ===".center(50))
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
    
    print("\nExpense Recorded:".center(50))
    print(f"Category: {category}".center(50))
    print(f"Amount: ₱{amount}".center(50))
    print(f"Date: {date}".center(50))
    print(f"Notes: {notes}".center(50))

def view_summary():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    
    print("\n=== Expense Summary ===".center(50))
    for exp in expenses:
        print(f"{exp['date']} | {exp['category']} | ₱{exp['amount']} | {exp['notes']}")

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

def main():
    while True:
        print("\n" + "================ Finance Calculator ===============".center(50))
        print("1. Enter Expense".center(50))
        print("2. View Summary".center(50))
        print("3. Analyze Budget".center(50))
        print("4. Report on Budget".center(50))
        print("5. Help Section".center(50))
        print("6. Exit".center(50))
        print("=" * 50)
        
        choice = input("\nChoose an option (1-6): ")
        
        if choice == '1':
            expense_tracker()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            analyze_budget()
        elif choice == '4':
            print("Feature Under Development!")
        elif choice == '5':
            print("Feature Under Development!")
        elif choice == '6':
            print("\n" + "Goodbye!".center(50))
            break
        else:
            print("\n" + "Invalid choice. Please select a valid option.".center(50))

if __name__ == "__main__":
    main()