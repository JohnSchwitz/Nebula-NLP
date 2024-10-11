<template>
    <div class="bg-[#F7C409] p-8 rounded-md max-w-lg mx-auto shadow-lg">
      <h1 class="text-lg font-bold text-center mb-4">
        Instructions to Save Your Story
      </h1>
      <p class="mt-4 mb-2">1. At the prompt above for Guest: enter 'Please Provide Complete Story'</p>
      <p class="mb-4">2. Enter Story Name</p>
      <input
        v-model="storyName"
        type="text"
        class="block w-full p-2 mb-4 border rounded shadow-sm"
        placeholder="Your Story Name here"
      />
      <button
        @click="uploadToDatabase"
        class="w-full bg-blue-600 text-white p-3 rounded mb-4 hover:bg-blue-700 transition"
      >
        Upload to Database
      </button>
      <p class="text-center mb-4">After Upload to Database</p>
      <button
        @click="downloadPdf"
        class="w-full bg-green-600 text-white p-3 rounded mb-4 hover:bg-green-700 transition"
      >
        Download a PDF
      </button>
      <div
        class="mt-4 p-4 border rounded overflow-y-auto shadow-inner bg-white text-gray-800"
        style="max-height: 400px; white-space: pre-wrap;"
      >
        {{ story }}
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default defineComponent({
    name: 'FormComponent',
    setup() {
      const userId = ref(1);
      const storyName = ref('');
      const story = ref('Princess Hazel lived in the Kingdom of the Dragons with her mother and father Queen Micky and King Jack. She had a big brother Prince Jackson and a baby brother Grayson. Hazel was 6 years old, Jackson was 8 and Grayson was 1. Hazel had a pony Bubbles and a faithful and ferocious creme colored cat Misty. She was startled from sleep one day by her parents crying that a young dragon had swooped in and carried off Grayson. Her parents were frozen with fear. Hazel told Jackson that it was up to them!');
  
      onMounted(() => {
        // Simulating fetching story from the page content
        const storyElement = document.querySelector('.mwai-reply.mwai-ai');
        if (storyElement) {
          story.value = storyElement.textContent || '';
        }
  
        // Simulate a WordPress function call
        // userId.value = 1; // Replace with actual method
      });
      console.log(userId.value);
      const uploadToDatabase = async () => {
        try {
          await axios.post('https://nebula-nlp.com/wp-json/form-submissions-api/v2/form-submission', {
            user_id: userId.value,
            story_name: storyName.value,
            story: story.value,
          });
          alert('Story uploaded.');
        } catch (error) {
          alert('Error uploading story.');
        }
      };
  
      const downloadPdf = async () => {
        try {
          await axios.post('https://nebula-nlp.com/wp-json/asyn-function-api/v2/pdf-download', {
            user_id: userId.value,
            story_name: storyName.value,
            story: story.value,
          });
          alert('PDF generation initiated.');
        } catch (error) {
          alert('Error downloading PDF.');
        }
      };
  
      //const getCurrentUserId = (): number => {
        // Implement this with a call or using WP-provided data
        //return 123; // Example/mock user ID
      //};
  
      return {
        userId,
        storyName,
        story,
        uploadToDatabase,
        downloadPdf,
      };
    },
  });
  </script>
  
  <style scoped>
  /* Any specific styles can go here */
  </style>