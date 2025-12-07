# Alerts and Scheduled Sync Setup Guide

## ✅ Features Implemented

### 1. Alerts System
- ✅ Alerts table/model for budget breach notifications
- ✅ Automatic alerts at 80% and 100% budget usage
- ✅ Overall balance limit alerts
- ✅ Alert generation and display in UI
- ✅ Alert routes and API endpoints

### 2. Scheduled Sync (APScheduler)
- ✅ Hourly/daily automated sync
- ✅ Complete workflow: fetch → normalize → dedup → categorize → store → check budgets → generate alerts
- ✅ Background scheduler integration
- ✅ Manual sync trigger endpoint

## 📋 Setup Instructions

### Step 1: Install Dependencies

Add APScheduler to your requirements:
```bash
pip install APScheduler
```

Or add to requirements.txt:
```
APScheduler>=3.10.0
```

### Step 2: Run Database Migration

Create the alerts table:
```bash
python add_alerts_table.py
```

This will create the `alerts` table with the following structure:
- `id` - Primary key
- `user_id` - Foreign key to users
- `budget_id` - Foreign key to budgets (nullable)
- `alert_type` - Enum (BUDGET_80_PERCENT, BUDGET_100_PERCENT, OVERALL_BALANCE_LIMIT)
- `message` - Alert message
- `is_read` - Read status (0 = unread, 1 = read)
- `created_at` - Timestamp

### Step 3: Start the Server

The scheduler will automatically start when you run the server:
```bash
python server.py
```

The scheduler will:
- Run hourly sync (every 1 hour)
- Run daily sync (at midnight)
- Check budgets and generate alerts automatically

## 🔧 API Endpoints

### Alerts Endpoints

1. **Get User Alerts**
   - `GET /alerts/user/{user_id}?unread_only=false`
   - Returns all alerts for a user

2. **Get Alert by ID**
   - `GET /alerts/{alert_id}`
   - Returns specific alert

3. **Mark Alert as Read**
   - `POST /alerts/{alert_id}/read`
   - Marks an alert as read

4. **Mark All Alerts as Read**
   - `POST /alerts/user/{user_id}/read-all`
   - Marks all user alerts as read

5. **Delete Alert**
   - `DELETE /alerts/{alert_id}`
   - Deletes an alert

### Sync Endpoints

1. **Manual Sync Trigger**
   - `POST /budgets/trigger-sync`
   - Manually triggers the sync workflow

## 🎯 How It Works

### Alert Generation

Alerts are automatically generated when:
1. **Budget reaches 80%**: Warning alert
2. **Budget reaches 100%**: Critical alert
3. **Overall balance exceeds limit**: Critical alert

The sync service checks all budgets and generates alerts if thresholds are met.

### Scheduled Sync Workflow

1. **Sync Accounts**: Fetches transactions from all registered accounts
2. **Update Budget Spent**: Calculates spent amounts based on DEBIT transactions
3. **Check Budgets**: Compares spent vs limits
4. **Generate Alerts**: Creates alerts for budget breaches

## 🖥️ Frontend

### Alerts Page
- View all alerts or unread only
- Mark alerts as read
- Delete alerts
- Color-coded alerts (yellow for warnings, red for critical)

### Dashboard
- Shows alert count
- Link to Alerts page

## 📝 Notes

- The scheduler runs in the background
- Sync logs are written to console
- Alerts are only generated once per threshold (no duplicates)
- Budget spent is recalculated on each sync based on all DEBIT transactions

## 🧪 Testing

1. Create a budget with a low limit
2. Add transactions that exceed the budget
3. Trigger manual sync: `POST /budgets/trigger-sync`
4. Check alerts: `GET /alerts/user/{user_id}`
5. View alerts in the UI at `Alerts.html`

## 🔍 Monitoring

Check server logs to see:
- Sync execution times
- Number of alerts generated
- Any errors during sync

The scheduler logs all activities with timestamps.

