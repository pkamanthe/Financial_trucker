import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, FinancialRecord

DATABASE_URL = "sqlite:///financial_records.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(engine)
    print("Database Initialized")

def create_user():
    """Create a new user."""
    name = input("Enter User name: ").strip()
    email = input("Enter User email: ").strip()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    print(f"User '{name}' created with ID {user.id}")

def view_users():
    """View all users in the system."""
    users = session.query(User).all()
    if not users:
        print("No users found.")
        return

    print("\nUsers:")
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

def create_financial_record():
    """Create a new financial record for a user."""
    try:
        user_id = int(input("Enter User ID for the financial record: ").strip())
        user = session.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} does not exist.")
            return

        amount = float(input("Enter the amount: ").strip())
        type_ = input("Enter the type ('income' or 'expense'): ").strip().lower()
        if type_ not in ['income', 'expense']:
            print("Invalid type. Please enter 'income' or 'expense'.")
            return

        date_ = input("Enter the date (YYYY-MM-DD): ").strip()
        date_ = datetime.strptime(date_, "%Y-%m-%d").date()

        record = FinancialRecord(amount=amount, type=type_, date=date_, user_id=user_id)
        session.add(record)
        session.commit()
        print(f"Financial record created with ID {record.id} for User '{user.name}'.")
    except ValueError as ve:
        print(f"Error: {ve}. Please ensure your inputs are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def update_financial_record():
    """Update an existing financial record."""
    try:
        record_id = int(input("Enter Financial Record ID to update: ").strip())
        record = session.get(FinancialRecord, record_id)
        if not record:
            print(f"Financial record with ID {record_id} does not exist.")
            return

        record.amount = float(input(f"Enter new amount (current: {record.amount}): ").strip() or record.amount)
        record.type = input(f"Enter new type ('income' or 'expense', current: {record.type}): ").strip() or record.type
        new_date = input(f"Enter new date (YYYY-MM-DD, current: {record.date}): ").strip()
        if new_date:
            record.date = datetime.strptime(new_date, "%Y-%m-%d").date()

        session.commit()
        print(f"Financial record ID {record_id} updated successfully.")
    except ValueError as ve:
        print(f"Error: {ve}. Please ensure your inputs are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def delete_financial_record():
    """Delete a financial record."""
    try:
        record_id = int(input("Enter Financial Record ID to delete: ").strip())
        record = session.get(FinancialRecord, record_id)

        if not record:
            print(f"Financial record with ID {record_id} does not exist.")
            return

        session.delete(record)
        session.commit()
        print(f"Financial record ID {record_id} deleted successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def view_financial_records():
    """View all financial records."""
    records = session.query(FinancialRecord).all()
    if not records:
        print("No financial records found.")
        return

    print("\nFinancial Records:")
    for record in records:
        print(f"ID: {record.id}, User ID: {record.user_id}, Type: {record.type}, Amount: {record.amount}, Date: {record.date}")

def track_savings_progress():
    """Track savings progress for a specific user."""
    try:
        user_id = int(input("Enter User ID to track savings progress: ").strip())
        user = session.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} does not exist.")
            return

        total_income = sum(record.amount for record in user.financial_records if record.type == "income")
        total_expenses = sum(record.amount for record in user.financial_records if record.type == "expense")
        savings = total_income - total_expenses

        print(f"\nUser '{user.name}' savings progress:")
        print(f"Total Income: {total_income}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Total Savings: {savings}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def view_reports():
    """Generate a financial report for a specific user."""
    try:
        user_id = int(input("Enter User ID for report: ").strip())
        user = session.get(User, user_id)
        if not user:
            print(f"User with ID {user_id} does not exist.")
            return

        total_income = sum(record.amount for record in user.financial_records if record.type == "income")
        total_expenses = sum(record.amount for record in user.financial_records if record.type == "expense")

        print(f"\nFinancial Report for User '{user.name}' (ID: {user.id}):")
        print(f"Total Income: {total_income}")
        print(f"Total Expenses: {total_expenses}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main_menu():
    """Display the main menu and handle user actions."""
    while True:
        print("\nWelcome to the Financial Record Application. What would you like to do?")
        print("1. Create User")
        print("2. Create Financial Record")
        print("3. Update Financial Record")
        print("4. Delete Financial Record")
        print("5. View All Financial Records")
        print("6. Track Savings Progress")
        print("7. View Users")
        print("8. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_user()
        elif choice == "2":
            create_financial_record()
        elif choice == "3":
            update_financial_record()
        elif choice == "4":
            delete_financial_record()
        elif choice == "5":
            view_financial_records()
        elif choice == "6":
            track_savings_progress()
        elif choice == "7":
            view_users()
        elif choice == "8":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    init_db()
    main_menu()
