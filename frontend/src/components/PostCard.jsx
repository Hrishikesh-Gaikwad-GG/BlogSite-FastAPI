import { Link } from 'react-router-dom'
import { useState } from 'react'
import { voteAPI } from '../services/api'

function PostCard({ post, onVoteUpdate, showActions = false, onDelete }) {
  const [voting, setVoting] = useState(false)
  const [currentVotes, setCurrentVotes] = useState(post.votes || 0)

  const handleVote = async (direction) => {
    if (voting) return
    setVoting(true)
    try {
      await voteAPI.vote(post.Post.id, direction)
      if (direction === 1) {
        setCurrentVotes(prev => prev + 1)
      } else {
        setCurrentVotes(prev => prev - 1)
      }
      if (onVoteUpdate) {
        onVoteUpdate()
      }
    } catch (error) {
      console.error('Error voting:', error)
      alert(error.response?.data?.detail || 'Failed to vote')
    } finally {
      setVoting(false)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const postData = post.Post || post

  return (
    <div className="card">
      <div className="flex gap-4">
        <div className="flex flex-col items-center space-y-2">
          <button
            onClick={() => handleVote(1)}
            disabled={voting}
            className="text-gray-400 hover:text-green-500 transition-colors disabled:opacity-50"
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
            </svg>
          </button>
          <span className="font-bold text-lg">{currentVotes}</span>
          <button
            onClick={() => handleVote(0)}
            disabled={voting}
            className="text-gray-400 hover:text-red-500 transition-colors disabled:opacity-50"
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        <div className="flex-1">
          <Link to={`/post/${postData.id}`}>
            <h2 className="text-2xl font-bold text-gray-900 hover:text-primary transition-colors mb-2">
              {postData.title}
            </h2>
          </Link>
          
          <p className="text-gray-600 mb-4 line-clamp-3">
            {postData.content}
          </p>
          
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-4">
              <span>By {postData.owner?.email || 'Unknown'}</span>
              <span>•</span>
              <span>{formatDate(postData.created_at)}</span>
              {postData.published !== undefined && (
                <>
                  <span>•</span>
                  <span className={postData.published ? 'text-green-600' : 'text-yellow-600'}>
                    {postData.published ? 'Published' : 'Draft'}
                  </span>
                </>
              )}
            </div>

            {showActions && (
              <div className="flex space-x-2">
                <Link
                  to={`/edit/${postData.id}`}
                  className="text-blue-600 hover:text-blue-800"
                >
                  Edit
                </Link>
                <button
                  onClick={() => onDelete && onDelete(postData.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  Delete
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PostCard
