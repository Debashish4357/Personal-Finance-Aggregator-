# How to Run the Project

## Prerequisites

1. **Python 3.8+** installed
2. **MySQL** database running
3. **Database `pfa-b`** created in MySQL

## Step 1: Install Python Dependencies

Open a terminal in the project root directory and run:

```bash
pip install fastapi uvicorn sqlalchemy pymysql pydantic pyjwt python-multipart
```

Or if you prefer to create a requirements.txt, install from it:
```bash
pip install -r requirements.txt
```

## Step 2: Setup Database

1. Make sure MySQL is running
2. Create the database (if not already created):
   ```sql
   CREATE DATABASE `pfa-b`;
   ```
3. The database connection is configured in `db/database.py`:
   - Host: `localhost`
   - Port: `3306`
   - Database: `pfa-b`
   - User: `root`
   - Password: `hanuman77`
   
   **Note:** If your MySQL credentials are different, update `db/database.py`

## Step 3: Run the Backend Server

Navigate to the project directory and run:

```bash
cd Personal-Finance-Aggregator-
python server.py
```

Or using uvicorn directly:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The backend will start at: **http://localhost:8000**

You can verify it's running by visiting: http://localhost:8000

## Step 4: Open the Frontend

Since the frontend is now in HTML/CSS, you have two options:

### Option A: Open Directly in Browser
1. Navigate to `frontend_components` folder
2. Double-click `Login.html` or `Signup.html` to open in your default browser

### Option B: Use a Simple HTTP Server (Recommended for CORS)
If you encounter CORS issues, use Python's built-in HTTP server:

```bash
cd frontend_components
python -m http.server 8080
```

Then open in browser: **http://localhost:8080/Login.html**

## Quick Test

1. Start the backend server (Step 3)
2. Open `Login.html` or `Signup.html` in your browser
3. Try signing up a new user
4. Then login with those credentials

## Troubleshooting

- **Database Connection Error**: Make sure MySQL is running and the database exists
- **CORS Errors**: Use Option B for frontend (HTTP server) instead of opening files directly
- **Port Already in Use**: Change the port in `server.py` or stop the process using port 8000
- **Module Not Found**: Make sure all dependencies are installed (Step 1)

