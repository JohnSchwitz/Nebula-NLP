import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // Or your Cloud Run service URL
});

export default {
  startStoryCreation() {
    return apiClient.post('/startStoryCreation').then(res => res.data.conversationId); // Return conversationId
  },

  generateNarrative(prompt, conversationId) {  // Add conversationId parameter
    return apiClient.post('/generateNarrative', { prompt, conversationId }).catch(handleError);
  },
  
  getStories() {
    return apiClient.get('/getStories').catch(handleError);
  },

  createStory(storyData) {
    return apiClient.post('/createStory', storyData).catch(handleError);
  },

  generateNarrative(prompt) {
    return apiClient.post('/generateNarrative', { prompt }).catch(handleError);
  },



  handleError(error) {
    console.error("API Error:", error);
    // TODO:  Display more user-friendly error messages
    // Example:  if (error.response) { alert(error.response.data.error); }
    throw error; // Re-throw to be handled by the calling component
  }
};