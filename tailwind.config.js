/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js}"
  ],
  theme: {
    extend: {
      colors: {
        dc: {
          primary: '#1a56db',
          'primary-light': '#4F8EF7',
          'primary-dark': '#1240a8',
          accent: '#3b82f6',
          dark: '#0f172a',
          light: '#eff6ff',
        }
      }
    }
  },
  plugins: []
}
