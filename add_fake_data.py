#!/usr/bin/env python3
"""
Script to add fake data to the database:
- 10-12 banks
- 5 fake users
- 50 transactions (10 anonymous, rest with other categories)
"""

from db.database import SessionLocal
from schema.models import Bank, User, RegisteredUser, Transaction, TransactionType, TransactionCategory
from controller.userController import create_user
from controller.BankController import create_bank
from controller.RegisteredAccountController import create_registered_account
from controller.TransactionController import create_transaction
from datetime import datetime, timedelta
import random
import hashlib

# Bank names
BANKS = [
    "State Bank of India",
    "HDFC Bank",
    "ICICI Bank",
    "Axis Bank",
    "Kotak Mahindra Bank",
    "Punjab National Bank",
    "Bank of Baroda",
    "Canara Bank",
    "Union Bank of India",
    "Indian Bank",
    "IDBI Bank",
    "Yes Bank"
]

# Fake users data
FAKE_USERS = [
    {"name": "Rajesh Kumar", "email": "rajesh.kumar@example.com", "password": "password123", "phone_no": "9876543210"},
    {"name": "Priya Sharma", "email": "priya.sharma@example.com", "password": "password123", "phone_no": "9876543211"},
    {"name": "Amit Patel", "email": "amit.patel@example.com", "password": "password123", "phone_no": "9876543212"},
    {"name": "Sneha Reddy", "email": "sneha.reddy@example.com", "password": "password123", "phone_no": "9876543213"},
    {"name": "Vikram Singh", "email": "vikram.singh@example.com", "password": "password123", "phone_no": "9876543214"}
]

# Transaction categories (excluding ANONYMOUS for now)
CATEGORIES = [
    TransactionCategory.TRAVEL,
    TransactionCategory.FOOD,
    TransactionCategory.HOUSEHOLD,
    TransactionCategory.HEALTH,
    TransactionCategory.INCOME
]

def generate_account_number():
    """Generate a random account number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def generate_ifsc():
    """Generate a random IFSC code"""
    bank_code = random.choice(['SBIN', 'HDFC', 'ICIC', 'AXIS', 'KKBK', 'PNB', 'BARB', 'CNRB', 'UBIN', 'IDIB', 'YESB'])
    branch_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"{bank_code}0{branch_code}"

def main():
    db = SessionLocal()
    
    try:
        print("Starting to add fake data...")
        
        # 1. Add Banks (10-12 banks)
        print("\n1. Adding banks...")
        bank_ids = []
        for bank_name in BANKS:
            # Check if bank already exists
            existing_bank = db.query(Bank).filter(Bank.bank_name == bank_name).first()
            if existing_bank:
                print(f"  Bank '{bank_name}' already exists (ID: {existing_bank.id})")
                bank_ids.append(existing_bank.id)
            else:
                bank = create_bank(db, bank_name)
                db.commit()
                bank_ids.append(bank.id)
                print(f"  Added bank: {bank_name} (ID: {bank.id})")
        
        # 2. Add Users (5 fake users)
        print("\n2. Adding users...")
        user_ids = []
        for user_data in FAKE_USERS:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"  User '{user_data['name']}' already exists (ID: {existing_user.id})")
                user_ids.append(existing_user.id)
            else:
                user = create_user(
                    db,
                    user_data["name"],
                    user_data["email"],
                    user_data["password"],
                    user_data["phone_no"]
                )
                db.commit()
                user_ids.append(user.id)
                print(f"  Added user: {user_data['name']} (ID: {user.id})")
        
        # 3. Add Registered Accounts (bank accounts) for transactions
        print("\n3. Adding registered accounts...")
        account_ids = []
        for i, user_data in enumerate(FAKE_USERS):
            # Create 1-2 accounts per user
            num_accounts = random.randint(1, 2)
            for j in range(num_accounts):
                account_number = generate_account_number()
                # Check if account already exists
                existing_account = db.query(RegisteredUser).filter(RegisteredUser.account_number == account_number).first()
                if existing_account:
                    account_ids.append(existing_account.id)
                    continue
                
                account = create_registered_account(
                    db,
                    account_number=account_number,
                    ifsc_code=generate_ifsc(),
                    phone_no=user_data["phone_no"],
                    email=user_data["email"],
                    bank_id=random.choice(bank_ids),
                    account_balance=random.uniform(10000, 100000)
                )
                # Note: create_registered_account already commits
                account_ids.append(account.id)
                print(f"  Added account: {account_number} (ID: {account.id}, Balance: ₹{account.account_balance:.2f})")
        
        if not account_ids:
            print("  No accounts available. Creating at least one account...")
            account = create_registered_account(
                db,
                account_number=generate_account_number(),
                ifsc_code=generate_ifsc(),
                phone_no=FAKE_USERS[0]["phone_no"],
                email=FAKE_USERS[0]["email"],
                bank_id=bank_ids[0],
                account_balance=50000.0
            )
            # Note: create_registered_account already commits
            account_ids.append(account.id)
        
        # 4. Add Transactions (50 transactions: 10 anonymous, 40 with other categories)
        print("\n4. Adding transactions...")
        transaction_count = 0
        anonymous_count = 0
        
        # First, add 10 anonymous transactions
        for _ in range(10):
            if not account_ids:
                break
            from_account_id = random.choice(account_ids)
            account = db.query(RegisteredUser).filter(RegisteredUser.id == from_account_id).first()
            
            if account:
                amount = round(random.uniform(100, 5000), 2)
                transaction_type = random.choice([TransactionType.CREDIT, TransactionType.DEBIT])
                
                # Update balance based on transaction type
                if transaction_type == TransactionType.DEBIT:
                    account.account_balance -= amount
                else:  # CREDIT
                    account.account_balance += amount
                
                transaction_date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                
                tx = Transaction(
                    from_account_id=from_account_id,
                    transaction_type=transaction_type,
                    amount=amount,
                    category=TransactionCategory.ANONYMOUS,
                    transaction_date=transaction_date,
                    balance_after_transaction=round(account.account_balance, 2)
                )
                db.add(tx)
                transaction_count += 1
                anonymous_count += 1
        
        # Add remaining 40 transactions with other categories
        for _ in range(40):
            if not account_ids:
                break
            from_account_id = random.choice(account_ids)
            account = db.query(RegisteredUser).filter(RegisteredUser.id == from_account_id).first()
            
            if account:
                category = random.choice(CATEGORIES)
                amount = round(random.uniform(50, 10000), 2)
                transaction_type = random.choice([TransactionType.CREDIT, TransactionType.DEBIT])
                
                # Update balance based on transaction type
                if transaction_type == TransactionType.DEBIT:
                    account.account_balance -= amount
                else:  # CREDIT
                    account.account_balance += amount
                
                transaction_date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                
                tx = Transaction(
                    from_account_id=from_account_id,
                    transaction_type=transaction_type,
                    amount=amount,
                    category=category,
                    transaction_date=transaction_date,
                    balance_after_transaction=round(account.account_balance, 2)
                )
                db.add(tx)
                transaction_count += 1
        
        db.commit()
        print(f"  Added {transaction_count} transactions ({anonymous_count} anonymous, {transaction_count - anonymous_count} with categories)")
        
        print("\n✅ Fake data added successfully!")
        print(f"\nSummary:")
        print(f"  - Banks: {len(bank_ids)}")
        print(f"  - Users: {len(user_ids)}")
        print(f"  - Accounts: {len(account_ids)}")
        print(f"  - Transactions: {transaction_count} (10 anonymous, {transaction_count - 10} with categories)")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()

