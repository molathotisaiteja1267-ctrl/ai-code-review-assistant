/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fff8f1',
          100: '#ffeedb',
          200: '#ffd8b5',
          300: '#ffbe85',
          400: '#ff9b4d',
          500: '#ff6a00', // Primary Orange
          600: '#f4511e', // Deep Orange
          700: '#d83b01',
          800: '#ab2e00',
          900: '#8c2600',
        },
        surface: {
          bg: '#fffdf9',       // Warm primary background
          subtle: '#fff8f1',   // Secondary background
          card: '#ffffff',     // Card surface
          border: '#e8e0d8',   // Subtle border
          hover: '#fbf5ee',
          active: '#faefe2'
        },
        text: {
          primary: '#1f1f1f',
          secondary: '#6b7280',
          muted: '#9ca3af',
        },
        accent: {
          yellow: '#ffc107',
          yellowLight: '#fff4cc',
          red: '#e53935',
          redLight: '#fff0f0',
          green: '#2e7d32',
          greenLight: '#e8f5e9',
          blue: '#1976d2',
          blueLight: '#e3f2fd',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'IBM Plex Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'subtle': '0 1px 2px 0 rgba(0, 0, 0, 0.04)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.06), 0 1px 2px -1px rgba(0, 0, 0, 0.04)',
        'elevated': '0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}
