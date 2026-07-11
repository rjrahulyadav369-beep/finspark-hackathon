import React, { useState, useEffect } from 'react'
import { AlertCircle, TrendingUp, Activity, Shield } from 'lucide-react'
import { dashboardAPI } from '@/api/client'

function StatCard({ icon: Icon, label, value, trend, color }) {
  return (
    <div className="glass rounded-lg p-6 hover:border-blue-400/50 transition border border-blue-500/10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm font-medium">{label}</p>
          <p className="text-3xl font-bold text-white mt-2">{value}</p>
          {trend && (
            <p className={`text-xs mt-2 ${
              trend > 0 ? 'text-red-400' : 'text-green-400'
            }`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last week
            </p>
          )}
        </div>
        <div
          className={`w-12 h-12 rounded-lg flex items-center justify-center ${
            color || 'bg-blue-500/20'
          }`}
        >
          <Icon size={24} className="text-blue-400" />
        </div>
      </div>
    </div>
  )
}

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const response = await dashboardAPI.getStats()
      setStats(response.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-4 border-blue-500/30 border-t-blue-500 animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-300">
        Error loading dashboard: {error}
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fadeInUp">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">Real-time threat intelligence and security monitoring</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Activity}
          label="Total Events"
          value={stats?.total_events || 0}
          trend={5}
          color="bg-blue-500/20"
        />
        <StatCard
          icon={AlertCircle}
          label="Critical Alerts"
          value={stats?.alerts_by_severity?.CRITICAL || 0}
          trend={12}
          color="bg-red-500/20"
        />
        <StatCard
          icon={TrendingUp}
          label="Risk Score"
          value={`${(stats?.average_risk_score || 0).toFixed(1)}/100`}
          color="bg-yellow-500/20"
        />
        <StatCard
          icon={Shield}
          label="Flagged Events"
          value={stats?.flagged_events || 0}
          color="bg-purple-500/20"
        />
      </div>

      {/* Risk Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-lg p-6 border border-blue-500/10">
          <h3 className="text-lg font-bold text-white mb-4">Events by Risk Level</h3>
          <div className="space-y-3">
            {Object.entries(stats?.events_by_risk_level || {}).map(([level, count]) => (
              <div key={level} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-3 h-3 rounded-full ${
                      level === 'CRITICAL'
                        ? 'bg-red-500'
                        : level === 'HIGH'
                        ? 'bg-orange-500'
                        : level === 'MEDIUM'
                        ? 'bg-yellow-500'
                        : level === 'LOW'
                        ? 'bg-green-500'
                        : 'bg-blue-500'
                    }`}
                  />
                  <span className="text-gray-300 font-medium">{level}</span>
                </div>
                <span className="text-white font-bold">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass rounded-lg p-6 border border-blue-500/10">
          <h3 className="text-lg font-bold text-white mb-4">Alerts by Severity</h3>
          <div className="space-y-3">
            {Object.entries(stats?.alerts_by_severity || {}).map(([severity, count]) => (
              <div key={severity} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-3 h-3 rounded-full ${
                      severity === 'CRITICAL'
                        ? 'bg-red-500'
                        : severity === 'HIGH'
                        ? 'bg-orange-500'
                        : severity === 'MEDIUM'
                        ? 'bg-yellow-500'
                        : 'bg-green-500'
                    }`}
                  />
                  <span className="text-gray-300 font-medium">{severity}</span>
                </div>
                <span className="text-white font-bold">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Last 24 Hours */}
      <div className="glass rounded-lg p-6 border border-blue-500/10">
        <h3 className="text-lg font-bold text-white mb-4">Last 24 Hours</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-gray-400 text-sm">Events</p>
            <p className="text-2xl font-bold text-blue-400 mt-1">{stats?.last_24_hours?.events || 0}</p>
          </div>
          <div>
            <p className="text-gray-400 text-sm">Alerts</p>
            <p className="text-2xl font-bold text-red-400 mt-1">{stats?.last_24_hours?.alerts || 0}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
