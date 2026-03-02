import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        periwinkle: {
          DEFAULT: '#B5C7EB',
          50: '#F5F7FC',
          100: '#E8EDF8',
          200: '#D4DFF3',
          300: '#B5C7EB',
          400: '#96AFE3',
          500: '#7797DB',
          600: '#5880D3',
          700: '#4268B8',
          800: '#345194',
          900: '#263A70',
        },
        cyan: {
          DEFAULT: '#9EF0FF',
          50: '#F0FCFF',
          100: '#E0F9FF',
          200: '#C1F3FF',
          300: '#9EF0FF',
          400: '#7BE7FF',
          500: '#58DEFF',
          600: '#35D5FF',
          700: '#12CCFF',
          800: '#00A3CC',
          900: '#007A99',
        },
        lavender: {
          DEFAULT: '#A4A5F5',
          50: '#F5F5FE',
          100: '#EBEBFD',
          200: '#D7D7FB',
          300: '#C3C4F9',
          400: '#A4A5F5',
          500: '#8586F1',
          600: '#6667ED',
          700: '#4748E9',
          800: '#2829D5',
          900: '#1F20A6',
        },
        purple: {
          DEFAULT: '#8E70CF',
          50: '#F3EFFA',
          100: '#E7DFF5',
          200: '#CFBFEB',
          300: '#B79FE1',
          400: '#9F7FD7',
          500: '#8E70CF',
          600: '#7D61C7',
          700: '#6C52BF',
          800: '#5B43B7',
          900: '#4A34AF',
        },
      },
      backgroundImage: {
        'gradient-lavender': 'linear-gradient(135deg, #B5C7EB 0%, #A4A5F5 50%, #8E70CF 100%)',
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      animation: {
        'slide-in-top': 'slide-in-top 0.8s cubic-bezier(0.250, 0.460, 0.450, 0.940) both',
        'text-focus-in': 'text-focus-in 1s cubic-bezier(0.550, 0.085, 0.680, 0.530) both',
        'scale-in-center': 'scale-in-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both',
        'fade-in': 'fade-in 1.2s cubic-bezier(0.390, 0.575, 0.565, 1.000) both',
        'shimmer': 'shimmer 3s linear infinite',
        'bounce-in': 'bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) both',
        'rotate-in-center': 'rotate-in-center 0.6s cubic-bezier(0.250, 0.460, 0.450, 0.940) both',
        'pulsate': 'pulsate 2s ease-in-out infinite',
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite',
        'floating': 'floating 3s ease-in-out infinite',
        'slide-in-blurred-left': 'slide-in-blurred-left 0.6s cubic-bezier(0.230, 1.000, 0.320, 1.000) both',
        'tracking-in-expand': 'tracking-in-expand 0.7s cubic-bezier(0.215, 0.610, 0.355, 1.000) both',
        'flip-in-hor-bottom': 'flip-in-hor-bottom 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both',
      },
      keyframes: {
        'slide-in-top': {
          '0%': { transform: 'translateY(-100px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'text-focus-in': {
          '0%': { filter: 'blur(12px)', opacity: '0' },
          '100%': { filter: 'blur(0px)', opacity: '1' },
        },
        'scale-in-center': {
          '0%': { transform: 'scale(0)', opacity: '1' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
        'bounce-in': {
          '0%': { transform: 'scale(0)', opacity: '0' },
          '50%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        'rotate-in-center': {
          '0%': { transform: 'rotate(-360deg)', opacity: '0' },
          '100%': { transform: 'rotate(0)', opacity: '1' },
        },
        pulsate: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        },
        'glow-pulse': {
          '0%, 100%': {
            boxShadow: '0 0 20px rgba(164, 165, 245, 0.5), 0 0 40px rgba(158, 240, 255, 0.3), 0 0 60px rgba(181, 199, 235, 0.2)',
          },
          '50%': {
            boxShadow: '0 0 30px rgba(164, 165, 245, 0.7), 0 0 60px rgba(158, 240, 255, 0.5), 0 0 90px rgba(181, 199, 235, 0.3)',
          },
        },
        floating: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'slide-in-blurred-left': {
          '0%': { transform: 'translateX(-100px)', filter: 'blur(40px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', filter: 'blur(0)', opacity: '1' },
        },
        'tracking-in-expand': {
          '0%': { letterSpacing: '-0.5em', opacity: '0' },
          '40%': { opacity: '0.6' },
          '100%': { opacity: '1' },
        },
        'flip-in-hor-bottom': {
          '0%': { transform: 'rotateX(80deg)', opacity: '0' },
          '100%': { transform: 'rotateX(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
