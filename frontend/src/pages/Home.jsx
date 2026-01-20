import { useState, useEffect } from 'react'
import { postsAPI } from '../services/api'
import PostCard from '../components/PostCard'

function Home({ isAuthenticated }) {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  const fetchPosts = async () => {
    try {
      setLoading(true)
      const data = await postsAPI.getPosts(searchTerm)
      setPosts(data)
    } catch (error) {
      console.error('Error fetching posts:', error)
      if (error.response?.status === 401) {
        // Not authenticated, but that's okay for viewing posts
        setPosts([])
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (isAuthenticated) {
      fetchPosts()
    } else {
      setLoading(false)
    }
  }, [searchTerm, isAuthenticated])

  const handleSearch = (e) => {
    e.preventDefault()
    setSearchTerm(search)
  }

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">Welcome to BlogSite</h1>
        <p className="text-xl text-gray-600 mb-8">
          Share your thoughts and stories with the world
        </p>
        <div className="space-x-4">
          <a href="/login" className="btn-primary inline-block">
            Login
          </a>
          <a href="/register" className="btn-secondary inline-block">
            Register
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">Latest Posts</h1>
        
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            placeholder="Search posts..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field flex-1"
          />
          <button type="submit" className="btn-primary">
            Search
          </button>
          {searchTerm && (
            <button
              type="button"
              onClick={() => {
                setSearch('')
                setSearchTerm('')
              }}
              className="btn-secondary"
            >
              Clear
            </button>
          )}
        </form>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      ) : posts.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">No posts found</p>
        </div>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => (
            <PostCard key={post.Post.id} post={post} onVoteUpdate={fetchPosts} />
          ))}
        </div>
      )}
    </div>
  )
}

export default Home
