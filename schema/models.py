from db.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


# ==========================
# ENUMS
# ==========================

class TransactionType(enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TransactionCategory(enum.Enum):
    TRAVEL = "TRAVEL"
    FOOD = "FOOD"
    HOUSEHOLD = "HOUSEHOLD"
    HEALTH = "HEALTH"
    ANONYMOUS = "ANONYMOUS"
    INCOME = "INCOME"


# ==========================
# USER
# ==========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    phone_no = Column(String(15), unique=True, nullable=False)
    overall_balance_limit = Column(Float, nullable=True)  # Overall balance limit across all accounts
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"


# ==========================
# BANK
# ==========================

class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bank_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    registered_user = relationship(
        "RegisteredUser",
        back_populates="bank_account",
        cascade="all, delete-orphan",
        uselist=False
    )

    def __repr__(self):
        return f"<Bank(id={self.id}, bank={self.bank_name})>"


# ==========================
# REGISTERED USER (Bank accounts)
# ==========================

class RegisteredUser(Base):
    __tablename__ = "registered_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_number = Column(String(20), unique=True, nullable=False, index=True)
    ifsc_code = Column(String(11), nullable=False)
    phone_no = Column(String(15), nullable=False)
    email = Column(String(255), nullable=False)
    bank_id = Column(Integer, ForeignKey("bank.id", ondelete="CASCADE"), nullable=False)

    account_balance = Column(Float, default=0.0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bank_account = relationship("Bank", back_populates="registered_user")

    transactions = relationship(
        "Transaction",
        back_populates="from_account",
        foreign_keys="Transaction.from_account_id"
    )

    received_transactions = relationship(
        "Transaction",
        back_populates="to_account",
        foreign_keys="Transaction.to_account_id"
    )

    def __repr__(self):
        return f"<RegisteredUser(id={self.id}, account={self.account_number}, email={self.email})>"


# ==========================
# TRANSACTIONS (FIXED)
# ==========================

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # FIXED — Correct FKs to registered_users
    from_account_id = Column(Integer, ForeignKey("registered_users.id", ondelete="CASCADE"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("registered_users.id", ondelete="CASCADE"), nullable=True)

    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    balance_after_transaction = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    from_account = relationship(
        "RegisteredUser",
        foreign_keys=[from_account_id],
        back_populates="transactions"
    )

    to_account = relationship(
        "RegisteredUser",
        foreign_keys=[to_account_id],
        back_populates="received_transactions"
    )

    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type.value}, amount={self.amount})>"


# ==========================
# BUDGET
# ==========================

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    current_spent = Column(Float, default=0.0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="budgets")
    alerts = relationship("Alert", back_populates="budget", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Budget(id={self.id}, category={self.category.value}, limit={self.monthly_limit})>"


# ==========================
# ALERT
# ==========================

class AlertType(enum.Enum):
    BUDGET_80_PERCENT = "BUDGET_80_PERCENT"
    BUDGET_100_PERCENT = "BUDGET_100_PERCENT"
    OVERALL_BALANCE_LIMIT = "OVERALL_BALANCE_LIMIT"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    budget_id = Column(Integer, ForeignKey("budgets.id", ondelete="CASCADE"), nullable=True)
    alert_type = Column(Enum(AlertType), nullable=False)
    message = Column(String(500), nullable=False)
    is_read = Column(Integer, default=0, nullable=False)  # 0 = unread, 1 = read
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="alerts")
    budget = relationship("Budget", back_populates="alerts")

    def __repr__(self):
        return f"<Alert(id={self.id}, type={self.alert_type.value}, user_id={self.user_id})>"
