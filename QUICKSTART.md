# Quick Start Guide

## First Time Setup (Do this once)

### 1. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database credentials
# See .env.example for required variables

# Run database migrations
alembic upgrade head
```

### 2. Frontend Setup

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Go back to root
cd ..
```

## Running the Application

### Option 1: Use the startup script (Windows)
Simply double-click `start-dev.bat` in the project root folder.

### Option 2: Manual start

**Terminal 1 - Backend:**
```bash
venv\Scripts\activate
cd app
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## First Steps

1. Open http://localhost:5173
2. Click "Register" to create an account
3. Login with your new account
4. Start creating posts!

## Troubleshooting

### Backend won't start
- Make sure PostgreSQL is running
- Check your .env file has correct database credentials
- Ensure virtual environment is activated

### Frontend won't start
- Make sure you ran `npm install`
- Check if port 5173 is available
- Try `npm cache clean --force` and reinstall

### Can't login/register
- Check backend is running on port 8000
- Open browser console (F12) to see error messages
- Verify database connection is working
