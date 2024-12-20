// App.vue (or your main application component)
<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
import { createRouter, createWebHistory } from 'vue-router';
import CreateStory from './components/CreateStory.vue';
import CreateNarrative from './components/CreateNarrative.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/create-story', component: CreateStory },
        { path: '/create-narrative', component: CreateNarrative },
    ],
});

export default {
    components: {},
    setup() {
        return { router };
    },
};
</script>