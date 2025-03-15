def expense_tracker():
    print("\n" + "=== Expense Tracker ===".center(50))
    category = input("Enter expense category (e.g., Food, Transport, Bills): ")
    amount = input("Enter expense amount: ")
    date = input("Enter the date (YYYY-MM-DD): ")
    notes = input("Enter any additional notes: ")
    
    print("\n" + "Expense Recorded:".center(50))
    print(f"Category: {category}".center(50))
    print(f"Amount: ₱{amount}".center(50))
    print(f"Date: {date}".center(50))
    print(f"Notes: {notes}".center(50))

def main():
    while True:
        print("\n" + "================ Finance Calculator ===============".center(50))
        print("1. Enter Expense".center(50))
        print("2. View Summary".center(50))
        print("3. Analyze Budget".center(50))
        print("4. Investment Suggestions".center(50))
        print("5. Exit".center(50))
        print("=" * 50)
        
        choice = input("\nChoose an option (1-5): ")
        
        if choice == '1':
            expense_tracker()
        elif choice == '2':
            print("\nFeature under development...")
        elif choice == '3':
            print("\nFeature under development...")
        elif choice == '4':
            print("\nFeature under development...")
        elif choice == '5':
            print("\n" + "Goodbye!".center(50))
            break
        else:
            print("\n" + "Invalid choice. Please select a valid option.".center(50))

if __name__ == "__main__":
    main()
