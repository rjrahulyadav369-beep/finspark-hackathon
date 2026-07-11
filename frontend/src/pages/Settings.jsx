import React, { useState } from 'react'
import { Moon, Bell, Lock, Eye } from 'lucide-react'

function Settings() {
  const [theme, setTheme] = useState('dark')
  const [notifications, setNotifications] = useState(true)
  const [alertThreshold, setAlertThreshold] = useState(50)

  const handleSave = () => {
    localStorage.setItem('theme', theme)
    localStorage.setItem('notifications', notifications)
    localStorage.setItem('alertThreshold', alertThreshold)
    alert('Settings saved successfully!')
  }

  return (
    <div className="space-y-6 animate-fadeInUp">
      <h1 className="text-3xl font-bold text-white">Settings</h1>

      {/* Display Settings */}
      <div className="glass rounded-lg p-6 border border-blue-500/10">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Moon size={20} /> Display
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-gray-300 font-medium mb-2">Theme</label>
            <select
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="w-full px-4 py-2 bg-slate-700/50 border border-blue-500/20 rounded-lg text-white focus:outline-none focus:border-blue-500"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
              <option value="auto">Auto</option>
            </select>
          </div>
        </div>
      </div>

      {/* Notification Settings */}
      <div className="glass rounded-lg p-6 border border-blue-500/10">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Bell size={20} /> Notifications
        </h3>
        <div className="space-y-4">
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="w-4 h-4 rounded cursor-pointer"
            />
            <span className="text-gray-300">Enable notifications</span>
          </label>
          <div>
            <label className="block text-gray-300 font-medium mb-2">
              Alert Threshold: {alertThreshold}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={alertThreshold}
              onChange={(e) => setAlertThreshold(e.target.value)}
              className="w-full cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Security Settings */}
      <div className="glass rounded-lg p-6 border border-blue-500/10">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Lock size={20} /> Security
        </h3>
        <div className="space-y-3">
          <button className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition">
            Change Password
          </button>
          <button className="w-full px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-gray-200 transition">
            Two-Factor Authentication
          </button>
        </div>
      </div>

      {/* Save Button */}
      <button
        onClick={handleSave}
        className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg text-white font-bold transition"
      >
        Save Settings
      </button>
    </div>
  )
}

export default Settings
