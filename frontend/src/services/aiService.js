import { api } from './api'

export const generateAISummary = (bundle) => api.post('/api/generate-summary', { bundle })
