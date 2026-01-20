import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { postsAPI } from '../services/api'
import PostCard from '../components/PostCard'

function MyPosts({ user }) {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMyPosts()
  }, [])

  const fetchMyPosts = async () => {
    try {
      setLoading(true)
      const data = await postsAPI.getMyPosts()
      // Transform the data to match PostCard expectations
      const transformedData = data.map(post => ({
        Post: post,
        votes: 0 // We don't have vote counts for my posts endpoint
      }))
      setPosts(transformedData)
    } catch (error) {
      console.error('Error fetching posts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return
    }

    try {
      await postsAPI.deletePost(id)
      setPosts(posts.filter(post => post.Post.id !== id))
    } catch (error) {
      alert('Failed to delete post')
    }
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900">My Posts</h1>
        <Link to="/create" className="btn-primary">
          Create New Post
        </Link>
      </div>

      {posts.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl shadow-sm">
          <p className="text-gray-600 text-lg mb-4">You haven't created any posts yet</p>
          <Link to="/create" className="btn-primary inline-block">
            Create Your First Post
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => (
            <PostCard 
              key={post.Post.id} 
              post={post} 
              showActions={true}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default MyPosts
