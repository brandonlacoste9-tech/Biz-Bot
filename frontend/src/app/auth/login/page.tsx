'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setMessage('')

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/request-magic-link`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      })

      if (response.ok) {
        setMessage('✓ Magic link sent! Check your email (or console in dev mode)')
      } else {
        setMessage('⚠ Error sending magic link. Please try again.')
      }
    } catch (error) {
      setMessage('⚠ Connection error. Is the backend running?')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="text-3xl font-bold text-center">Sign in to Biz-Bot</h2>
          <p className="mt-2 text-center text-gray-600">
            Enter your email to receive a magic link
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-2">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="your@email.com"
            />
          </div>

          {message && (
            <div className={`p-3 rounded ${message.includes('✓') ? 'bg-green-50 text-green-800' : 'bg-yellow-50 text-yellow-800'}`}>
              {message}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400"
          >
            {isLoading ? 'Sending...' : 'Send Magic Link'}
          </button>
        </form>

        <div className="text-center text-sm text-gray-500">
          <p>Don't have an account? Contact your administrator</p>
        </div>
      </div>
    </div>
  )
}
