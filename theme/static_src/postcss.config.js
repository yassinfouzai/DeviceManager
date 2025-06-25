module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
    "postcss-simple-vars": {},
    "postcss-nested": {}
  },
  theme: {
    extend: {
      colors: {
        'mint-500': 'oklch(0.72 0.11 178)', // You can also use a CSS variable here
      },
    },
  },
}
