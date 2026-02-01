module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          start: '#7C3AED',
          end: '#A855F7',
        },
        bg: {
          start: '#1a1a2e',
          end: '#16213e',
        },
      },
      fontFamily: {
        display: ['Outfit', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
};
