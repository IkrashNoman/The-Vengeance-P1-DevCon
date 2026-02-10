/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        "mcs-red": "#EE2022",       // MCS Logo Background
        "mcs-yellow": "#FED001",    // MCS Logo Foreground
        "mcs-light": "#EDEAEC",     // Light accent
        "nust-blue": "#003366",     // Dark blue for NUST branding
        "nust-light": "#0072CE",    // NUST accent
        "gray-light": "#F8F8F8",    // Background gray
        "gray-dark": "#333333",     // Dark text
      },
    },
  },
  plugins: [],
};
