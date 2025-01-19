// src/services/api.ts
import axios from 'axios'

const api = {
  async generateStory(prompt: string) {
    try {
      const response = await axios.post('/create_story', {
        prompt,
        max_tokens: 2048,
        temperature: 0.8
      })
      return response.data.story
    } catch (error) {
      throw new Error('Failed to generate story. Please try again.')
    }
  },

  async completeStory(storyContent: string) {
    try {
      const response = await axios.post('/complete_story', {
        story_content: storyContent,
        max_tokens: 1024,
        temperature: 0.7
      })
      return response.data.story
    } catch (error) {
      throw new Error('Failed to complete story')
    }
  },

  async generateNarrative(selectedStories: any[]) {
    try {
      const response = await axios.post('/generate_narrative', {
        stories: selectedStories,
        max_tokens: 2048,
        temperature: 0.8
      })
      return response.data.narrative
    } catch (error) {
      throw new Error('Gemini API error')
    }
  },

  async saveStory(userId: number, storyName: string, storyContent: string) {
    try {
      const response = await axios.post('/save_story', {
        user_id: userId,
        story_name: storyName,
        story_content: storyContent
      })
      return response.data.story_id
    } catch (error) {
      throw new Error('Failed to save story')
    }
  }
}

export default api