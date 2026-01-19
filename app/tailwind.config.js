/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        identity: '#6366f1',      // indigo - top layer
        orientation: '#8b5cf6',   // violet
        flow: '#a855f7',          // purple
        structure: '#d946ef',     // fuchsia
        work: '#ec4899',          // pink - bottom layer
      }
    },
  },
  plugins: [],
}

