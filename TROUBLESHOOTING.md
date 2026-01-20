# Common Issues and Solutions

## Backend Issues

### 1. Database Connection Error
**Error**: `could not connect to server`

**Solutions**:
- Ensure PostgreSQL is running
- Check `.env` file has correct credentials
- Verify database exists: `psql -l` (should show 'blogsite')
- Try creating database: `createdb blogsite`

### 2. Import Errors
**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solutions**:
- Activate virtual environment: `venv\Scripts\activate`
- Install requirements: `pip install -r requirements.txt`

### 3. Alembic Migration Issues
**Error**: `Target database is not up to date`

**Solutions**:
```bash
# Check current revision
alembic current

# Apply all migrations
alembic upgrade head

# If tables exist but alembic doesn't know, stamp it
alembic stamp head
```

### 4. CORS Errors
**Error**: `Access-Control-Allow-Origin`

**Solution**: Backend already has CORS configured for all origins. If still getting errors:
- Check backend is running on port 8000
- Verify frontend proxy in `vite.config.js` is correct

## Frontend Issues

### 1. npm install fails
**Error**: Various package installation errors

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### 2. Port Already in Use
**Error**: `Port 5173 is already in use`

**Solutions**:
- Kill the process: 
  - Windows: Find and end the process in Task Manager
  - Or change port in `vite.config.js`: `port: 5174`

### 3. API Calls Return 401
**Error**: Unauthorized errors on API calls

**Solutions**:
- Clear localStorage: Open DevTools (F12) → Application → Local Storage → Clear
- Login again
- Check token in localStorage exists
- Verify backend is running

### 4. Blank Page After Login
**Solutions**:
- Open DevTools Console (F12) to see errors
- Check if backend is running and accessible
- Verify API URL in `api.js` is correct
- Check CORS settings

## Authentication Issues

### Can't Register
**Possible causes**:
- Email already exists
- Backend not running
- Database connection issue

**Solutions**:
- Try different email
- Check backend logs
- Verify database is accessible

### Can't Login
**Possible causes**:
- Wrong credentials
- User doesn't exist
- Token generation failing

**Solutions**:
- Double-check email and password
- Register if haven't already
- Check backend logs for errors
- Verify SECRET_KEY is set in .env

### Token Expired
**Error**: 401 errors after some time

**Solution**: This is normal - tokens expire after 30 minutes. Just login again.

## Post/Vote Issues

### Can't Create Post
**Possible causes**:
- Not authenticated
- Missing required fields

**Solutions**:
- Ensure you're logged in
- Check console for validation errors
- Title and content are required

### Voting Doesn't Work
**Possible causes**:
- Not authenticated  
- Already voted (for upvote)
- Haven't voted (for downvote)

**Solutions**:
- Ensure you're logged in
- Backend prevents duplicate votes
- Downvote only works if you've upvoted

### Can't Edit/Delete Post
**Error**: 403 Forbidden

**Solution**: You can only edit/delete your own posts. This is correct behavior.

## Development Tips

### Check if Backend is Running
Open http://localhost:8000/docs - should see FastAPI docs

### Check if Frontend is Running
Open http://localhost:5173 - should see BlogSite homepage

### View Backend Logs
Terminal running `uvicorn` shows all API requests and errors

### View Frontend Errors
Press F12 → Console tab to see JavaScript errors

### Test API Directly
Use http://localhost:8000/docs to test API endpoints without frontend

## Getting Help

1. Check browser console (F12) for errors
2. Check backend terminal for error messages
3. Verify all environment variables are set
4. Make sure both servers are running
5. Try clearing browser cache and localStorage

## Useful Commands

```bash
# Backend
venv\Scripts\activate              # Activate virtual environment
cd app && uvicorn main:app --reload  # Run backend
alembic upgrade head               # Run migrations
alembic current                    # Check current migration

# Frontend
cd frontend
npm install                        # Install dependencies
npm run dev                        # Run development server
npm run build                      # Build for production

# Database
psql -U postgres                   # Connect to PostgreSQL
\l                                 # List databases
\c blogsite                        # Connect to blogsite database
\dt                                # List tables
```

## Still Having Issues?

1. Delete and recreate virtual environment
2. Delete node_modules and reinstall
3. Drop and recreate database
4. Check all file paths are correct
5. Ensure all dependencies are installed
