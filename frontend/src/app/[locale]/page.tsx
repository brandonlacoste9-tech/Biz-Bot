'use client'

import { useTranslations } from 'next-intl'
import Link from 'next/link'
import { useParams } from 'next/navigation'

export default function HomePage() {
  const t = useTranslations('home')
  const params = useParams()
  const locale = params.locale as string

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold text-primary-600">
            Biz-Bot
          </h1>
          <p className="text-xl text-gray-600">
            {t('tagline')}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <Link 
            href={`/${locale}/auth/login`}
            className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
          >
            <h2 className="text-2xl font-semibold mb-2">
              {t('login')}
            </h2>
            <p className="text-gray-600">
              {t('loginDescription')}
            </p>
          </Link>

          <Link 
            href={`/${locale}/onboarding`}
            className="block p-6 bg-primary-600 text-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
          >
            <h2 className="text-2xl font-semibold mb-2">
              {t('getStarted')}
            </h2>
            <p className="text-primary-100">
              {t('getStartedDescription')}
            </p>
          </Link>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="text-center space-y-2">
            <div className="text-4xl">📱</div>
            <h3 className="font-semibold">{t('features.whatsapp')}</h3>
            <p className="text-sm text-gray-600">{t('features.whatsappDesc')}</p>
          </div>
          
          <div className="text-center space-y-2">
            <div className="text-4xl">📅</div>
            <h3 className="font-semibold">{t('features.booking')}</h3>
            <p className="text-sm text-gray-600">{t('features.bookingDesc')}</p>
          </div>
          
          <div className="text-center space-y-2">
            <div className="text-4xl">🤖</div>
            <h3 className="font-semibold">{t('features.automation')}</h3>
            <p className="text-sm text-gray-600">{t('features.automationDesc')}</p>
          </div>
        </div>

        <div className="text-center pt-8">
          <div className="space-x-4">
            <Link 
              href="/en" 
              className={`px-4 py-2 rounded ${locale === 'en' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            >
              English
            </Link>
            <Link 
              href="/fr" 
              className={`px-4 py-2 rounded ${locale === 'fr' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            >
              Français
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
