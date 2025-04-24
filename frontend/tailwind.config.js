const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--primary)",
        "primary-foreground": "var(--primary-foreground)",
        border: "var(--border)",
        background: "var(--background)",
        foreground: "var(--foreground)",
        popover: "var(--popover)",
        "popover-foreground": "var(--popover-foreground)",
        muted: "var(--muted)",
        "muted-foreground": "var(--muted-foreground)",
      },
      outline: {
        "ring/50": "2px solid rgba(124, 58, 237, 0.5)",
      },
    },
  },
  plugins: [
    plugin(function ({ addBase }) {
      addBase({
        ":root": {
          "--primary": "#7c3aed",
          "--primary-foreground": "#ffffff",
          "--background": "#f5f3ff", // Light mode background
          "--foreground": "#1e1b4b", // Light mode text
          "--border": "#d4d4d8",
        },
        ".dark": {
          "--primary": "#7c3aed",
          "--primary-foreground": "#ffffff",
          "--background": "#1e1b4b", // Dark mode background
          "--foreground": "#f5f3ff", // Dark mode text
          "--border": "#3f3f46",
        },
      });
    }),
  ],
};