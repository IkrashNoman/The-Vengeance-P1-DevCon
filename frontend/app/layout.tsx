// app/layout.tsx
import './globals.css'

export const metadata = {
  title: 'MCS Olympiad',
  description: 'Landing page for MCS Olympiad',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
