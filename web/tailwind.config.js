/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './layouts/**/*.html',
  ],
  safelist: [{
    pattern: /(text-blue-600|text-yellow-500|text-orange-600)/,
    variants: ['hover', 'focus'],
  }, ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
