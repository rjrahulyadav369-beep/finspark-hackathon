import React, { useState, useEffect } from 'react'
import { eventsAPI } from '@/api/client'
import { Search, Filter, Download } from 'lucide-react'

function Events() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(false)
  const [search, setSearch] = useState('')
  const [riskFilter, setRiskFilter] = useState('ALL')
  const [page, setPage] = useState(1)

  useEffect(() => {
    fetchEvents()
  }, [riskFilter, page])

  const fetchEvents = async () => {
    try {
      setLoading(true)
      const params = {
        limit: 20,
        offset: (page - 1) * 20,
        ...(riskFilter !== 'ALL' && { risk_level: riskFilter }),
      }
      const response = await eventsAPI.getAll(params)
      setEvents(response.data)
    } catch (error) {
      console.error('Error fetching events:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredEvents = events.filter((event) =>
    event.event_type.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-6 animate-fadeInUp">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Security Events</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition">
          <Download size={20} />
          Export
        </button>
      </div>

      {/* Search and Filters */}
      <div className="glass rounded-lg p-4 border border-blue-500/10 space-y-4">
        <div className="flex gap-4 flex-col md:flex-row">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 text-gray-500" size={20} />
            <input
              type="text"
              placeholder="Search events..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-700/50 border border-blue-500/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="px-4 py-2 bg-slate-700/50 border border-blue-500/20 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="ALL">All Risk Levels</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
            <option value="SAFE">Safe</option>
          </select>
        </div>
      </div>

      {/* Events Table */}
      <div className="glass rounded-lg border border-blue-500/10 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-800/50 border-b border-blue-500/10">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Timestamp</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Event Type</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">User</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Location</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Risk Score</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Status</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                  Loading events...
                </td>
              </tr>
            ) : filteredEvents.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-6 py-8 text-center text-gray-500">
                  No events found
                </td>
              </tr>
            ) : (
              filteredEvents.map((event) => (
                <tr key={event.id} className="border-t border-blue-500/5 hover:bg-blue-500/5 transition">
                  <td className="px-6 py-4 text-sm text-gray-300">
                    {new Date(event.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">
                    <span className="px-3 py-1 bg-blue-500/20 rounded text-blue-300 text-xs font-medium">
                      {event.event_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">User {event.user_id}</td>
                  <td className="px-6 py-4 text-sm text-gray-400">{event.location || 'N/A'}</td>
                  <td className="px-6 py-4 text-sm font-bold text-white">{event.risk_score.toFixed(1)}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        event.risk_level === 'CRITICAL'
                          ? 'bg-red-500/20 text-red-300'
                          : event.risk_level === 'HIGH'
                          ? 'bg-orange-500/20 text-orange-300'
                          : event.risk_level === 'MEDIUM'
                          ? 'bg-yellow-500/20 text-yellow-300'
                          : event.risk_level === 'LOW'
                          ? 'bg-green-500/20 text-green-300'
                          : 'bg-blue-500/20 text-blue-300'
                      }`}
                    >
                      {event.risk_level}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Events
