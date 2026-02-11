'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

export default function VerifyPage() {
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying')
  const [message, setMessage] = useState('')
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const token = searchParams.get('token')
    
    if (!token) {
      setStatus('error')
      setMessage('No token provided')
      return
    }

    const verifyToken = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/verify-magic-link`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token }),
        })

        if (response.ok) {
          const data = await response.json()
          localStorage.setItem('access_token', data.access_token)
          setStatus('success')
          setMessage('Successfully logged in! Redirecting...')
          
          setTimeout(() => {
            router.push('/dashboard')
          }, 1500)
        } else {
          setStatus('error')
          setMessage('Invalid or expired magic link')
        }
      } catch (error) {
        setStatus('error')
        setMessage('Connection error. Please try again.')
      }
    }

    verifyToken()
  }, [searchParams, router])

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-4">
        {status === 'verifying' && (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <h2 className="text-2xl font-bold">Verifying...</h2>
            <p className="text-gray-600">Please wait while we verify your magic link</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="text-green-600 text-5xl">✓</div>
            <h2 className="text-2xl font-bold text-green-600">Success!</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="text-red-600 text-5xl">✗</div>
            <h2 className="text-2xl font-bold text-red-600">Error</h2>
            <p className="text-gray-600">{message}</p>
            <button
              onClick={() => router.push('/auth/login')}
              className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Try Again
            </button>
          </>
        )}
      </div>
    </div>
  )
}
