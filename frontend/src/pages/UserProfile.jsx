import React, { useState, useEffect } from 'react'
import { usersAPI } from '@/api/client'
import { useParams } from 'react-router-dom'

function UserProfile() {
  const { id } = useParams()
  const [user, setUser] = useState(null)
  const [riskProfile, setRiskProfile] = useState(null)
  const [transactions, setTransactions] = useState([])
  const [logins, setLogins] = useState([])
  const [devices, setDevices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUserData()
  }, [id])

  const fetchUserData = async () => {
    try {
      setLoading(true)
      const [userRes, riskRes, txRes, loginsRes, devicesRes] = await Promise.all([
        usersAPI.getById(id),
        usersAPI.getRiskProfile(id),
        usersAPI.getTransactions(id),
        usersAPI.getLogins(id),
        usersAPI.getDevices(id),
      ])

      setUser(userRes.data)
      setRiskProfile(riskRes.data)
      setTransactions(txRes.data)
      setLogins(loginsRes.data)
      setDevices(devicesRes.data)
    } catch (error) {
      console.error('Error fetching user data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-4 border-blue-500/30 border-t-blue-500 animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading user profile...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fadeInUp">
      {/* User Header */}
      <div className="glass rounded-lg p-6 border border-blue-500/10">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">{user?.username}</h1>
            <p className="text-gray-400">{user?.email}</p>
            {user?.full_name && <p className="text-gray-400 mt-1">{user.full_name}</p>}
          </div>
          <div className="text-right">
            <p className="text-gray-400 text-sm">Risk Score</p>
            <p className={`text-4xl font-bold mt-1 ${
              riskProfile?.overall_risk_score > 60 ? 'text-red-400' :
              riskProfile?.overall_risk_score > 40 ? 'text-yellow-400' :
              'text-green-400'
            }`}>
              {riskProfile?.overall_risk_score?.toFixed(1) || 0}
            </p>
          </div>
        </div>
      </div>

      {/* Risk Profile Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass rounded-lg p-4 border border-blue-500/10">
          <p className="text-gray-400 text-sm">Threat Level</p>
          <p className="text-2xl font-bold text-white mt-2">{riskProfile?.threat_level}</p>
        </div>
        <div className="glass rounded-lg p-4 border border-blue-500/10">
          <p className="text-gray-400 text-sm">Total Events</p>
          <p className="text-2xl font-bold text-blue-400 mt-2">{riskProfile?.total_events}</p>
        </div>
        <div className="glass rounded-lg p-4 border border-blue-500/10">
          <p className="text-gray-400 text-sm">Flagged Events</p>
          <p className="text-2xl font-bold text-red-400 mt-2">{riskProfile?.flagged_events}</p>
        </div>
      </div>

      {/* Devices */}
      {devices && devices.length > 0 && (
        <div className="glass rounded-lg p-6 border border-blue-500/10">
          <h3 className="text-lg font-bold text-white mb-4">Known Devices</h3>
          <div className="space-y-3">
            {devices.map((device, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <div>
                  <p className="text-white font-medium">{device.device_name}</p>
                  <p className="text-sm text-gray-400">{device.location}</p>
                </div>
                <p className="text-xs text-gray-500">{new Date(device.last_seen).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Transactions */}
      {transactions && transactions.length > 0 && (
        <div className="glass rounded-lg p-6 border border-blue-500/10">
          <h3 className="text-lg font-bold text-white mb-4">Recent Transactions</h3>
          <div className="space-y-3">
            {transactions.slice(0, 5).map((tx) => (
              <div key={tx.id} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <div>
                  <p className="text-white font-medium">${tx.amount.toLocaleString()}</p>
                  <p className="text-sm text-gray-400">{tx.location}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-blue-400">{tx.risk_score.toFixed(1)}</p>
                  <p className="text-xs text-gray-500">{new Date(tx.timestamp).toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default UserProfile
