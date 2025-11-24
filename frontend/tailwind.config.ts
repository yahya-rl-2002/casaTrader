import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fear: {
          100: "#fcd7d4",
          500: "#f15b5b",
          700: "#a82020",
        },
        greed: {
          100: "#d1f7da",
          500: "#33cc66",
          700: "#1a7f3a",
        },
      },
    },
  },
  plugins: [],
};

export default config;



