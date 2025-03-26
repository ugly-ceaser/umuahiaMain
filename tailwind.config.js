/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: "#99414A",
        hover: "#101924",
        secondary: "#D4A53F",
        menu: "#EAF6EC",
        border: "#3A0E13",
      },
    },
  },
  plugins: [],
};
