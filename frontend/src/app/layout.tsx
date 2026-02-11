import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Biz-Bot - Multi-Tenant Automation Platform',
  description: 'WhatsApp and web automation for Quebec SMBs',
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
