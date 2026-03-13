import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
})

export const uploadFile = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const fetchUpload = (id) => api.get(`/upload/${id}`)
export const convertUpload = (id) => api.post(`/convert/${id}`)
export const fetchFhir = (id) => api.get(`/fhir/${id}`)

export const fetchHistory = () => api.get('/uploads')
