import { Link } from 'react-router-dom'

function Navbar({ isAuthenticated, user, onLogout }) {
  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-2xl font-bold text-primary">
              BlogSite
            </Link>
            <div className="hidden md:flex space-x-4">
              <Link to="/" className="text-gray-700 hover:text-primary transition-colors">
                Home
              </Link>
              {isAuthenticated && (
                <>
                  <Link to="/my-posts" className="text-gray-700 hover:text-primary transition-colors">
                    My Posts
                  </Link>
                  <Link to="/create" className="text-gray-700 hover:text-primary transition-colors">
                    Create Post
                  </Link>
                </>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-gray-700 hidden sm:inline">
                  {user?.email}
                </span>
                <button
                  onClick={onLogout}
                  className="btn-secondary"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-secondary">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
