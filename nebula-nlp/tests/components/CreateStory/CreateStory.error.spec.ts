// tests/components/CreateStory/CreateStory.error.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import CreateStory from '@/views/CreateStory.vue'
import axios from 'axios'

vi.mock('axios')

describe('CreateStory Error Handling', () => {
    it('handles network errors', async () => {
      const wrapper = mount(CreateStory)
      axios.post.mockRejectedValueOnce(new Error('Network Error'))
  
      await wrapper.vm.generateStory()
      expect(wrapper.vm.error).toContain('Failed')
    })
  
    it('handles invalid story name', async () => {
      const wrapper = mount(CreateStory)
      wrapper.vm.storyName = ''
      
      await wrapper.vm.uploadToDatabase()
      expect(wrapper.vm.error).toContain('title')
    })
  
    it('handles database errors', async () => {
      const wrapper = mount(CreateStory)
      wrapper.vm.isStoryCompleted = true
      wrapper.vm.storyName = 'Test'
      axios.post.mockRejectedValueOnce(new Error('Database Error'))
  
      await wrapper.vm.uploadToDatabase()
      expect(wrapper.vm.error).toContain('Failed to save')
    })
  })