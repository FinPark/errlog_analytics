/**
 * API service for Error Log Analytics
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// File upload
export async function uploadFiles(files: File[]) {
  const formData = new FormData()
  files.forEach((file) => {
    formData.append('files', file)
  })

  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })

  return response.data
}

// Log type detection
export async function detectLogTypes(filenames: string[]) {
  const response = await api.post('/api/analyze/detect-types', {
    filenames
  })
  return response.data
}

// Visual Objects analysis
export async function analyzeVisualObjectsLogs(filenames: string[]) {
  const response = await api.post('/api/analyze/visual-objects', {
    filenames
  })
  return response.data
}

// .NET analysis
export async function analyzeDotNetLogs(filenames: string[]) {
  const response = await api.post('/api/analyze/dotnet', {
    filenames
  })
  return response.data
}

// Get error summary
export async function getErrorSummary() {
  const response = await api.get('/api/errors/summary')
  return response.data
}

// Get error timeline
export async function getErrorTimeline() {
  const response = await api.get('/api/errors/timeline')
  return response.data
}

// Get critical errors
export async function getCriticalErrors() {
  const response = await api.get('/api/errors/critical')
  return response.data
}

// Get all errors with pagination
export async function getErrors(page = 1, limit = 100) {
  const response = await api.get(`/api/errors?page=${page}&limit=${limit}`)
  return response.data
}

// Get error types distribution
export async function getErrorTypes() {
  const response = await api.get('/api/errors/types')
  return response.data
}

// Get user activity data
export async function getUserActivity() {
  const response = await api.get('/api/errors/users')
  return response.data
}

export default api