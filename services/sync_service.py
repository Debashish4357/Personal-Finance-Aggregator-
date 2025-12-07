# services/sync_service.py
"""
Scheduled Sync Service
Automated fetching → normalize → dedup → categorize → store → check budgets → generate alerts
"""

from sqlalchemy.orm import Session
from db.database import SessionLocal
from schema.models import Transaction, TransactionCategory, RegisteredUser, Budget
from controller.AlertController import check_and_generate_budget_alerts, check_overall_balance_limit_alert
from controller.TransactionController import create_transaction
from datetime import datetime, timedelta
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_transaction_hash(transaction_data: dict) -> str:
    """Generate SHA-256 hash for transaction deduplication"""
    # Create a unique string from transaction data
    hash_string = f"{transaction_data.get('from_account_id')}_{transaction_data.get('amount')}_{transaction_data.get('transaction_date')}_{transaction_data.get('category')}"
    return hashlib.sha256(hash_string.encode()).hexdigest()


def normalize_transaction(raw_transaction: dict) -> dict:
    """Normalize different bank formats to canonical schema"""
    # This is a mock normalization - in real scenario, you'd have different bank formats
    normalized = {
        'from_account_id': raw_transaction.get('from_account_id'),
        'to_account_id': raw_transaction.get('to_account_id'),
        'transaction_type': raw_transaction.get('transaction_type'),
        'amount': float(raw_transaction.get('amount', 0)),
        'category': raw_transaction.get('category', TransactionCategory.ANONYMOUS),
        'transaction_date': raw_transaction.get('transaction_date', datetime.utcnow()),
        'balance_after_transaction': raw_transaction.get('balance_after_transaction', 0)
    }
    return normalized


def auto_categorize_transaction(description: str = "", amount: float = 0) -> TransactionCategory:
    """Auto-categorize transaction based on keywords"""
    description_lower = description.lower()
    
    # Food keywords
    food_keywords = ['zomato', 'swiggy', 'uber eats', 'food', 'restaurant', 'cafe', 'pizza', 'burger', 'mcdonalds', 'kfc']
    if any(keyword in description_lower for keyword in food_keywords):
        return TransactionCategory.FOOD
    
    # Travel keywords
    travel_keywords = ['uber', 'ola', 'taxi', 'flight', 'hotel', 'booking', 'travel', 'train', 'bus', 'metro']
    if any(keyword in description_lower for keyword in travel_keywords):
        return TransactionCategory.TRAVEL
    
    # Health keywords
    health_keywords = ['pharmacy', 'hospital', 'clinic', 'medicine', 'doctor', 'health', 'medical']
    if any(keyword in description_lower for keyword in health_keywords):
        return TransactionCategory.HEALTH
    
    # Household keywords
    household_keywords = ['grocery', 'supermarket', 'walmart', 'target', 'home', 'electricity', 'water', 'gas', 'utility']
    if any(keyword in description_lower for keyword in household_keywords):
        return TransactionCategory.HOUSEHOLD
    
    # Income keywords
    income_keywords = ['salary', 'income', 'payment received', 'refund', 'deposit']
    if any(keyword in description_lower for keyword in income_keywords):
        return TransactionCategory.INCOME
    
    # Default to anonymous if no match
    return TransactionCategory.ANONYMOUS


def check_duplicate_transaction(db: Session, transaction_hash: str, from_account_id: int, amount: float, transaction_date: datetime) -> bool:
    """Check if transaction already exists (deduplication)"""
    # Check for duplicate within a time window (e.g., same day)
    start_date = transaction_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1)
    
    existing = db.query(Transaction).filter(
        Transaction.from_account_id == from_account_id,
        Transaction.amount == amount,
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date < end_date
    ).first()
    
    return existing is not None


def update_budget_spent(db: Session, user_id: int, category: TransactionCategory, amount: float):
    """Update budget spent amount for a category"""
    budget = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category == category
    ).first()
    
    if budget:
        budget.current_spent += amount
        db.flush()


