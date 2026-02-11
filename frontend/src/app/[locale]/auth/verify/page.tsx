'use client'

import { useEffect, useState } from 'react'
import { useSearchParams, useRouter, useParams } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { authAPI } from '@/lib/api'

export default function VerifyPage() {
  const t = useTranslations('auth')
  const searchParams = useSearchParams()
  const router = useRouter()
  const params = useParams()
  const locale = params.locale as string
  
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying')

  useEffect(() => {
    const token = searchParams.get('token')
    
    if (!token) {
      setStatus('error')
      return
    }

    const verify = async () => {
      try {
        const response = await authAPI.verifyMagicLink(token)
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        localStorage.setItem('tenant', JSON.stringify(response.data.tenant))
        
        setStatus('success')
        
        // Redirect to dashboard
        setTimeout(() => {
          router.push(`/${locale}/dashboard`)
        }, 1500)
      } catch (error) {
        setStatus('error')
      }
    }

    verify()
  }, [searchParams, router, locale])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full text-center space-y-8">
        {status === 'verifying' && (
          <>
            <div className="text-6xl animate-spin">⚡</div>
            <h2 className="text-2xl font-bold">{t('verifying')}</h2>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div className="text-6xl">✅</div>
            <h2 className="text-2xl font-bold text-green-600">{t('loginSuccess')}</h2>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div className="text-6xl">❌</div>
            <h2 className="text-2xl font-bold text-red-600">Invalid or expired token</h2>
          </>
        )}
      </div>
    </div>
  )
}
