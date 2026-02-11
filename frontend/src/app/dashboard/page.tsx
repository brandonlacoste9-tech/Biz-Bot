'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function DashboardPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [stats, setStats] = useState({ bookings: 0, faqs: 0 })
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/auth/login')
      return
    }
    setIsAuthenticated(true)
    
    // Simulate loading stats
    setStats({ bookings: 15, faqs: 8 })
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    router.push('/')
  }

  if (!isAuthenticated) {
    return <div>Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">Biz-Bot</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-gray-900">EN / FR</button>
              <button 
                onClick={handleLogout}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-3xl font-bold mb-6">Dashboard</h2>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-2">Total Bookings</h3>
              <p className="text-4xl font-bold text-blue-600">{stats.bookings}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-2">Active FAQs</h3>
              <p className="text-4xl font-bold text-green-600">{stats.faqs}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-2">WhatsApp Status</h3>
              <p className="text-2xl font-semibold text-green-600">Connected</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-semibold mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Link 
                  href="/dashboard/bookings"
                  className="block w-full text-left px-4 py-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition"
                >
                  📅 Manage Bookings
                </Link>
                <Link 
                  href="/dashboard/faqs"
                  className="block w-full text-left px-4 py-3 bg-green-50 hover:bg-green-100 rounded-lg transition"
                >
                  ❓ Manage FAQs
                </Link>
                <Link 
                  href="/dashboard/settings"
                  className="block w-full text-left px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition"
                >
                  ⚙️ Settings
                </Link>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-semibold mb-4">Recent Activity</h3>
              <div className="space-y-3 text-sm">
                <div className="pb-3 border-b">
                  <p className="font-medium">New booking received</p>
                  <p className="text-gray-500">2 hours ago</p>
                </div>
                <div className="pb-3 border-b">
                  <p className="font-medium">FAQ answered via WhatsApp</p>
                  <p className="text-gray-500">5 hours ago</p>
                </div>
                <div className="pb-3">
                  <p className="font-medium">System health check passed</p>
                  <p className="text-gray-500">1 day ago</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
