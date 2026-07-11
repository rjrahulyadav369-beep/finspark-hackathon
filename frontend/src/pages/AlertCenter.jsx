import React, { useState, useEffect } from 'react'
import { Bell, Trash2, CheckCircle } from 'lucide-react'

function AlertCenter() {
  const [alerts, setAlerts] = useState([])
  const [filter, setFilter] = useState('OPEN')

  const mockAlerts = [
    {
      id: 1,
      title: 'Multiple Failed Login Attempts',
      description: 'User experienced 5 failed login attempts in 10 minutes',
      severity: 'CRITICAL',
      status: 'OPEN',
      created_at: new Date(Date.now() - 3600000),
    },
    {
      id: 2,
      title: 'Large Transaction Detected',
      description: 'Transaction amount exceeds normal behavior by 300%',
      severity: 'HIGH',
      status: 'OPEN',
      created_at: new Date(Date.now() - 7200000),
    },
    {
      id: 3,
      title: 'New Device Login',
      description: 'Account accessed from a new device in a new location',
      severity: 'MEDIUM',
      status: 'ACKNOWLEDGED',
      created_at: new Date(Date.now() - 86400000),
    },
  ]

  useEffect(() => {
    setAlerts(mockAlerts)
  }, [])

  const filteredAlerts = alerts.filter((a) => a.status === filter)

  const handleResolve = (id) => {
    setAlerts(alerts.map((a) => (a.id === id ? { ...a, status: 'RESOLVED' } : a)))
  }

  const handleDismiss = (id) => {
    setAlerts(alerts.filter((a) => a.id !== id))
  }

  return (
    <div className="space-y-6 animate-fadeInUp">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Alert Center</h1>
        <div className="flex items-center gap-2 px-3 py-2 bg-red-500/20 rounded-lg text-red-300 text-sm font-medium">
          <Bell size={18} />
          {alerts.filter((a) => a.status === 'OPEN').length} Open
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {['OPEN', 'ACKNOWLEDGED', 'RESOLVED', 'FALSE_POSITIVE'].map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg transition ${
              filter === status
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600/50'
            }`}
          >
            {status}
          </button>
        ))}
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.length === 0 ? (
          <div className="glass rounded-lg p-8 text-center border border-blue-500/10">
            <Bell size={48} className="mx-auto text-gray-500 mb-3" />
            <p className="text-gray-400">No {filter.toLowerCase()} alerts</p>
          </div>
        ) : (
          filteredAlerts.map((alert) => (
            <div
              key={alert.id}
              className={`glass rounded-lg p-6 border transition ${
                alert.severity === 'CRITICAL'
                  ? 'border-red-500/30 bg-red-500/5'
                  : alert.severity === 'HIGH'
                  ? 'border-orange-500/30 bg-orange-500/5'
                  : 'border-yellow-500/30 bg-yellow-500/5'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span
                      className={`px-3 py-1 rounded text-xs font-bold ${
                        alert.severity === 'CRITICAL'
                          ? 'bg-red-500/30 text-red-300'
                          : alert.severity === 'HIGH'
                          ? 'bg-orange-500/30 text-orange-300'
                          : 'bg-yellow-500/30 text-yellow-300'
                      }`}
                    >
                      {alert.severity}
                    </span>
                    <span className="text-xs text-gray-500">
                      {alert.created_at.toLocaleString()}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mb-1">{alert.title}</h3>
                  <p className="text-gray-400 text-sm">{alert.description}</p>
                </div>
                <div className="flex gap-2 ml-4">
                  {alert.status !== 'RESOLVED' && (
                    <button
                      onClick={() => handleResolve(alert.id)}
                      className="p-2 hover:bg-green-500/20 rounded transition"
                      title="Resolve"
                    >
                      <CheckCircle size={20} className="text-green-400" />
                    </button>
                  )}
                  <button
                    onClick={() => handleDismiss(alert.id)}
                    className="p-2 hover:bg-red-500/20 rounded transition"
                    title="Dismiss"
                  >
                    <Trash2 size={20} className="text-red-400" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default AlertCenter
