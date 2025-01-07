// src/services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})

export const generateStory = async (prompt: string) => {
  const response = await api.post('/generate_story', { prompt })
  return response.data
}

export const completeStory = async (content: string) => {
  const response = await api.post('/complete_story', { content })
  return response.data
}

export default {
  generateStory,
  completeStory
}