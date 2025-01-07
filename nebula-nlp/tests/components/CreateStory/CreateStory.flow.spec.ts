import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import CreateStory from '@/views/CreateStory.vue'
import axios from 'axios'

vi.mock('axios')

describe('CreateStory User Flows', () => {
  it('completes full story creation flow', async () => {
    const wrapper = mount(CreateStory)
    
    // 1. Enter story input
    const input = wrapper.find('[data-test="storyteller-input"]')
    expect(input.exists()).toBe(true)
    await input.setValue('Test story input')
    
    // 2. Send story
    const sendButton = wrapper.find('[data-test="send-button"]')
    expect(sendButton.exists()).toBe(true)
    axios.post.mockResolvedValueOnce({ 
      data: { story: 'Generated story' } 
    })
    await sendButton.trigger('click')
    
    // 3. Complete story
    const completeButton = wrapper.find('[data-test="complete-button"]')
    expect(completeButton.exists()).toBe(true)
    axios.post.mockResolvedValueOnce({ 
      data: { story: 'Completed story' } 
    })
    await completeButton.trigger('click')
    
    // 4. Set story name
    const nameInput = wrapper.find('[data-test="story-name"]')
    expect(nameInput.exists()).toBe(true)
    await nameInput.setValue('My Story')
    
    // 5. Upload to database
    const uploadButton = wrapper.find('[data-test="upload-button"]')
    expect(uploadButton.exists()).toBe(true)
    axios.post.mockResolvedValueOnce({ 
      data: { story_id: 1 } 
    })
    await uploadButton.trigger('click')
    
    // Verify final state
    expect(wrapper.vm.error).toBeFalsy()
    expect(axios.post).toHaveBeenCalledTimes(3)
  })
})