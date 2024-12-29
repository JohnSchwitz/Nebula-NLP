/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nebula-yellow': '#FFC107',
        'chatbox-dark': '#4a4a4a',
        'chatbox-light': '#666666',
      },
      fontFamily: {
        didot: ['Didot', 'Didot LT STD', 'Hoefler Text', 'Garamond', 'Times New Roman', 'serif'],
      },
      fontSize: {
        '2xl': '24px',  // For the main instruction text
      }
    },
  },
  plugins: [],
}
