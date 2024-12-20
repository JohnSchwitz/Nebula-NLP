// CreateStory.vue
<template>
    <div>
      <h1>Create a Story</h1>
      <textarea v-model="storyPrompt" placeholder="Enter initial prompt"></textarea>
      <button @click="generateStory">Generate Story</button>
      <textarea v-model="storyContent" readonly></textarea>
      <button @click="saveStory">Save Story</button>
      <button @click="downloadPDF">Download PDF</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        storyPrompt: "",
        storyContent: "",
        user_id: 1, // Replace with actual user ID retrieval method.
      };
    },
    methods: {
      async generateStory() {
        try {
            const response = await axios.post('/create_story', {
                user_id: this.user_id,
                initial_prompt: this.storyPrompt
            });
            //Handle response and update storyContent
        } catch (error) {
            console.error("Error generating story:", error);
        }
      },
      async saveStory() {
        // Send storyContent to backend for database saving.
      },
      downloadPDF() {
        // Send request to backend to generate and download PDF.
      },
    },
  };
  </script>