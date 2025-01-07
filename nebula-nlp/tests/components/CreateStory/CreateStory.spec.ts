// tests/components/CreateStory/CreateStory.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import CreateStory from '@/views/CreateStory.vue'
import axios from 'axios'

vi.mock('axios')

describe('CreateStory.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('enables ScrollBox editing after Complete Story', async () => {
    const wrapper = mount(CreateStory)
    
    // Mock successful API response
    vi.mocked(axios.post).mockResolvedValueOnce({
      data: { story: 'Completed story' }
    })
    
    await wrapper.vm.completeStory()
    await wrapper.vm.$nextTick()
    
    expect(wrapper.vm.isScrollBoxEditable).toBe(true)
  })

  it('handles API errors gracefully', async () => {
    const wrapper = mount(CreateStory)
    
    // Mock API error
    vi.mocked(axios.post).mockRejectedValueOnce(new Error('API Error'))
    
    await wrapper.vm.completeStory()
    await wrapper.vm.$nextTick()
    
    expect(wrapper.vm.error).toBe('Failed to complete story')
  })
})