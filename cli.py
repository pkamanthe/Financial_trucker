import sys
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, FinancialRecord

DATABASE_URL = "sqlite:///financial_records.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    # Initialize Database
    Base.metadata.create_all(engine)
    print("Database Initialized")

def create_user():
    # Create new user
    name = input("Enter User name: ")
    email = input("Enter User email: ")
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    print(f"User '{name}' created with ID {user.id}")

def create_financial_record():
    # Create a financial record
    user_id = int(input("Enter User ID for the financial record: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist.")
        return
    amount = float(input("Enter the amount: "))
    type_ = input("Enter the type ('income' or 'expense'): ").lower()
    date_ = input("Enter the date (YYYY-MM-DD): ")
    record = FinancialRecord(amount=amount, type=type_, date=date_, user_id=user_id)
    session.add(record)
    session.commit()
    print(f"Financial record created with ID {record.id} for User '{user.name}'.")

def update_financial_record():
    record_id = int(input("Enter Financial Record ID to update: "))
    record = session.get(FinancialRecord, record_id)
    if not record:
        print(f"Financial record with ID {record_id} does not exist.")
        return
    record.amount = float(input(f"Enter new amount (current: {record.amount}): ") or record.amount)
    record.type = input(f"Enter new type ('income' or 'expense', current: {record.type}): ") or record.type
    record.date = input(f"Enter new date (current: {record.date}): ") or record.date
    session.commit()
    print(f"Financial record ID {record_id} updated successfully.")

def delete_financial_record():
    record_id = int(input("Enter Financial Record ID to delete: "))
    record = session.get(FinancialRecord, record_id)

    if not record:
        print(f"Financial record with ID {record_id} does not exist. Available records are:")
        records = session.query(FinancialRecord).all()
        if records:
            for rec in records:
                print(f"ID: {rec.id}, Type: {rec.record_type}, Amount: {rec.amount}")
        else:
            print("No financial records available.")
        return

    session.delete(record)
    session.commit()
    print(f"Financial record ID {record_id} deleted successfully.")

def view_financial_records():
    records = session.query(FinancialRecord).all()
    if not records:
        print("No financial records found.")
        return
    for record in records:
        print(record)

def track_savings_progress():
    user_id = int(input("Enter User ID to track savings progress: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist.")
        return
    
    # Sum all income records for the user
    total_income = sum(record.amount for record in user.financial_records if record.type == "income")
    
    # Sum all expense records for the user
    total_expenses = sum(record.amount for record in user.financial_records if record.type == "expense")
    
    # Calculate total savings
    savings = total_income - total_expenses
    
    # Display results
    print(f"User '{user.name}' savings progress:")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Total Savings: {savings}")

def view_reports():
    # Reports: View income and expenses by user
    user_id = int(input("Enter User ID for report: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist.")
        return
    print(f"Financial Report for User '{user.name}' (ID: {user.id}):")
    total_income = sum(record.amount for record in user.financial_records if record.type == "income")
    total_expenses = sum(record.amount for record in user.financial_records if record.type == "expense")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")

def main_menu():
    while True:
        print("\nWelcome to the Financial Record Application. What would you like to do?")
        print("1. Create User")
        print("2. Create Financial Record")
        print("3. Update Financial Record")
        print("4. Delete Financial Record")
        print("5. View All Financial Records")
        print("6. Exit")
        choice = input("Enter your choice: ")

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
            print("Exiting.......")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    init_db()
    main_menu()
