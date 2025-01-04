// CreateNarrative.vue
<template>
  <input v-model="prompt" placeholder="Enter your prompt">
  <button @click="generateText">Generate Narrative</button>
  <div v-if="story">
      {{ story }}
  </div>
  <div class="max-w-4xl mx-auto px-4">
    <div class="mb-8">
      <p class="text-lg font-didot leading-[1.2]">
        The AI Agent will create a NARRATIVE from your previous STORIES. 
        First, check the boxes of the stories you wish to include and click Start Narrative.
        These stories are placed in the ScrollBox permitting you to edit them. 
        After editing enter your contribution to the narrative in StoryTeller input. 
        The AI agent will then add to the narrative providing new twists as it weaves the stories together. 
        You may modify as many times as required and edit the result.
      </p>
    </div>

    <h2 class="text-2xl font-didot mb-4">Select Stories to Include</h2>

    <div class="bg-white rounded-lg p-6 shadow-lg mb-6">
      <div class="flex mb-4 font-didot font-bold">
        <div class="w-1/3">
          Story Name
        </div>
        <div class="w-2/3">
          Story
        </div>
      </div>

      <div class="space-y-4">
        <div class="flex items-start border-b pb-2">
          <div class="w-1/3 flex items-center">
            <input 
              type="checkbox" 
              value="1" 
              v-model="selectedStoryIds"
              class="mr-2 w-4 h-4"
            />
            <span class="font-didot">The Lost Expedition</span>
          </div>
          <div class="w-2/3 font-didot text-sm">
            Professor Amelia Thorne, a paleontologist with a fiery spirit and a penchant for the unorthodox, had scoffed at the notion of a living Pterodactylus...
          </div>
        </div>
        <div class="flex items-start border-b pb-2">
          <div class="w-1/3 flex items-center">
            <input 
              type="checkbox" 
              value="2" 
              v-model="selectedStoryIds"
              class="mr-2 w-4 h-4"
            />
            <span class="font-didot">Fearless Princess Hazel</span>
          </div>
          <div class="w-2/3 font-didot text-sm">
            Princess Hazel peered out the window of her bedroom in the palace, watching as dusk fell over the Kingdom of the Dragons...
          </div>
        </div>
      </div>
    </div>
    
    <div class="my-8">
      <h2 class="text-2xl font-bold font-didot text-center mb-4 leading-[1.2]">
        Instructions to Save Your Narrative and create a PDF
      </h2>
      <p class="text-lg font-didot text-left leading-[1.2]">
        1) At the prompt below click the Create Narrative BUTTON. You may then EDIT your narrative in the ScrollBox.
      </p>
      <p class="text-lg font-didot text-left leading-[1.2]">
        2) Enter a Narrative Name, Upload to Database, and then download a PDF.
      </p>
    </div>

    <div class="flex flex-wrap items-center gap-4 my-2">
      <label for="narrativeName" class="font-didot">Narrative Name</label>
      <input 
        type="text" 
        v-model="narrativeName" 
        id="narrativeName" 
        placeholder="your narrative name here" 
        class="border rounded px-3 py-2 w-48 font-didot"
      />
<!-- Upload to Database button -->
<button 
  @click="uploadToDatabase"
  :disabled="!isCompleted || !narrativeName.trim() || narrativeName === 'Narrative Title'"
  class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
>
  Upload to Database
</button>

<!-- Download PDF button -->
<button 
  @click="downloadPDF"
  :disabled="!isCompleted"
  class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
>
  Download PDF
</button>

<div class="flex flex-wrap items-center justify-between gap-4 mb-0 w-full">
  <p class="text-lg font-didot font-bold text-left leading-[1.2]">
    AI StoryCreator:
  </p>
  <!-- Start and Create Narrative button -->
  <button 
    @click="startNarrative"
    :disabled="!narrativeContent.trim()"
    class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
  >
    Start Narrative
  </button>
  <button 
    @click="createNarrative"
    :disabled="!narrativeContent.trim()"
    class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
  >
    Create Narrative
  </button>
        <div class="flex-grow text-center">
          <p class="text-xl font-didot font-bold">ScrollBox</p>
        </div>
        <div class="w-[140px]"></div>
</div>
</div> 

    <div class="bg-chatbox-light rounded-lg p-4 mb-4 min-h-[200px] max-h-[400px] overflow-y-auto">
      <div v-if="!isEditable" v-for="(message, index) in messages" 
          :key="index" 
          class="mb-3">
        <div :class="message.sender === 'AI' ? 'bg-white' : 'bg-white'" 
            class="rounded p-3 relative">
          <span class="text-black block" 
                :class="message.sender === 'AI' ? 'ml-0' : ''">
            {{ message.text }}
          </span>
        </div>
      </div>
      <textarea 
        v-if="isEditable"
        v-model="storyContent"
        class="w-full h-full bg-white text-black p-3 rounded resize-none"
      ></textarea>
    </div>

    <div class="bg-chatbox-light rounded-lg p-4 flex gap-4 items-start">
      <textarea 
        v-model="narrativeInput" 
        placeholder="StoryTeller input:"
        rows="2"
        class="flex-1 bg-white placeholder-black resize-y p-2 focus:outline-none"
      ></textarea>
      <button 
        @click="sendNarrativeInput"
        :disabled="!narrativeInput.trim() || loading"
        class="bg-white text-black px-6 py-2 rounded font-bold text-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Send
      </button>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      <span class="block sm:inline">{{ error }}</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import api from './api'
