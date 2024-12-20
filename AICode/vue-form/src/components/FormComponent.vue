<template>
  <div class="bg-[#F7C409] min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-md max-w-lg w-full mx-4 shadow-lg">
      <h2 class="text-base font-semibold text-center mb-4">
        Instructions to Save Your Story
      </h2>
      <p class="mt-4 mb-2 text-left">
        1. At the prompt above for StoryTeller input: enter 'Please Provide the Complete Story'<br>Please ensure that your Complete Story is displayed in the ScrollBox below<br>You may EDIT your story in the ScrollBox
      </p>
      <p class="mb-4 text-left">2. Enter Story Name and Upload to Database<br>This permits you to retriew all your Stories as a pdf</p>
      <input
        v-model="storyName"
        type="text"
        class="block w-full p-2 mb-4 border rounded shadow-sm"
        placeholder="Your Story Name here"
        required
        :disabled="isSubmitted"
      />
      <button
        :disabled="isSubmitting || isSubmitted"
        @click="handleFormSubmission"
        :class="{
          'bg-blue-600 hover:bg-blue-700': !isSubmitting && !isSubmitted,
          'bg-gray-400 cursor-not-allowed': isSubmitting || isSubmitted
        }"
        class="w-full text-white p-3 rounded mb-4 transition"
      >
        Upload to Database
      </button>
      <div class="flex justify-center items-center mb-4">
        <button
          @click="refreshStory"
          class="bg-blue-500 text-white p-2 rounded"
        >
          Refresh Story
        </button>
        <span class="text-xl font-semibold ml-4">ScrollBox</span>
      </div>
      <textarea
        class="block w-full p-4 border rounded overflow-y-auto shadow-inner bg-white text-gray-800 resize-none"
        style="min-width: 100%; min-height: 15rem;"
        v-model="story"
        :disabled="isSubmitted"
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
const story = ref('');  // Initialize to an empty string
const isSubmitting = ref(false);
const isSubmitted = ref(false);

// Function to update story from the DOM
const updateStory = () => {
  const storyElement = document.querySelector('.mwai-reply.mwai-ai:last-child');
  if (storyElement) {
    story.value = storyElement.textContent.trim();
    console.log('Story Element Updated:', story.value);

    // Enable the storyName field and submit button when a new story is detected
    if (story.value) {
      isSubmitted.value = false; // Reset submitted state after detecting new story
    }
  }
};

onMounted(() => {
  // Check for user ID in data attributes, handle scenario where userId might be present
  const element = document.getElementById('vue-form');
  if (element && element.dataset.userId) {
    userId.value = parseInt(element.dataset.userId, 10);
    console.log('User ID set to:', userId.value);
  } else {
    console.error('User ID attribute not set or not a number');
  }

  // Observe body for changes and update story
  const observer = new MutationObserver(updateStory);
  observer.observe(document.body, { childList: true, subtree: true });

  // Initial update
  updateStory();
});

// Handle form submission
const handleFormSubmission = async () => {
  if (isSubmitting.value || isSubmitted.value) return;

  if (!storyName.value.trim()) {
    alert('Please enter a story name.');
    return;
  }

  if (!story.value.trim()) {
    alert('Please ensure the story is displayed in the ScrollBox.');
    return;
  }

  await uploadToDatabase();
};

// Refresh Story action
const refreshStory = () => {
  updateStory();
};

// Handle uploading to database
const uploadToDatabase = async () => {
  isSubmitting.value = true;
  try {
    await axios.post('https://nebula-nlp.com/wp-json/form-submissions-api/v2/form-submission', {
      user_id: userId.value,
      story_name: storyName.value,
      story: story.value,
    });
    alert('Story uploaded successfully.');
    isSubmitted.value = true; // Only allow submit once
  } catch (error) {
    console.error('Upload error:', error);
    alert('Error uploading story. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* No additional styles needed with Tailwind CSS */
</style>



