import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center">
          <h1 className="text-5xl font-bold mb-4">
            Welcome to Biz-Bot
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Multi-Tenant WhatsApp & Web Automation Platform for Quebec SMBs
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="border rounded-lg p-6 hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-3">🇨🇦 For Businesses</h2>
            <p className="text-gray-600 mb-4">
              Automate customer interactions, bookings, and FAQs in English and French
            </p>
            <Link 
              href="/auth/login" 
              className="inline-block bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
            >
              Sign In
            </Link>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition">
            <h2 className="text-2xl font-semibold mb-3">⚙️ Admin Portal</h2>
            <p className="text-gray-600 mb-4">
              Manage tenants, users, and system configuration
            </p>
            <Link 
              href="/admin" 
              className="inline-block bg-gray-800 text-white px-6 py-2 rounded hover:bg-gray-900 transition"
            >
              Admin Login
            </Link>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 mt-8">
          <h3 className="text-xl font-semibold mb-3">Features</h3>
          <ul className="grid md:grid-cols-2 gap-3">
            <li className="flex items-start">
              <span className="mr-2">✓</span>
              <span>WhatsApp & SMS Integration (Twilio)</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✓</span>
              <span>Voice AI (ElevenLabs)</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✓</span>
              <span>Booking Management</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✓</span>
              <span>FAQ Automation</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✓</span>
              <span>Bilingual Support (EN/FR-CA)</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✓</span>
              <span>Multi-Tenant Architecture</span>
            </li>
          </ul>
        </div>

        <div className="text-center text-sm text-gray-500 mt-8">
          <p>API Status: <a href="http://localhost:8000/health" className="text-blue-600 hover:underline">Check Health</a></p>
          <p className="mt-2">API Docs: <a href="http://localhost:8000/docs" className="text-blue-600 hover:underline">OpenAPI Documentation</a></p>
        </div>
      </div>
    </main>
  )
}
