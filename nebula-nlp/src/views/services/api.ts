// src/services/api.ts
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

const handleError = (error) => {
  console.error('API Error:', error)
  throw error
}

export default {
  generateStory(prompt) {
    return apiClient.post('/generateStory', { prompt }).catch(handleError)
  },
  
  generateNarrative(prompt) {
    return apiClient.post('/generateNarrative', { prompt }).catch(handleError)
  },
  
  completeStory(content) {
    return apiClient.post('/completeStory', { content }).catch(handleError)
  }
}