<!-- Vueform_reversed.vue -->

<template>
    <form :class="classes.form" @submit.prevent="submit">
      <slot name="empty" :classes="classes">
        <component is="FormLanguages" v-if="showLanguages"/>
        <component is="FormTabs" v-if="showTabs"/>
        <component is="FormSteps" v-if="showSteps"/>
        <FormElements><slot/></FormElements>
        <component is="FormMessages" v-if="showMessages"/>
        <component is="FormErrors" v-if="showErrors"/>
        <component is="FormStepsControls" v-if="showStepsControls"/>
      </slot>
    </form>
  </template>
  
  <script>
  export default {
    data: () => ({
      merge: true,
      defaultClasses: {}
    })
  }
  </script>