<template>
  <div class="bg-[#F7C409] min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-md max-w-lg w-full mx-4 shadow-lg">
      <h2 class="text-base font-semibold text-center mb-4">
        Instructions to Save Your Story
      </h2>
      <p class="mt-4 mb-2 text-left">
        1. At the prompt above for StoryTeller input: enter 'Please Provide the Complete Story'<br>Please ensure that your Complete Story is displayed in the ScrollBox below.
      </p>
      <p class="mb-4 text-left">2. Enter Story Name</p>
      <input
        v-model="storyName"
        type="text"
        class="block w-full p-2 mb-4 border rounded shadow-sm"
        placeholder="Your Story Name here"
      />
      <button
        :disabled="isSubmitting"
        @click="uploadToDatabase"
        :class="{
          'bg-blue-600 hover:bg-blue-700': !isSubmitting,
          'bg-gray-400 cursor-not-allowed': isSubmitting
        }"
        class="w-full text-white p-3 rounded mb-4 transition"
      >
        Upload to Database
      </button>
      <p class="text-center mb-4">ScrollBox with your Story<br>You may edit the Story</p>
      <div class="mb-4"></div>
      <textarea
        class="block w-full p-4 border rounded overflow-y-auto shadow-inner bg-white text-gray-800 resize-none"
        style="min-width: 100%; min-height: 15rem;"
        :value="story"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Reactive variables
const userId = ref(1);
const storyName = ref('');
const story = ref('Princess Hazel lived in the Kingdom of the Dragons with her mother and father Queen Micky and King Jack. She had a big brother Prince Jackson and a baby brother Grayson. Hazel was 6 years old, Jackson was 8 and Grayson was 1. Hazel had a pony Bubbles and a faithful and ferocious creme colored cat Misty. She was startled from sleep one day by her parents crying that a young dragon had swooped in and carried off Grayson. Her parents were frozen with fear. Hazel told Jackson that it was up to them!');
const isSubmitting = ref(false);

onMounted(() => {
  setTimeout(() => {
  console.log('onMounted executed');
  const element = document.getElementById('vue-form');
  if (element && element.dataset.userId) {
    userId.value = parseInt(element.dataset.userId, 10);
    console.log('User ID set to:', userId.value);
  } else {
    console.error('User ID attribute not set or not a number');
  }

  const storyElement = document.querySelector('.mwai-reply.mwai-ai:last-child');
  console.log('Story Element:', storyElement);
  if (storyElement) {
    story.value = storyElement.textContent;
    console.log('Story Element Found:', story.value);
  } else {
    console.error('Story Element not found.');
  }
  }, 500); // Adjust delay as needed
});

const uploadToDatabase = async () => {
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  try {
    await axios.post('https://nebula-nlp.com/wp-json/form-submissions-api/v2/form-submission', {
      user_id: userId.value,
      story_name: storyName.value,
      story: story.value,
    });
    alert('Story uploaded.');
  } catch (error) {
    console.error('Upload error:', error);
    alert('Error uploading story.');
  } finally {
    isSubmitting.value = false;
  }
};

// user_id is NOT NEEDED pdf is GENERATED FROM story_name & story
const downloadPdf = async () => {
  try {
    await axios.post('https://nebula-nlp.com/wp-json/asyn-function-api/v2/pdf-download', {
      story_name: storyName.value,
      story: story.value,
    });
    alert('PDF generation initiated.');
  } catch (error) {
    console.error('Error downloading PDF:', error);
    alert('Error downloading PDF.');
  }
};
</script>

<style scoped>
/* No additional styles needed with Tailwind CSS */
</style>

