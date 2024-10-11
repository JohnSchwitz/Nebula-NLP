<template>
  <div class="bg-[#F7C409] min-h-screen flex items-center justify-center p-4">
    <form class="bg-white p-6 rounded shadow-md w-full max-w-lg">
      <h2 class="text-2xl font-bold mb-4">Instructions to Save Your Story</h2>

      <!-- Instructions -->
      <div class="mb-4 text-sm text-gray-700">
        <p>1) At prompt Guest: enter 'Please display full story'</p>
        <p>2) Enter a Story Name</p>
        <div class="h-4"></div>

        <!-- Story Name Field -->
        <label for="story_name" class="block text-sm font-medium text-gray-700 mb-2">Story Name</label>
        <input
          type="text"
          v-model="formData.story_name"
          id="story_name"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50 focus:ring-yellow-500 mb-2"
          required
        />

        <hr class="my-4" />

        <!-- Story Field -->
        <label for="story" class="block text-sm font-medium text-gray-700 mb-2">Story</label>
        <textarea
          v-model="formData.story"
          id="story"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50 focus:ring-yellow-500 mb-4"
          required
          readonly
          style="height: 40em; overflow-y: auto;" <!-- Adjust height and set overflow behavior -->
        ></textarea>

        <!-- Upload Button -->
        <button type="button" @click="uploadToDatabase" class="w-full bg-blue-500 text-white py-2 px-4 rounded-md shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-700 mt-4">
          Upload to Database
        </button>

        <div class="h-4"></div>

        <!-- After Upload Message -->
        <div class="mb-4 text-sm text-gray-700">
          <p>After Upload to Database</p>
        </div>

        <div class="h-4"></div>

        <!-- Download PDF Button -->
        <button type="button" @click="downloadPDF" class="w-full bg-yellow-500 text-white py-2 px-4 rounded-md shadow hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-700 mt-4">
          Download a PDF
        </button>

        <!-- Feedback Message -->
        <div v-if="message" :class="`mt-4 p-2 text-sm rounded-md ${success ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`">
          {{ message }}
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

// Safely access window.storyFormData with defaults
const storyFormData = (window as any)?.storyFormData || {};

// Initialize formData with defaults using optional chaining
const formData = ref({
  user_id: storyFormData.userID ?? 0,  // Use nullish coalescing operator to provide default
  story_name: '',
  story: storyFormData.story ?? '',    // Default to an empty string
});

const message = ref('');
const success = ref(false);

async function uploadToDatabase() {
  try {
    await axios.post('https://nebula-nlp.com/wp-json/form-submissions-api/v2/form-submission', formData.value, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    message.value = 'Story uploaded successfully!';
    success.value = true;
  } catch (error) {
    console.error('Error uploading story:', error);
    message.value = 'There was an error uploading the story.';
    success.value = false;
  }
}

async function downloadPDF() {
  try {
    const pdfResponse = await axios.post('https://nebula-nlp.com/wp-json/asyn-function-api/v2/pdf-download', formData.value, {
      headers: {
        'Content-Type': 'application/json',
      },
      responseType: 'blob',
    });

    const url = URL.createObjectURL(new Blob([pdfResponse.data], { type: 'application/pdf' }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'story.pdf');
    document.body.appendChild(link);
    link.click();
    link.remove();

    message.value = 'PDF downloaded successfully!';
    success.value = true;
  } catch (error) {
    console.error('Error downloading PDF:', error);
    message.value = 'There was an error downloading the PDF.';
    success.value = false;
  }
}
</script>

<style scoped>
.success {
  color: green;
}
.error {
  color: red;
}
</style>