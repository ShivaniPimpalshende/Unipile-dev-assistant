/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}", // all files in the app folder
    "./components/**/*.{js,ts,jsx,tsx}" // if you have a components folder
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
