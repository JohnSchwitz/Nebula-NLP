// CreateStory.vue
<template>
  <div class="max-w-4xl mx-auto px-4">
    <div class="mb-4">
      <p class="text-lg font-didot leading-[1.2]">
        Your turn to create a story. Provide as much detail on the characters, their names,
        the setting, and action or challenge in <b>StoryTeller input:</b>.
        <br><br>
        The <b>AI StoryCreator</b> will then create a story. You may interact with the StoryCreator
        as many times as required to alter or add to the story. Here is an example of AI StoryTelling:
        <router-link
          to="/example-story"
          class="text-blue-600 hover:text-blue-800 underline"
        >
          Fearless Princess Hazel
        </router-link>.
        If you wish to create PDF's or a NARRATIVE from previous stories click the Create Narrative button in the NAVAGATION line above.
      </p>
    </div>

    <div class="my-0">
      <h2 class="text-2xl font-didot font-bold text-center mb-4 leading-[1.2]">
        Instructions to Save Your Story and create a PDF
      </h2>
      <p class="text-lg font-didot text-left leading-[1.2]">
        1) At the prompt below click the Complete Story BUTTON to show your complete Story
        in the ScrollBox. You may then EDIT your story in the ScrollBox.
      </p>
      <p class="text-lg font-didot text-left leading-[1.2]">
        2) Then, enter a Story Name, Upload to Database, and download a PDF of the Story.
      </p>
    </div>

    <div class="flex flex-wrap items-center gap-4 my-8">
      <label for="storyName" class="text-lg font-didot">Story Name</label>
      <input
        type="text"
        v-model="storyName"
        id="storyName"
        placeholder="your story name here"
        class="border rounded px-3 py-2 w-48 font-didot"
      />
       <button
        @click="uploadToDatabase"
        :disabled="!isStoryNameValid || !storyContent.trim()"
        class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Upload to Database
      </button>
       <button
        @click="downloadPDF"
        :disabled="!storyContent.trim()"
        class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
        >
        Download PDF
      </button>
       <button
        @click="generateImage"
       :disabled="!storyContent.trim()"
         class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Generate Image
      </button>
    </div>
     <div class="flex flex-wrap items-center justify-between gap-4 mb-2 w-full">
          <p class="text-lg font-didot font-bold text-left leading-[1.2]">
            AI StoryCreator:
           </p>
        <button
        @click="completeStory"
        :disabled="!storyContent.trim()"
         class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot disabled:opacity-50 disabled:cursor-not-allowed"
        >
         Complete Story
        </button>
        <div class="flex-grow text-center">
          <p class="text-xl font-didot font-bold">ScrollBox</p>
        </div>
        <div class="w-[140px]"></div>
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
          v-model="storyTellerInput"
            placeholder="StoryTeller input:"
         rows="2"
         class="flex-1 bg-white placeholder-black resize-y p-2 focus:outline-none"
        ></textarea>
        <button
          @click="generateStory"
            :disabled="!storyTellerInput.trim() || loading"
        class="bg-white text-black px-6 py-2 rounded font-bold text-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
          Send
       </button>
      </div>
     <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4">
        <span class="block sm:inline">{{ error }}</span>
   </div>
   <img v-if="imageUrl" :src="imageUrl" alt="Generated image" class="w-full rounded-lg" />
 </div>
</template>

<script>
import axios from 'axios'
import api from './api'
import { ref } from 'vue'


const story = ref("")
const prompt = ref("")
const conversationId = ref(null)

async function startStory(){
  conversationId.value = await api.startStoryCreation()

}


async function generateText(){
    try {
        story.value = await api.generateNarrative(prompt.value, conversationId.value)
    } catch (error) {
        console.error(error)
    }
}

