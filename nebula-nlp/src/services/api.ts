import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = {
  async generateStory(prompt: string): Promise<string> {
    try {
      const response = await axios.post(`${API_URL}/create_story`, { prompt })
      return response.data.story
    } catch (error) {
      throw new Error('Failed to generate story. Please try again.')
    }
  },

  async completeStory(content: string): Promise<string> {
    try {
      const response = await axios.post(`${API_URL}/complete_story`, { content })
      return response.data.story
    } catch (error) {
      throw new Error('Failed to complete story')
    }
  }
}

export default api