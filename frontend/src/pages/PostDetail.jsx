import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { postsAPI, voteAPI } from '../services/api'

function PostDetail({ isAuthenticated, user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [voting, setVoting] = useState(false)

  useEffect(() => {
    fetchPost()
  }, [id])

  const fetchPost = async () => {
    try {
      setLoading(true)
      const data = await postsAPI.getPost(id)
      if (data && data.length > 0) {
        setPost(data[0])
      }
    } catch (error) {
      setError('Failed to load post')
      console.error('Error fetching post:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleVote = async (direction) => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    
    if (voting) return
    setVoting(true)
    
    try {
      await voteAPI.vote(post.Post.id, direction)
      fetchPost()
    } catch (error) {
      console.error('Error voting:', error)
      alert(error.response?.data?.detail || 'Failed to vote')
    } finally {
      setVoting(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return
    }

    try {
      await postsAPI.deletePost(id)
      navigate('/')
    } catch (error) {
      alert('Failed to delete post')
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (error || !post) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 text-center">
        <p className="text-red-600 text-lg">{error || 'Post not found'}</p>
        <Link to="/" className="text-primary hover:underline mt-4 inline-block">
          Back to Home
        </Link>
      </div>
    )
  }

  const postData = post.Post
  const isOwner = user && postData.owner_id === user.id

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <Link to="/" className="text-primary hover:underline mb-6 inline-block">
        ← Back to Posts
      </Link>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex gap-6">
          {/* Vote Section */}
          <div className="flex flex-col items-center space-y-2">
            <button
              onClick={() => handleVote(1)}
              disabled={voting || !isAuthenticated}
              className="text-gray-400 hover:text-green-500 transition-colors disabled:opacity-50"
              title={!isAuthenticated ? 'Login to vote' : ''}
            >
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
            </button>
            <span className="font-bold text-2xl">{post.votes || 0}</span>
            <button
              onClick={() => handleVote(0)}
              disabled={voting || !isAuthenticated}
              className="text-gray-400 hover:text-red-500 transition-colors disabled:opacity-50"
              title={!isAuthenticated ? 'Login to vote' : ''}
            >
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>

          {/* Content Section */}
          <div className="flex-1">
            <div className="flex justify-between items-start mb-4">
              <h1 className="text-4xl font-bold text-gray-900">{postData.title}</h1>
              {isOwner && (
                <div className="flex space-x-2">
                  <Link
                    to={`/edit/${postData.id}`}
                    className="btn-secondary text-sm"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={handleDelete}
                    className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors text-sm"
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-center space-x-4 text-sm text-gray-500 mb-6">
              <span>By {postData.owner?.email || 'Unknown'}</span>
              <span>•</span>
              <span>{formatDate(postData.created_at)}</span>
              <span>•</span>
              <span className={postData.published ? 'text-green-600' : 'text-yellow-600'}>
                {postData.published ? 'Published' : 'Draft'}
              </span>
            </div>

            <div className="prose max-w-none">
              <p className="text-gray-700 text-lg whitespace-pre-wrap leading-relaxed">
                {postData.content}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PostDetail
