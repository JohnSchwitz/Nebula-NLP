<template>
  <div v-if="isAuthenticated" class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-[36px] font-didot text-center mb-8 leading-[1.2]">
      Admin Settings
    </h1>

    <div class="bg-white rounded-lg p-6 shadow-lg">
      <div class="mb-8">
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
  </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AdminView',
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)
    const apiKey = ref('')
    const temperature = ref(0.7)
    const maxTokens = ref(1000)
    const saveStatus = ref(false)

    onMounted(() => {
      const adminStatus = localStorage.getItem('isAdmin')
      if (adminStatus !== 'true') {
        router.push('/admin-login')
      } else {
        isAuthenticated.value = true
        loadSettings()
      }
    })

    const loadSettings = async () => {
      try {
        const response = await axios.get('/api/admin/settings')
        apiKey.value = response.data.apiKey
        temperature.value = response.data.temperature
        maxTokens.value = response.data.maxTokens
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    }

    const saveSettings = async () => {
      try {
        await axios.post('/api/admin/settings', {
          apiKey: apiKey.value,
          temperature: temperature.value,
          maxTokens: maxTokens.value
        })
        saveStatus.value = true
        setTimeout(() => {
          saveStatus.value = false
        }, 3000)
      } catch (error) {
        console.error('Error saving settings:', error)
      }
    }

    const logout = () => {
      localStorage.removeItem('isAdmin')
      router.push('/')
    }

    return {
      isAuthenticated,
      apiKey,
      temperature,
      maxTokens,
      saveStatus,
      saveSettings,
      logout
    }
  }
}
</script>
