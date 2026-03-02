import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Bharat Content AI',
  description: 'AI-powered multilingual content creation for Indian languages',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
