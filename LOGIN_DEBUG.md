# Login Debugging Guide

## What Was Fixed

The issue was that `getCurrentUser()` was being called BEFORE the token was stored in localStorage. The API interceptor couldn't find the token, so the request was sent without authorization, causing a 401 error.

**Fixed Flow:**
1. ✅ Login with credentials
2. ✅ Store token in localStorage FIRST
3. ✅ Call getCurrentUser() (now token is available for interceptor)
4. ✅ Update App state
5. ✅ Navigate to home

## Testing the Fix

### 1. Clear Browser Storage First

Open Developer Tools (F12) → Application tab → Storage:
- Clear **Local Storage**
- Clear **Session Storage**  
- Close Developer Tools

### 2. Try Logging In

1. Go to http://localhost:5173/login
2. Enter your credentials
3. Click Login
4. You should be redirected to home page
5. Navbar should show your email

### 3. Check If Token Is Stored

Press F12 → Console tab, type:
```javascript
localStorage.getItem('token')
localStorage.getItem('user')
```

You should see:
- Token: A long JWT string
- User: JSON object with your email and id

### 4. Verify Authentication State

After logging in:
- ✅ Navbar shows your email
- ✅ "My Posts" and "Create Post" links visible
- ✅ Can access /create, /my-posts routes
- ✅ "Login" and "Register" buttons hidden

## If Still Not Working

### Debug Step 1: Check Browser Console

Press F12 → Console tab. Look for errors like:
- 401 Unauthorized
- Network errors
- CORS errors

### Debug Step 2: Check Network Tab

F12 → Network tab:

**During Login:**
1. Look for `/api/token` request
   - Status should be 200
   - Response should have `access_token`

2. Look for `/api/users/me` request
   - Status should be 200
   - Response should have your user data
   - Request headers should have `Authorization: Bearer <token>`

### Debug Step 3: Manual Token Test

In Console (F12):
```javascript
// Check if token exists
console.log('Token:', localStorage.getItem('token'))

// Manually test API call
fetch('/api/users/me', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
})
.then(r => r.json())
.then(d => console.log('User:', d))
```

### Debug Step 4: Check Backend Response

In your backend terminal, you should see:
```
INFO:     127.0.0.1:xxxxx - "POST /token HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /users/me HTTP/1.1" 200 OK
```

If you see 401 errors, the token isn't being sent correctly.

## Common Issues & Solutions

### Issue 1: "Not Authenticated" Message
**Cause**: Token not stored or expired
**Solution**: 
- Clear localStorage and login again
- Check token exists: `localStorage.getItem('token')`

### Issue 2: Redirected Back to Login
**Cause**: Protected route checking authentication
**Solution**:
- Verify `isAuthenticated` state in App.jsx
- Check token is in localStorage

### Issue 3: Navbar Doesn't Update
**Cause**: App state not updating
**Solution**:
- Check `onLogin()` is being called
- Verify state updates in App.jsx

### Issue 4: 401 on API Calls After Login
**Cause**: Token not being sent in headers
**Solution**:
- Check axios interceptor in api.js
- Verify token format: "Bearer <token>"

## Testing Checklist

- [ ] Clear localStorage before testing
- [ ] Register a new account (if needed)
- [ ] Login with correct credentials
- [ ] Check token in localStorage
- [ ] Check user object in localStorage
- [ ] Verify navbar shows email
- [ ] Try creating a post
- [ ] Try viewing "My Posts"
- [ ] Logout and verify localStorage cleared
- [ ] Login again to confirm persistence

## If Everything Works

You should now be able to:
1. ✅ Register new account
2. ✅ Login successfully  
3. ✅ Stay logged in (token persists)
4. ✅ Access protected routes
5. ✅ Create/edit/delete posts
6. ✅ Vote on posts
7. ✅ Logout properly

## Still Having Issues?

Check these files:
- `frontend/src/pages/Login.jsx` - Updated with correct flow
- `frontend/src/services/api.js` - Axios interceptor adds token
- `frontend/src/App.jsx` - Manages auth state

Make sure your backend is running and accessible at http://localhost:8000
