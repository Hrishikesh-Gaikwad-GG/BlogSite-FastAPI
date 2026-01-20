import axios from 'axios'

const API_URL = '/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  login: async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    const response = await api.post('/token', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
  
  register: async (email, password) => {
    const response = await api.post('/users/', { email, password })
    return response.data
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/users/me')
    return response.data
  },
}

export const postsAPI = {
  getPosts: async (search = '', limit = 10, offset = 0) => {
    const response = await api.get('/posts/', {
      params: { search, limit, offset },
    })
    return response.data
  },
  
  getPost: async (id) => {
    const response = await api.get(`/posts/${id}`)
    return response.data
  },
  
  createPost: async (postData) => {
    const response = await api.post('/posts/', postData)
    return response.data
  },
  
  updatePost: async (id, postData) => {
    const response = await api.patch(`/posts/${id}`, postData)
    return response.data
  },
  
  deletePost: async (id) => {
    const response = await api.delete(`/posts/${id}`)
    return response.data
  },
  
  getMyPosts: async (limit = 10, offset = 0) => {
    const response = await api.get('/posts/me', {
      params: { limit, offset },
    })
    return response.data
  },
}

export const voteAPI = {
  vote: async (post_id, dir) => {
    const response = await api.post('/vote/', { post_id, dir })
    return response.data
  },
}

export default api
