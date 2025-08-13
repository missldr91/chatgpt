import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',
        accent: '#059669',
      },
      fontFamily: {
        sans: ['"Source Sans Pro"', 'sans-serif'],
        heading: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
} satisfies Config;
