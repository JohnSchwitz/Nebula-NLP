// tests/setup/test-setup.ts
import { vi } from 'vitest'
import { config } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import CreateStory from '@/views/CreateStory.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'CreateStory',
      component: CreateStory
    },
    {
      path: '/example-story',
      name: 'ExampleStory',
      component: { template: '<div>Example Story</div>' }
    }
  ]
})

// Configure Vue Test Utils
config.global.plugins = [router]
config.global.stubs = {
  'router-link': true
}

// Mock console.error to reduce noise
console.error = vi.fn()