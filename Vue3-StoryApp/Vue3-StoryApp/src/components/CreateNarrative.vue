// CreateNarrative.vue 
<template>
    <div>
      <h1>Create a Narrative</h1>
      <ul>
        <li v-for="story in stories" :key="story.story_id">
          {{ story.story_name }}
          <button @click="deleteStory(story.story_id)">Delete</button>
        </li>
      </ul>
      <button @click="generateNarrative">Generate Narrative</button>
      <textarea v-model="narrativeContent" readonly></textarea>
      <button @click="saveNarrative">Save Narrative</button>
      <button @click="downloadPDF">Download PDF</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        stories: [],
        narrativeContent: "",
        selectedStoryIds: [], // To keep track of selected stories
        user_id: 1, // Replace with actual user ID
      };
    },
    mounted() {
      this.fetchStories();
    },
    methods: {
      async fetchStories() {
        try {
          const response = await axios.get('/get_stories', { params: { user_id: this.user_id } });
          this.stories = response.data;
        } catch (error) {
          console.error("Error fetching stories:", error);
        }
      },
      deleteStory(storyId) {
        // Send DELETE request to backend to delete the story
      },
      async generateNarrative() {
         try {
              const response = await axios.post('/create_narrative', {
                  user_id: this.user_id,
                  story_ids: this.selectedStoryIds
              });
              // Handle response, update narrativeContent
          } catch (error) {
              console.error("Error generating narrative:", error);
          }
      },
      async saveNarrative() {
        // Send narrativeContent to backend for database saving.
      },
      downloadPDF() {
        // Send request to backend to generate and download PDF.
      }
    },
  };
  </script>