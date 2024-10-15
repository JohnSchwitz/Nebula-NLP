<?php
/*
Plugin Name: VueAI
Description: A simple plugin to add a Vue.js form using a shortcode.
Version: 1.0
Author: John G Schwitz
*/
// Enqueue Vue app script
function vue_form_enqueue_scripts() {
// Register the main JavaScript app file generated by Vite
wp_enqueue_script(
'vue-form-app',
plugins_url('/dist/assets/index.js', __FILE__), // Adjust this path if necessary
[], // Add dependencies if needed
null, // Versioning can be by filemtime
true // Load in footer
);
// Optionally, enqueue the CSS file if your Vue app needs it
wp_enqueue_style(
'vue-form-styles',
plugins_url('/dist/assets/index.css', __FILE__), // Adjust this path if necessary
[],
null
);
}
add_action('wp_enqueue_scripts', 'vue_form_enqueue_scripts');
// Create the shortcode to render the Vue component
function vue_form_shortcode() {
// Retrieve the user_id
    $current_user_id = get_current_user_id();
    return '<div id="vue-form" data-user-id="' . esc_attr($current_user_id) . '"></div>';
    // Ensure to include a div that matches the element ID the Vue app mounts to
    return '<div id="app"></div>';
}
add_shortcode('vueform', 'vue_form_shortcode');