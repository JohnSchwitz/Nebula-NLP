<script setup lang="ts">
import { ref } from 'vue'
const message = ref('This is vue3 CODE')
const count = ref(0)
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

  <div>
    {{ message}}
  </div>
  <div><br><br>
  <button @click="count++">
    Clicked {{ count }} times.
  </button>
  </div>
  </header>

</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
