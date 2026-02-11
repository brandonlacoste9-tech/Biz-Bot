'use client'

import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { useRouter, useParams } from 'next/navigation'
import { bookingAPI } from '@/lib/api'

export default function DashboardPage() {
  const t = useTranslations('dashboard')
  const router = useRouter()
  const params = useParams()
  const locale = params.locale as string
  
  const [user, setUser] = useState<any>(null)
  const [tenant, setTenant] = useState<any>(null)
  const [bookings, setBookings] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token')
    if (!token) {
      router.push(`/${locale}/auth/login`)
      return
    }

    const userData = localStorage.getItem('user')
    const tenantData = localStorage.getItem('tenant')
    
    if (userData && tenantData) {
      setUser(JSON.parse(userData))
      setTenant(JSON.parse(tenantData))
    }

    // Load bookings
    loadBookings()
  }, [router, locale])

  const loadBookings = async () => {
    try {
      const response = await bookingAPI.list()
      setBookings(response.data)
    } catch (error) {
      console.error('Failed to load bookings:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('tenant')
    router.push(`/${locale}`)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl">Loading...</div>
      </div>
    )
  }

  const pendingBookings = bookings.filter(b => b.status === 'pending').length
  const totalBookings = bookings.length

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {tenant?.name || 'Dashboard'}
              </h1>
              <p className="text-sm text-gray-600">
                {t('welcome')}, {user?.full_name || user?.email}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
            >
              {t('logout')}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">{t('stats.totalBookings')}</div>
            <div className="text-3xl font-bold text-primary-600">{totalBookings}</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">{t('stats.pendingBookings')}</div>
            <div className="text-3xl font-bold text-yellow-600">{pendingBookings}</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600">Status</div>
            <div className="text-3xl font-bold text-green-600">Active</div>
          </div>
        </div>

        {/* Recent Bookings */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold">{t('bookings')}</h2>
          </div>
          <div className="p-6">
            {bookings.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No bookings yet</p>
            ) : (
              <div className="space-y-4">
                {bookings.slice(0, 5).map((booking) => (
                  <div key={booking.id} className="border-l-4 border-primary-600 pl-4 py-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-semibold">{booking.customer_name}</div>
                        <div className="text-sm text-gray-600">{booking.service_type}</div>
                        <div className="text-sm text-gray-500">{booking.customer_phone}</div>
                      </div>
                      <div className="text-right">
                        <div className={`inline-block px-2 py-1 text-xs rounded ${
                          booking.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                          booking.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {booking.status}
                        </div>
                        <div className="text-sm text-gray-500 mt-1">
                          {new Date(booking.appointment_date).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
