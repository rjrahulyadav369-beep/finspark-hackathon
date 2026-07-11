import React, { useState, useEffect } from 'react'
import { Download, FileText } from 'lucide-react'
import { reportsAPI } from '@/api/client'

function Reports() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [days, setDays] = useState(30)

  useEffect(() => {
    fetchReport()
  }, [days])

  const fetchReport = async () => {
    try {
      setLoading(true)
      const response = await reportsAPI.getSummary(days)
      setSummary(response.data)
    } catch (error) {
      console.error('Error fetching report:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const response = await reportsAPI.exportCSV(days)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `events_export_${new Date().toISOString()}.csv`)
      document.body.appendChild(link)
      link.click()
      link.parentElement.removeChild(link)
    } catch (error) {
      console.error('Error exporting:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-12 h-12 rounded-full border-4 border-blue-500/30 border-t-blue-500 animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading report...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fadeInUp">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Reports</h1>
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition"
        >
          <Download size={20} />
          Export CSV
        </button>
      </div>

      {/* Period Selector */}
      <div className="glass rounded-lg p-4 border border-blue-500/10">
        <label className="block text-gray-300 font-medium mb-2">Report Period</label>
        <select
          value={days}
          onChange={(e) => setDays(parseInt(e.target.value))}
          className="px-4 py-2 bg-slate-700/50 border border-blue-500/20 rounded-lg text-white focus:outline-none focus:border-blue-500"
        >
          <option value={7}>Last 7 Days</option>
          <option value={30}>Last 30 Days</option>
          <option value={90}>Last 90 Days</option>
          <option value={365}>Last Year</option>
        </select>
      </div>

      {/* Summary Stats */}
      {summary && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <p className="text-gray-400 text-sm">Total Events</p>
              <p className="text-3xl font-bold text-blue-400 mt-2">{summary.total_events}</p>
            </div>
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <p className="text-gray-400 text-sm">Total Alerts</p>
              <p className="text-3xl font-bold text-red-400 mt-2">{summary.total_alerts}</p>
            </div>
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <p className="text-gray-400 text-sm">Critical Events</p>
              <p className="text-3xl font-bold text-red-500 mt-2">{summary.critical_events}</p>
            </div>
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <p className="text-gray-400 text-sm">Average Risk Score</p>
              <p className="text-3xl font-bold text-yellow-400 mt-2">{summary.avg_risk_score}</p>
            </div>
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <p className="text-gray-400 text-sm">High Events</p>
              <p className="text-3xl font-bold text-orange-400 mt-2">{summary.high_events}</p>
            </div>
          </div>

          {/* Top Threat Categories */}
          {summary.top_threat_categories && summary.top_threat_categories.length > 0 && (
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <FileText size={20} /> Top Threat Categories
              </h3>
              <div className="space-y-3">
                {summary.top_threat_categories.map(([category, count], idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                    <span className="text-gray-300">{category}</span>
                    <span className="font-bold text-blue-400">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Top Event Types */}
          {summary.top_event_types && summary.top_event_types.length > 0 && (
            <div className="glass rounded-lg p-6 border border-blue-500/10">
              <h3 className="text-lg font-bold text-white mb-4">Top Event Types</h3>
              <div className="space-y-3">
                {summary.top_event_types.map(([type, count], idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                    <span className="text-gray-300">{type}</span>
                    <span className="font-bold text-purple-400">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default Reports
