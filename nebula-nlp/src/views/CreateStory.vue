// CreateStory.vue
<template>
  <div class="max-w-4xl mx-auto px-4">
    <!-- Main instruction text -->
    <div class="mb-8">
      <p class="text-2xl font-didot leading-[1.2]">
        Your turn to create a story. Provide as much detail on the characters, their names, the setting, and action or challenge. The AI agent will then create a
        story and permit you to modify as many times as required. Here is another example of AI StoryTelling: Fearless Princess Hazel. If you wish to create
        PDF's or a NARRATIVE from previous stories click the Create Narrative button in the NAVIGATION line above.
        <br><br>
        Please follow the instructions below to upload your Story to the database.
        Once you create a story you may download a PDF of the Story.
      </p>
    </div>

    <!-- Chatbox -->
    <div class="bg-chatbox-dark rounded-lg p-4 mb-4 min-h-[200px] max-h-[400px] overflow-y-auto">
      <div v-for="(message, index) in messages" 
           :key="index" 
           class="mb-3">
        <div :class="message.sender === 'AI' ? 'bg-chatbox-light' : 'bg-chatbox-light'" 
             class="rounded p-3 relative">
          <span v-if="message.sender === 'AI'" 
                class="text-white font-bold absolute left-3">
            AI:
          </span>
          <span class="text-white block" 
                :class="message.sender === 'AI' ? 'ml-8' : ''">
            {{ message.text }}
          </span>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="bg-chatbox-light rounded-lg p-4 flex gap-4 items-start">
      <textarea 
        v-model="storyTellerInput" 
        placeholder="StoryTeller input:"
        rows="2"
        class="flex-1 bg-chatbox-light text-white placeholder-gray-300 resize-y p-2 focus:outline-none"
      ></textarea>
      <button 
        @click="generateStory"
        class="bg-white text-black px-6 py-2 rounded font-bold text-lg hover:bg-gray-100 transition-colors"
      >
        Send
      </button>
    </div>

    <!-- Instructions -->
    <div class="my-8">
      <h2 class="text-[36px] font-didot text-center mb-4 leading-[1.2]">
        Instructions to Save Your Story and create a PDF
      </h2>
      <p class="text-2xl font-didot text-left leading-[1.2]">
        1) At the prompt below click the Complete Story BUTTON. You may then EDIT your story in the ScrollBox.
      </p>
      <p class="text-2xl font-didot text-left leading-[1.2]">
        2) Enter a Story Name, Upload to Database, and then download a PDF.
      </p>
    </div>

    <!-- Bottom Controls -->
    <div class="flex flex-wrap items-center gap-4 my-8">
      <label for="storyName" class="font-didot">Story Name</label>
      <input 
        type="text" 
        v-model="storyName" 
        id="storyName" 
        placeholder="your story name here" 
        class="border rounded px-3 py-2 w-48 font-didot"
      >
      <button class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot">
        Upload to Database
      </button>
      <button class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot">
        Download PDF
      </button>
      <button class="bg-white text-black px-4 py-2 rounded font-bold hover:bg-gray-100 font-didot">
        Generate Image
      </button>
    </div>

    <!-- Scrollbox -->
    <div class="text-center font-bold mb-2 font-didot">ScrollBox</div>
    <textarea 
      v-model="storyContent" 
      readonly 
      class="w-full min-h-[300px] border rounded p-4 resize-y mb-8 font-didot"
    ></textarea>
    
    <img v-if="imageUrl" :src="imageUrl" alt="Generated image" class="w-full rounded-lg">
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateStory',
  data() {
    return {
      storyPrompt: `Create an ADVENTURE STORY with CHARACTERS, SETTING, ACTION, MOTIVATION, CHALLENGE and STORY LINE provided by the
          StoryTeller. Please introduce at least one SURPRISE CHARACTER to challenge the HERO and a PLOT TWIST. The STORY should be
          composed in segments each approximately 150 words. Each segment should continue the narrative from the previous. The StoryTeller can
          provide 5 to 7 iterations. The STORY should be 1,000 to 1,200 words.`,
      storyContent: `Professor Amelia Thorne, a paleontologist with a fiery spirit and a penchant for the unorthodox, had scoffed at the notion of a living Pterodactylus. Yet, here she was, deep within the untamed wilderness of the Amazon rainforest, driven by a thirst for knowledge and a stubborn streak that refused to accept defeat. Her trusty graduate assistant, young and eager Ethan, trailed behind, his backpack laden with equipment and a healthy dose of apprehension. The rainforest was a symphony of sounds, a cacophony of life that both captivated and unnerved Amelia. The air hung thick with humidity, the scent of decaying leaves and damp earth clinging to her clothes. As they ventured deeper, the foliage grew denser, sunlight struggling to penetrate the leafy canopy. Ethan shivered, his hand instinctively reaching for the machete strapped to his waist. "Don't worry, Ethan," Amelia said, her voice a reassuring calm amidst the overwhelming grandeur. "The stories about this place are exaggerated. It's just a rainforest, albeit a particularly dense one." Her words held a tremor of uncertainty that she did not allow Ethan to see. The rumors of the Pterodactylus had been dismissed by the scientific community as folklore, yet a flicker of hope, a spark of possibility, ignited within her.Suddenly Amelia noticed that the forest was thinned by a machete trail. "Ethan, I am afraid that we are not alone. Also, did you remember to bring the pack of medicines and emergency kit? I seem to remember that they were in a white and red knapsack."Amelia's eyes narrowed as she scrutinized the trail. It was undeniably recent, the freshly cut vegetation still damp with morning dew. A chill ran down her spine. "Ethan, check your backpack," she said, her voice laced with urgency. "Did you bring the emergency kit?"Ethan rummaged through his backpack, his brow furrowed in concentration. "I... I don't think so, Professor. I thought you had it," he stammered, his voice betraying his growing anxiety. Amelia's heart sank. The emergency kit was essential, containing antidotes for venomous bites and stings, as well as basic medical supplies. "We need to find it," she said, her voice firm despite the rising panic within her. "We can't go forward without it. "They retraced their steps, searching for the missing knapsack. The jungle seemed to close in around them, the air thick with an unsettling silence. The machete trail disappeared into the dense foliage, leading them deeper into the unknown. Amelia's mind raced, conjuring images of poachers, illegal loggers, or worse, a rival expedition seeking the same prize.`,
      storyName: "Story Title",
      imageUrl: null,
      user_id: 1,
      messages: [],
      storyTellerInput: ""
    }
  },
  mounted() {
    axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL
    this.messages.push({ sender: 'AI', text: this.storyPrompt })
  },
  // ... rest of the methods
}
</script>

<style scoped>
/* Custom font loading */
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