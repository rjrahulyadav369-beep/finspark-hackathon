import { create } from 'zustand'

const useDashboardStore = create((set) => ({
  stats: null,
  events: [],
  alerts: [],
  loading: false,
  error: null,

  setStats: (stats) => set({ stats }),
  setEvents: (events) => set({ events }),
  setAlerts: (alerts) => set({ alerts }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}))

export { useDashboardStore }
