# BlogSite - FastAPI + React Full Stack Application

A full-stack blog application built with FastAPI backend and React frontend.

## Features

- 🔐 User Authentication (JWT-based)
- 📝 Create, Read, Update, Delete Posts
- 👍 Upvote/Downvote Posts
- 🔍 Search Posts
- 👤 User Profile & My Posts
- 📱 Responsive Design with Tailwind CSS

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLModel** - ORM for database operations
- **Alembic** - Database migrations
- **JWT** - Authentication
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling

## Project Structure

```
BlogSite-FastAPI/
├── app/
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── post.py          # Post CRUD operations
│   │   ├── user.py          # User operations
│   │   └── vote.py          # Voting system
│   ├── main.py              # FastAPI app configuration
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   ├── config.py            # Configuration settings
│   └── utils.py             # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── PostCard.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── CreatePost.jsx
│   │   │   ├── EditPost.jsx
│   │   │   ├── PostDetail.jsx
│   │   │   └── MyPosts.jsx
│   │   ├── services/
│   │   │   └── api.js       # API integration
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── alembic/                 # Database migrations
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL

### Backend Setup

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=blogsite
   DATABASE_USERNAME=postgres
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Set up the database**
   ```bash
   # Create the database in PostgreSQL
   createdb blogsite
   
   # Run migrations
   alembic upgrade head
   ```

5. **Run the backend server**
   ```bash
   cd app
   uvicorn main:app --reload
   ```
   
   The API will be available at `http://localhost:8000`
   
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user info

### Users
- `POST /users/` - Register new user
- `GET /users/{id}` - Get user by ID

### Posts
- `GET /posts/` - Get all posts (with pagination and search)
- `GET /posts/{id}` - Get single post
- `GET /posts/me` - Get current user's posts
- `POST /posts/` - Create new post (requires auth)
- `PATCH /posts/{id}` - Update post (requires auth & ownership)
- `DELETE /posts/{id}` - Delete post (requires auth & ownership)

### Votes
- `POST /vote/` - Vote on a post (dir: 1 for upvote, 0 to remove vote)

## Usage

1. **Register a new account**
   - Navigate to `/register`
   - Enter email and password
   - Click "Register"

2. **Login**
   - Navigate to `/login`
   - Enter your credentials
   - You'll be redirected to the home page

3. **Create a post**
   - Click "Create Post" in the navbar
   - Fill in the title and content
   - Choose whether to publish immediately
   - Click "Create Post"

4. **Vote on posts**
   - Click the up arrow to upvote
   - Click the down arrow to remove your vote
   - Vote count is displayed in the center

5. **Edit/Delete your posts**
   - Go to "My Posts" to see all your posts
   - Click "Edit" to modify a post
   - Click "Delete" to remove a post

## Development

### Backend Development
- FastAPI automatically reloads on code changes with `--reload` flag
- Check API docs at `/docs` for testing endpoints
- Use Alembic for database migrations:
  ```bash
  # Create a new migration
  alembic revision --autogenerate -m "description"
  
  # Apply migrations
  alembic upgrade head
  ```

### Frontend Development
- Vite provides hot module replacement
- Components follow functional React patterns with hooks
- Tailwind CSS for styling
- Axios interceptors handle JWT authentication automatically

## Building for Production

### Backend
```bash
# Use gunicorn or uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
```
The build output will be in `frontend/dist/`

## Common Issues

1. **CORS errors**: Make sure the backend CORS configuration includes your frontend URL
2. **Database connection errors**: Check your `.env` file and ensure PostgreSQL is running
3. **Authentication issues**: Ensure the JWT secret key is consistent and tokens aren't expired

## Future Enhancements

- [ ] Profile pictures
- [ ] Comments on posts
- [ ] Categories/Tags
- [ ] Rich text editor
- [ ] Image uploads
- [ ] Email verification
- [ ] Password reset
- [ ] Social sharing

## License

MIT License
