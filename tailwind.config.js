module.exports = {
  content: [
    "./src/templates/**/*.html", // Archivos de plantillas Flask
    "./src/static/js/**/*.js",
     // Archivos JS en static (si usas Tailwind en scripts)
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF", // Azul oscuro (puedes cambiarlo)
        secondary: "#9333EA", // Púrpura
        accent: "#FACC15", // Amarillo
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"], // Fuente personalizada
        serif: ["Merriweather", "serif"],
      },
      spacing: {
        128: "32rem",
        144: "36rem",
      },
      borderRadius: {
        xl: "1.5rem",
      },
    },
  },
  darkMode: "class", // Habilita el modo oscuro con una clase (ej. <body class="dark">)
  plugins: [
    require("@tailwindcss/forms"), // Estiliza formularios automáticamente
    require("@tailwindcss/typography"), // Estilos para texto largo
    require("@tailwindcss/aspect-ratio"), // Para manejar relaciones de aspecto
  ],
};