export default {
    name: 'CreateStory',
    data() {
        return {
            storyPrompt: `Create an ADVENTURE STORY with CHARACTERS, SETTING, ACTION, MOTIVATION, CHALLENGE and STORY LINE provided by the
              StoryTeller. Please introduce at least one SURPRISE CHARACTER to challenge the HERO and a PLOT TWIST. The STORY should be
              composed in segments each approximately 150 words. Each segment should continue the narrative from the previous. The StoryTeller can
              provide 5 to 7 iterations. The STORY should be 1,000 to 1,200 words.`,
            storyContent: "",
            storyName: "Story Title",
            imageUrl: null,
            user_id: 1,
            messages: [],
            storyTellerInput: "",
           error: "",
            loading: false,
            isEditable: false
       }
    },
    computed: {
        isStoryNameValid() {
           return this.storyName && this.storyName.trim() !== "Story Title"
       }
    },
    mounted() {
       axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL
       this.messages.push({ sender: 'AI', text: this.storyPrompt })
    },
    methods: {
       async generateStory() {
           if (!this.storyTellerInput.trim()) return

         this.error = ""
          this.loading = true
         try {
            this.messages.push({ sender: 'StoryTeller', text: this.storyTellerInput });
          const response = await axios.post('/create_story', {
                user_id: this.user_id,
              initial_prompt: this.storyTellerInput,
             })
              this.messages.push({ sender: 'AI', text: response.data.story })
              this.storyContent = response.data.story
              this.storyTellerInput = "";
        } catch (error) {
            this.error = "Failed to generate story. Please try again."
             console.error("Error generating story:", error)
         } finally {
           this.loading = false
         }
   },
   async uploadToDatabase() {
          if (!this.storyName.trim() || !this.storyContent.trim()) return

           this.error = ""
            this.loading = true
          try {
             const response = await axios.post('/save_story', {
              user_id: this.user_id,
               story_name: this.storyName,
              story_content: this.storyContent
           })
             // Add success message or notification here
             console.log('Story saved successfully')
      } catch (error) {
           this.error = "Failed to save story. Please try again."
           console.error("Error saving story:", error)
         } finally {
           this.loading = false
       }
    },
     async downloadPDF() {
      if (!this.storyContent.trim()) return

         this.error = ""
         this.loading = true
      try {
          const response = await axios.post('/generate_pdf', {
           story_name: this.storyName,
            story_content: this.storyContent
        }, { responseType: 'blob' })

          const url = window.URL.createObjectURL(new Blob([response.data]))
           const link = document.createElement('a')
           link.href = url
        link.setAttribute('download', `${this.storyName || 'story'}.pdf`)
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
   async generateImage() {
          if (!this.storyContent.trim()) return

            this.error = ""
             this.loading = true
        try {
           const response = await axios.post('/generate_image', {
           story_content: this.storyContent
          })
          this.imageUrl = response.data.image_url
       } catch (error) {
            this.error = "Failed to generate image. Please try again."
           console.error("Error generating image:", error)
        } finally {
         this.loading = false
      }
   },
    async completeStory() {
       this.error = ""
         this.loading = true
         try {
           const response = await axios.post('/complete_story', {
           user_id: this.user_id,
                story_content: this.messages.map(m => m.text).join('\n')
            })
             this.storyContent = response.data.story
            this.isEditable = true
           // Clear messages and show the complete story in editable mode
           this.messages = []
       } catch (error) {
           this.error = "Failed to complete story. Please try again."
          console.error("Error completing story:", error)
        } finally {
           this.loading = false
       }
     }
   },
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
.page-container {
  max-width: 1000px;
   margin: 0 auto;
    text-align: left;
}
.instruction-dialog {
    margin-bottom: 20px;
  text-align: left;
}
textarea {
    width: 100%;
     box-sizing: border-box;
}
.chatbox{
   border: 1px solid black;
   min-height: 100px;
    max-height: 300px;
    overflow-y: scroll;
    padding: 10px;
    margin-bottom: 10px;
   background-color: gray;
}
.message-text {
  color: white;
  text-align: left;
}
.AI{
  color: blue;
   font-weight: bold;
  text-align: left;
}
.StoryTeller {
 color: green;
   font-weight: bold;
    text-align: left;
}
.instructions-area {
   margin-top: 20px;
    text-align: center;
}
.input-area {
   display: flex;
    align-items: center;
  width: 100%;
    margin-bottom: 10px;
}
.input-area textarea {
   flex: 1;
   margin-right: 10px;
   background-color: white;
}
.bottom-area {
   display: flex;
    align-items: center;
}
.story-name-input {
   flex: 0 0 200px; /* Limit the input to a specific size */
  margin-right: 10px;
}
.scrollbox-label {
  text-align: center;
  margin-bottom: 5px;
   font-weight: bold;
}
</style>