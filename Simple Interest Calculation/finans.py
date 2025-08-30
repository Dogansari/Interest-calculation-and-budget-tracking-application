import os
import sqlite3
from datetime import datetime

# Get the directory of this .py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the database file (finance.db will be saved in the same folder)
DB_PATH = os.path.join(BASE_DIR, "finance.db")

# =====================
# 1. DATABASE SETUP
# =====================
def init_db():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the transactions table
    # id → auto-increment primary key
    # type → "income" or "expense"
    # amount → transaction amount
    # category → transaction category (e.g., rent, salary)
    # date → date of the transaction
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,          -- income / expense
        amount REAL NOT NULL,
        category TEXT,
        date TEXT NOT NULL
    )
    """)
    
    conn.commit()  # save changes
    conn.close()   # close connection

# =====================
# 2. ADD INCOME / EXPENSE
# =====================
def add_transaction(t_type, amount, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert a new transaction
    cursor.execute("""
    INSERT INTO transactions (type, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (t_type, amount, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()

# =====================
# 3. SUMMARY REPORT
# =====================
def show_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    total_income = cursor.fetchone()[0] or 0
    
    # Calculate total expense
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    total_expense = cursor.fetchone()[0] or 0
    
    # Balance = income - expense
    balance = total_income - total_expense
    
    # Print results
    print("\n💰 Financial Overview")
    print("---------------------")
    print(f"Total Income: {total_income:.2f} TL")
    print(f"Total Expense: {total_expense:.2f} TL")
    print(f"Remaining Balance: {balance:.2f} TL")
    
    conn.close()

# =====================
# 4. SIMPLE & COMPOUND INTEREST
# =====================
def simple_interest(principal, rate, time):
    """Simple Interest formula: A = P(1 + rt)"""
    amount = principal * (1 + (rate/100) * time)
    return round(amount, 2)

def compound_interest(principal, rate, time, n=1):
    """Compound Interest formula: A = P(1 + r/n)^(nt)"""
    amount = principal * ((1 + (rate/100)/n) ** (n * time))
    return round(amount, 2)

# =====================
# 5. MENU SYSTEM
# =====================
def main():
    init_db()  # Initialize database at program start
    
    while True:
        # Show menu options to the user
        print("\n===== Financial Tracker =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Summary Report")
        print("4. Calculate Simple Interest")
        print("5. Calculate Compound Interest")
        print("6. Exit")
        
        choice = input("Your choice: ")  # Get user choice
        
        if choice == "1":
            # Add income
            amount = float(input("Income amount: "))
            category = input("Category: ")
            add_transaction("income", amount, category)
            print("✅ Income added!")
        
        elif choice == "2":
            # Add expense
            amount = float(input("Expense amount: "))
            category = input("Category: ")
            add_transaction("expense", amount, category)
            print("✅ Expense added!")
        
        elif choice == "3":
            # Show summary report
            show_summary()
        
        elif choice == "4":
            # Simple interest calculation
            p = float(input("Principal (P): "))
            r = float(input("Interest Rate (%): "))
            t = float(input("Time (years): "))
            result = simple_interest(p, r, t)
            print(f"📊 Simple Interest Result: {result} TL")
        
        elif choice == "5":
            # Compound interest calculation
            p = float(input("Principal (P): "))
            r = float(input("Interest Rate (%): "))
            t = float(input("Time (years): "))
            n = int(input("Times interest is compounded per year (e.g., 12 for monthly): "))
            result = compound_interest(p, r, t, n)
            print(f"📊 Compound Interest Result: {result} TL")
        
        elif choice == "6":
            # Exit program
            print("👋 Exiting...")
            break
        
        else:
            # Invalid choice
            print("⚠ Invalid choice!")

# Run the menu system if the script is executed directly
if __name__ == "__main__":
    main()