def sync_transactions_for_account(db: Session, account_id: int):
    """Sync transactions for a specific account"""
    try:
        account = db.query(RegisteredUser).filter(RegisteredUser.id == account_id).first()
        if not account:
            logger.warning(f"Account {account_id} not found")
            return
        
        # In a real scenario, you would fetch transactions from external bank API
        # For now, we'll simulate by checking recent transactions and processing them
        # This is a mock - you would replace this with actual bank API calls
        
        logger.info(f"Syncing transactions for account {account_id}")
        
        # Get recent transactions (last 24 hours) that might need processing
        # In real scenario, fetch from bank API
        # For now, we'll just check budgets and generate alerts
        
    except Exception as e:
        logger.error(f"Error syncing account {account_id}: {str(e)}")


def sync_all_accounts():
    """Sync all registered accounts"""
    db = SessionLocal()
    try:
        accounts = db.query(RegisteredUser).all()
        logger.info(f"Starting sync for {len(accounts)} accounts")
        
        for account in accounts:
            sync_transactions_for_account(db, account.id)
        
        db.commit()
        logger.info("Sync completed successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during sync: {str(e)}")
    finally:
        db.close()


def update_budget_spent_for_transactions():
    """Update budget spent based on all DEBIT transactions"""
    db = SessionLocal()
    try:
        from schema.models import Transaction, TransactionType, User
        
        # Get all DEBIT transactions
        debit_transactions = db.query(Transaction).filter(
            Transaction.transaction_type == TransactionType.DEBIT
        ).all()
        
        # Reset all budgets to 0
        budgets = db.query(Budget).all()
        for budget in budgets:
            budget.current_spent = 0.0
        
        # Calculate spent for each budget based on transactions
        for tx in debit_transactions:
            # Find user_id from account email
            account = db.query(RegisteredUser).filter(RegisteredUser.id == tx.from_account_id).first()
            if account:
                # Try to find user by email
                user = db.query(User).filter(User.email == account.email).first()
                if user:
                    budget = db.query(Budget).filter(
                        Budget.user_id == user.id,
                        Budget.category == tx.category
                    ).first()
                    if budget:
                        budget.current_spent += tx.amount
        
        db.commit()
        logger.info("Updated budget spent amounts based on transactions")
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating budget spent: {str(e)}")
    finally:
        db.close()


def check_budgets_and_generate_alerts():
    """Check all budgets and generate alerts"""
    db = SessionLocal()
    try:
        from schema.models import User
        
        # First update budget spent amounts
        update_budget_spent_for_transactions()
        
        users = db.query(User).all()
        logger.info(f"Checking budgets for {len(users)} users")
        
        for user in users:
            # Check category budgets
            alerts = check_and_generate_budget_alerts(db, user.id)
            if alerts:
                logger.info(f"Generated {len(alerts)} budget alerts for user {user.id}")
            
            # Check overall balance limit
            accounts = db.query(RegisteredUser).filter(RegisteredUser.email == user.email).all()
            total_balance = sum(acc.account_balance for acc in accounts)
            
            alert = check_overall_balance_limit_alert(db, user.id, total_balance)
            if alert:
                logger.info(f"Generated overall balance limit alert for user {user.id}")
        
        db.commit()
        logger.info("Budget check and alert generation completed")
    except Exception as e:
        db.rollback()
        logger.error(f"Error checking budgets: {str(e)}")
    finally:
        db.close()


def full_sync_workflow():
    """Complete sync workflow: fetch → normalize → dedup → categorize → store → check budgets → generate alerts"""
    logger.info("=" * 50)
    logger.info("Starting full sync workflow")
    logger.info("=" * 50)
    
    # Step 1: Sync all accounts (fetch transactions)
    # In a real scenario, this would fetch from external bank APIs
    logger.info("Step 1: Syncing accounts...")
    sync_all_accounts()
    
    # Step 2: Update budget spent amounts based on transactions
    logger.info("Step 2: Updating budget spent amounts...")
    update_budget_spent_for_transactions()
    
    # Step 3: Check budgets and generate alerts
    logger.info("Step 3: Checking budgets and generating alerts...")
    check_budgets_and_generate_alerts()
    
    logger.info("=" * 50)
    logger.info("Full sync workflow completed")
    logger.info("=" * 50)

