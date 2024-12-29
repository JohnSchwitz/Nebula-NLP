// CreateNarrative.vue
<template>
  <div class="max-w-4xl mx-auto px-4">
    <div class="mb-8">
      <h1 class="text-[36px] font-didot text-center mb-4 leading-[1.2]">
        Create a Narrative from Previous Stories
      </h1>
      <p class="text-2xl font-didot leading-[1.2] mb-6">
        The AI Agent will create a NARRATIVE from your previous STORIES. First, check the boxes of the stories you wish to include in the narrative. The AI will then create a NARRATIVE based on the characters, their names, the setting, and action or challenge using the selected STORIES. The AI agent will then add to the narrative providing new twists as it weaves the stories together. You may modify as many times as required.
      </p>
    </div>

    <div class="bg-white rounded-lg p-6 shadow-lg mb-6">
      <h2 class="text-2xl font-didot mb-4">Select Stories to Include:</h2>
      
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-4">
        Loading stories...
      </div>

      <!-- Stories list -->
      <div v-else-if="stories.length > 0">
        <ul class="space-y-3">
          <li v-for="story in stories" 
              :key="story.story_id" 
              class="flex items-center space-x-3">
            <input 
              type="checkbox" 
              :value="story.story_id" 
              v-model="selectedStoryIds"
              class="w-5 h-5"
            />
            <span class="text-xl font-didot">{{ story.story_name }}</span>
          </li>
        </ul>
      </div>

      <!-- No stories message -->
      <div v-else class="text-center py-4 text-gray-600">
        No stories available. Create some stories first!
      </div>
    </div>

    <button 
      v-if="stories.length > 0"
      @click="generateNarrative"
      class="bg-white text-black px-6 py-3 rounded font-bold text-lg hover:bg-gray-100 transition-colors font-didot mb-6"
    >
      Start Narrative
    </button>

    <div class="bg-chatbox-dark rounded-lg p-4 mb-6 min-h-[200px] max-h-[400px] overflow-y-auto">
      <div v-for="(message, index) in messages" 
           :key="index" 
           class="mb-3">
        <div class="bg-chatbox-light rounded p-3">
          <span v-if="message.sender === 'AI'" class="text-white font-bold">AI: </span>
          <span class="text-white font-didot">{{ message.text }}</span>
        </div>
      </div>
    </div>

    <div class="instruction-title text-[36px] font-didot text-center mb-4 leading-[1.2]">
      Instructions to Save Your Narrative and create a PDF
    </div>
    
    <div class="instructions-area text-2xl font-didot text-left leading-[1.2] mb-6">
      At the prompt below click the Complete Narrative BUTTON. You may then EDIT your narrative in the ScrollBox.
      <br/>
      Enter a Narrative Name, Upload to Database, and then download a PDF.
    </div>

    <div class="bottom-area flex gap-4 mb-6">
      <label for="narrativeName" class="font-didot">Narrative Name</label>
      <input 
        type="text" 
        v-model="narrativeName" 
        id="narrativeName" 
        placeholder="your narrative name here" 
        class="border rounded px-3 py-2 w-48 font-didot"
      />
      <button class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot">
        Upload to Database
      </button>
      <button class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot">
        Download PDF
      </button>
    </div>

    <div class="text-center font-bold mb-2 font-didot">ScrollBox</div>
    <textarea 
      v-model="narrativeContent" 
      readonly 
      class="w-full min-h-[300px] border rounded p-4 resize-y mb-8 font-didot"
    ></textarea>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateNarrative',
  data() {
    return {
      stories: [],
      narrativeContent: "",
      narrativeName: "Narrative Title",
      selectedStoryIds: [],
      messages: [],
      user_id: 1,
      loading: true
    }
  },
  async mounted() {
    axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL
    await this.fetchStories()
  },
  methods: {
    async fetchStories() {
      try {
        this.loading = true
        const response = await axios.get('/get_stories', { 
          params: { user_id: this.user_id } 
        })
        this.stories = response.data || []
      } catch (error) {
        console.error("Error fetching stories:", error)
        this.stories = []
      } finally {
        this.loading = false
      }
    },
    async generateNarrative() {
      try {
        this.messages.push({sender: 'StoryTeller', text: "Starting Narrative Generation..."})
        const response = await axios.post('/create_narrative', {
          user_id: this.user_id,
          story_ids: this.selectedStoryIds
        })
        this.messages.push({sender: 'AI', text: response.data.story})
        this.narrativeContent = response.data.story
      } catch (error) {
        console.error("Error generating narrative:", error)
      }
    },
    async saveNarrative() {
      // Implement save logic
    },
    downloadPDF() {
      // Implement PDF download logic
    }
  }
}
</script>
