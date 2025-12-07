📘 Personal Finance Aggregator (Plaid-Like Mock)

A mock financial aggregator system inspired by Plaid, Mint, and YNAB, built to simulate real-world fintech workflows like OAuth-style bank linking, data normalization, transaction deduplication, budgeting, categorization, and scheduled sync.

This project is designed for learning, demonstration, and academic submission.

✨ Project Details
Project Title	Personal Finance Aggregator (Plaid-Like Mock)
Project Type	Application Developer
Tech Stack	FastAPI, SQLAlchemy, APScheduler, Pydantic, pytest, SQLite, React
🚀 Overview

Users often have multiple bank accounts and struggle to see their full financial picture in one place.
This system solves that by providing:

✔ Unified dashboard for all accounts
✔ Automatic spending categorization
✔ Monthly budgets & alerts
✔ Scheduled syncing of bank data
✔ Fake/mock bank APIs for development

📌 Features
🔗 1. OAuth-Style Bank Linking (Mock)

Connect mock banks (Bank A, Bank B, Bank C)

Token generation + secure storage

Token refresh simulation

🔄 2. Transaction Aggregation

Fetch raw data from mock banks

Normalize different bank formats

Schema cleaning using Pydantic

🧹 3. Deduplication + Version History

SHA-256 hash-based deduplication

Prevent duplicate transactions

(Optional) delta-history for corrected txns

🤖 4. Auto Categorization

Keyword matching

Example: “Zomato”, “Swiggy” → FOOD

User override option

💰 5. Budgets & Alerts

Category wise budgets

Alerts at 80% and 100%

🔁 6. Scheduled Sync (APScheduler)

Hourly / Daily sync

Automated fetching → normalize → dedup → categorize

🧪 7. Unit + Integration Tests (pytest)

Hashing, normalization, categorization

Sync logic

Budget alerts

🏛 System Architecture
User → OAuth-style bank link
    → Store tokens (encrypted)
    → Scheduled sync 
        → Fetch raw txns
        → Normalize schema
        → Dedup (hash)
        → Categorize (rules engine)
        → Store in DB
        → Check budgets
        → Generate alerts
    → API returns clean data

🗂 Database Design (SQLAlchemy)
Tables:

users — auth, identity

banks — mock bank providers

accounts — linked bank accounts

transactions — normalized & deduped

budgets — per-category budget

alerts — budget breach notifications

bank_mapping — bank → canonical schema mapping

registered_banks — banks user has linked

🔧 Technologies Used
Purpose	Library
API Framework	FastAPI
Database ORM	SQLAlchemy
Data Validation	Pydantic
Scheduler	APScheduler
Testing	pytest
Database	SQLite
Frontend	React
🧪 Testing Strategy

Unit tests

hashing

normalization

categorization

Integration tests

OAuth flow

fetch + sync

deduplication

budget breach detection

Success Metrics

100% CRUD for all entities

0 duplicate transactions

Sync 500 txns < 3 sec

80% test coverage

📅 Project Timeline
Week	Deliverables
W1	Mock bank API, OAuth Flow, Database schema
W2	Fetch txns, normalization, dedup, scheduler
W3	Budgets, alerts, audit logs, tests
W4	Anomaly detection, docs, demo, final README
🧩 Folder Structure (Recommended)
backend/
 ├── app/
 │    ├── routers/
 │    ├── services/
 │    ├── models/
 │    ├── schemas/
 │    ├── core/
 │    └── main.py
 ├── tests/
 └── requirements.txt

frontend/
 ├── src/
 └── package.json
