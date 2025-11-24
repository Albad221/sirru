import typography from '@tailwindcss/typography';
import containerQueries from '@tailwindcss/container-queries';

/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// Sirru Brand Colors - African-inspired palette
				sirru: {
					// Primary - Deep Forest Green (sovereignty, growth)
					primary: {
						50: '#f0fdf4',
						100: '#dcfce7',
						200: '#bbf7d0',
						300: '#86efac',
						400: '#4ade80',
						500: '#22c55e',
						600: '#16a34a',
						700: '#15803d',
						800: '#166534',
						900: '#14532d',
						950: '#052e16'
					},
					// Secondary - Warm Gold (prosperity, excellence)
					gold: {
						50: '#fefce8',
						100: '#fef9c3',
						200: '#fef08a',
						300: '#fde047',
						400: '#facc15',
						500: '#eab308',
						600: '#ca8a04',
						700: '#a16207',
						800: '#854d0e',
						900: '#713f12',
						950: '#422006'
					},
					// Accent - Terracotta (earth, African heritage)
					terracotta: {
						50: '#fef7ee',
						100: '#feecd6',
						200: '#fcd5ad',
						300: '#f9b679',
						400: '#f58d42',
						500: '#f26d1d',
						600: '#e35213',
						700: '#bc3d12',
						800: '#963116',
						900: '#792b15',
						950: '#411309'
					},
					// Neutral - Slate (professional, modern)
					slate: {
						50: '#f8fafc',
						100: '#f1f5f9',
						200: '#e2e8f0',
						300: '#cbd5e1',
						400: '#94a3b8',
						500: '#64748b',
						600: '#475569',
						700: '#334155',
						800: '#1e293b',
						850: '#172033',
						900: '#0f172a',
						950: '#020617'
					}
				},
				gray: {
					50: 'var(--color-gray-50, #f8fafc)',
					100: 'var(--color-gray-100, #f1f5f9)',
					200: 'var(--color-gray-200, #e2e8f0)',
					300: 'var(--color-gray-300, #cbd5e1)',
					400: 'var(--color-gray-400, #94a3b8)',
					500: 'var(--color-gray-500, #64748b)',
					600: 'var(--color-gray-600, #475569)',
					700: 'var(--color-gray-700, #334155)',
					800: 'var(--color-gray-800, #1e293b)',
					850: 'var(--color-gray-850, #172033)',
					900: 'var(--color-gray-900, #0f172a)',
					950: 'var(--color-gray-950, #020617)'
				}
			},
			fontFamily: {
				sirru: ['Inter', 'Archivo', 'system-ui', 'sans-serif'],
				'sirru-display': ['Archivo', 'Inter', 'system-ui', 'sans-serif']
			},
			boxShadow: {
				'sirru-sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
				'sirru-md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
				'sirru-lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
				'sirru-xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
				'sirru-glow': '0 0 20px rgba(22, 163, 74, 0.3)',
				'sirru-gold-glow': '0 0 20px rgba(234, 179, 8, 0.3)'
			},
			backgroundImage: {
				'sirru-gradient': 'linear-gradient(135deg, #166534 0%, #14532d 50%, #052e16 100%)',
				'sirru-gradient-light': 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
				'sirru-gold-gradient': 'linear-gradient(135deg, #fef9c3 0%, #fde047 50%, #eab308 100%)'
			},
			animation: {
				'sirru-pulse': 'sirru-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
				'sirru-float': 'sirru-float 3s ease-in-out infinite'
			},
			keyframes: {
				'sirru-pulse': {
					'0%, 100%': { opacity: 1 },
					'50%': { opacity: 0.5 }
				},
				'sirru-float': {
					'0%, 100%': { transform: 'translateY(0)' },
					'50%': { transform: 'translateY(-10px)' }
				}
			},
			typography: {
				DEFAULT: {
					css: {
						pre: false,
						code: false,
						'pre code': false,
						'code::before': false,
						'code::after': false
					}
				}
			},
			padding: {
				'safe-bottom': 'env(safe-area-inset-bottom)'
			},
			transitionProperty: {
				width: 'width'
			}
		}
	},
	plugins: [typography, containerQueries]
};