import { ref, onMounted } from 'vue'

const story = ref("")
const prompt = ref("")
const conversationId = ref(null)

onMounted(async () => {  // Get a new conversation ID when the component mounts
  conversationId.value = await api.startStoryCreation()
})

async function generateText(){
    try {
        story.value = await api.generateNarrative(prompt.value, conversationId.value)

    } catch (error) {
        console.error(error)

    }
}

export default {
  name: 'CreateNarrative',
  data() {
    return {
      stories: [
        {
          story_id: 1,
          story_name: "The Lost Expedition",
          story_content: "Professor Amelia Thorne, a paleontologist with a fiery spirit and a penchant for the unorthodox, had scoffed at the notion of a living Pterodactylus..."
        },
        {
          story_id: 2,
          story_name: "Fearless Princess Hazel",
          story_content: "Princess Hazel peered out the window of her bedroom in the palace, watching as dusk fell over the Kingdom of the Dragons..."
        }
      ],
      narrativeContent: "",
      narrativeName: "Narrative Title",
      selectedStoryIds: [],
      selectedStories: [], // To store full story details for PDF
      messages: [],
      narrativeInput: "",
      loading: false,
      error: "",
      user_id: 1,
      isEditable: false,
      isCompleted: false,      
      narrativePrompt: `Creating a narrative from selected stories. The AI will weave together the characters, settings, and plots into a cohesive narrative with new twists and connections. You may modify the narrative as needed.`
    }
  },
  mounted() {
    axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL
    this.messages.push({ sender: 'AI', text: this.narrativePrompt })
  },
  methods: {
    async generateNarrative() {
  if (this.selectedStoryIds.length === 0) {
    this.error = "Please select at least one story"
    return
  }

  this.error = ""
  this.loading = true
  try {
    this.selectedStories = this.stories.filter(story => 
      this.selectedStoryIds.includes(story.story_id)
    )
    
    // Combine selected stories into editable content
    this.narrativeContent = this.selectedStories
      .map(story => story.story_content)
      .join('\n\n')
    
    this.isEditable = true  // Make content editable immediately
  } catch (error) {
    this.error = "Failed to start narrative. Please try again."
    console.error("Error starting narrative:", error)
  } finally {
    this.loading = false
  }
},

    async sendNarrativeInput() {
      if (!this.narrativeInput.trim()) return

      this.error = ""
      this.loading = true
      try {
        this.messages.push({ sender: 'StoryTeller', text: this.narrativeInput })
        const response = await axios.post('/update_narrative', {
          user_id: this.user_id,
          narrative_input: this.narrativeInput,
          current_narrative: this.narrativeContent,
          selected_stories: this.selectedStories // Include source stories
        })
        this.messages.push({ sender: 'AI', text: response.data.narrative })
        this.narrativeContent = response.data.narrative
        this.narrativeInput = ""
      } catch (error) {
        this.error = "Failed to update narrative. Please try again."
        console.error("Error updating narrative:", error)
      } finally {
        this.loading = false
      }
    },

    async uploadToDatabase() {
      if (!this.narrativeName.trim() || !this.narrativeContent.trim()) return

      this.error = ""
      this.loading = true
      try {
        const response = await axios.post('/save_narrative', {
          user_id: this.user_id,
          narrative_name: this.narrativeName,
          narrative_content: this.narrativeContent,
          source_stories: this.selectedStories // Include source stories
        })
        // Add success message or notification here
        console.log('Narrative saved successfully')
      } catch (error) {
        this.error = "Failed to save narrative. Please try again."
        console.error("Error saving narrative:", error)
      } finally {
        this.loading = false
      }
    },

    async downloadPDF() {
      if (!this.narrativeContent.trim()) return

      this.error = ""
      this.loading = true
      try {
        const response = await axios.post('/generate_narrative_pdf', {
          narrative_name: this.narrativeName,
          narrative_content: this.narrativeContent,
          source_stories: this.selectedStories.map(story => ({
            name: story.story_name,
            id: story.story_id
          }))
        }, { responseType: 'blob' })

        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${this.narrativeName || 'narrative'}.pdf`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (error) {
        this.error = "Failed to generate PDF. Please try again."
        console.error("Error generating PDF:", error)
      } finally {
        this.loading = false
      }
    },

    async createNarrative() {
  if (!this.narrativeContent.trim()) return

  this.error = ""
  this.loading = true
  try {
    const response = await axios.post('/complete_narrative', {
      user_id: this.user_id,
      narrative_content: this.narrativeContent,
      source_stories: this.selectedStories
    })
    this.narrativeContent = response.data.narrative
    this.isEditable = true
    this.isCompleted = true  // Enable other buttons
  } catch (error) {
    this.error = "Failed to complete narrative. Please try again."
    console.error("Error completing narrative:", error)
  } finally {
    this.loading = false
  }
},

    // Helper method to track selected stories
    updateSelectedStories() {
      this.selectedStories = this.stories.filter(story => 
        this.selectedStoryIds.includes(story.story_id)
      )
    }
  },
  watch: {
    // Watch for changes in selected stories
    selectedStoryIds: {
      handler() {
        this.updateSelectedStories()
      },
      deep: true
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'Didot';
  src: url('@/assets/fonts/Didot.woff2') format('woff2'),
       url('@/assets/fonts/Didot.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

.font-didot {
  font-family: 'Didot', serif;
}
</style>
