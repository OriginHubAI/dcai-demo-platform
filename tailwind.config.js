/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js}"
  ],
  theme: {
    extend: {
      colors: {
        hf: {
          yellow: '#FFD21E',
          'yellow-dark': '#E5BD1A',
          dark: '#1a1a2e',
        }
      }
    }
  },
  plugins: []
}
