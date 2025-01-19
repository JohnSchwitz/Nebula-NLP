// AdminVue.vue
<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-[36px] font-didot text-center mb-8 leading-[1.2]">
      Admin Settings
    </h1>

    <div class="bg-white rounded-lg p-6 shadow-lg mb-8">
      <h2 class="text-2xl font-didot mb-4">Story Creator Instructions</h2>
      <div class="space-y-6">
        <!-- Create Story Instructions -->
        <div>
          <label class="block text-lg mb-2 font-didot">Initial AI StoryCreator Instructions</label>
          <textarea
            v-model="storyInstructions"
            rows="4"
            placeholder="Enter instructions for Story Creation..."
            class="w-full p-2 border rounded resize-y font-didot"
          ></textarea>
        </div>

        <!-- Create Narrative Instructions -->
        <div>
          <label class="block text-lg mb-2 font-didot">Initial Narrative Creator Instructions</label>
          <textarea
            v-model="narrativeInstructions"
            rows="4"
            placeholder="Enter instructions for Narrative Creation..."
            class="w-full p-2 border rounded resize-y font-didot"
          ></textarea>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg p-6 shadow-lg mb-8">
      <h2 class="text-2xl font-didot mb-4">Gemini API Configuration</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-lg mb-2">API Key</label>
          <input 
            type="password"
            v-model="apiKey"
            placeholder="Enter Gemini API Key"
            class="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label class="block text-lg mb-2">Temperature</label>
          <input 
            type="number"
            v-model="temperature"
            min="0"
            max="1"
            step="0.1"
            class="w-full p-2 border rounded"
          />
        </div>
        <div>
          <label class="block text-lg mb-2">Max Tokens</label>
          <input 
            type="number"
            v-model="maxTokens"
            class="w-full p-2 border rounded"
          />
        </div>
      </div>
    </div>

    <div class="flex justify-between items-center">
      <button 
        @click="saveSettings"
        class="bg-nebula-yellow text-black px-6 py-3 rounded font-bold hover:bg-opacity-90"
      >
        Save Settings
      </button>
      <button 
        @click="logout"
        class="bg-red-500 text-white px-6 py-3 rounded font-bold hover:bg-opacity-90"
      >
        Logout
      </button>
    </div>

    <div v-if="saveStatus" class="mt-4 text-green-500 text-center">
      Settings saved successfully!
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminView',
  data() {
    return {
      apiKey: '',
      temperature: 0.7,
      maxTokens: 1000,
      storyInstructions: '',
      narrativeInstructions: '',
      saveStatus: false,
      isAuthenticated: false
    }
  },
  async created() {
    this.isAuthenticated = localStorage.getItem('isAdmin') === 'true'
    if (!this.isAuthenticated) {
      await this.$router.push('/admin-login')
      return
    }
    await this.loadSettings()
  },
  methods: {
    async loadSettings() {
      try {
        const response = await axios.get('/api/admin/settings')
        this.apiKey = response.data.apiKey
        this.temperature = response.data.temperature
        this.maxTokens = response.data.maxTokens
        this.storyInstructions = response.data.storyInstructions
        this.narrativeInstructions = response.data.narrativeInstructions
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    },
    async saveSettings() {
      try {
        await axios.post('/api/admin/settings', {
          apiKey: this.apiKey,
          temperature: this.temperature,
          maxTokens: this.maxTokens,
          storyInstructions: this.storyInstructions,
          narrativeInstructions: this.narrativeInstructions
        })
        this.saveStatus = true
        setTimeout(() => {
          this.saveStatus = false
        }, 3000)
      } catch (error) {
        console.error('Error saving settings:', error)
      }
    },
    async logout() {
      localStorage.removeItem('isAdmin')
      await this.$router.push('/')
    }
  }
}
</script>
