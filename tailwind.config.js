/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/templates/**/*.html", // Plantillas HTML de Flask
    "./src/static/js/**/*.js",   // Archivos JS en static
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
