import sqlite3

def create_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database ready!")

def add_expense():
    try:
        amount = float(input("Enter amount spent: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    print("Suggested categories: Food, Travel, Shopping, Savings, Rent, Bills, Entertainment, Other")
    category = input("Enter category: ").strip().title()
    date = input("Enter date (DD-MM-YYYY): ")
    note = input("Any note (optional): ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, date, note)
        VALUES (?, ?, ?, ?)
    """, (amount, category, date, note))
    conn.commit()
    conn.close()
    print("Expense added successfully!")

def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(f"ID: {row[0]} | Amount: {row[1]} | Category: {row[2]} | Date: {row[3]} | Note: {row[4]}")

def delete_expense():
    view_expenses()
    expense_id = input("Enter the ID of the expense to delete: ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    print("Expense deleted (if ID existed).")

def total_spending():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()

    if total is None:
        print("No expenses yet.")
    else:
        print(f"Total spending: {total}")

def spending_by_category():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No expenses yet.")
    else:
        print("\n--- Spending by Category ---")
        for row in rows:
            print(f"{row[0]}: {row[1]}")
def update_expense():
    view_expenses()
    expense_id = input("Enter the ID of the expense to update: ")

    try:
        new_amount = float(input("Enter new amount: "))
    except ValueError:
        print("Invalid amount. Update cancelled.")
        return

    new_category = input("Enter new category: ").strip().title()
    new_date = input("Enter new date (DD-MM-YYYY): ")
    new_note = input("Enter new note: ")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, date = ?, note = ?
        WHERE id = ?
    """, (new_amount, new_category, new_date, new_note, expense_id))
    conn.commit()
    conn.close()
    print("Expense updated (if ID existed).")
def menu():
    create_database()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. Total Spending")
        print("6. Spending by Category")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            total_spending()
        elif choice == "6":
            spending_by_category()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

menu()
