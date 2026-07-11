import tailwindcss from 'tailwindcss'
import defaultTheme from 'tailwindcss/defaultConfig'

export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        slate: defaultTheme.colors.slate,
        blue: defaultTheme.colors.blue,
        purple: defaultTheme.colors.purple,
      },
      fontFamily: {
        sans: ['system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
