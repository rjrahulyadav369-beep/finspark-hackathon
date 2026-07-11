import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { LogOut, Settings, User } from 'lucide-react'

function Navbar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="glass border-b border-blue-500/20 sticky top-0 z-40">
      <div className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <span className="text-white font-bold text-lg">🛡️</span>
          </div>
          <div>
            <h1 className="text-white font-bold">BankShield AI</h1>
            <p className="text-xs text-gray-400">Cybersecurity Dashboard</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {user && (
            <>
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-white">{user.full_name || user.username}</p>
                <p className="text-xs text-gray-400">{user.email}</p>
              </div>
              <button
                onClick={() => navigate('/settings')}
                className="p-2 hover:bg-blue-500/10 rounded-lg transition"
                title="Settings"
              >
                <Settings size={20} className="text-gray-400 hover:text-blue-400" />
              </button>
              <button
                onClick={handleLogout}
                className="p-2 hover:bg-red-500/10 rounded-lg transition"
                title="Logout"
              >
                <LogOut size={20} className="text-gray-400 hover:text-red-400" />
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
