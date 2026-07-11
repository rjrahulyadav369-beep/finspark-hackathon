import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, Shield, Zap, BarChart3, Lock, Users, CheckCircle } from 'lucide-react'

function Landing() {
  const navigate = useNavigate()

  const features = [
    {
      icon: Shield,
      title: 'Intelligent Threat Detection',
      description: 'AI-powered correlation of 10+ banking security events to detect suspicious behavior before fraud happens.',
    },
    {
      icon: Zap,
      title: 'Real-time Risk Scoring',
      description: 'Instant ML-powered risk assessment with confidence scores and threat categorization.',
    },
    {
      icon: BarChart3,
      title: 'Advanced Analytics',
      description: 'Comprehensive dashboards with threat timelines, risk distribution, and behavioral analysis.',
    },
    {
      icon: Lock,
      title: 'Enterprise Security',
      description: 'JWT authentication, password hashing, CORS protection, and rate limiting.',
    },
    {
      icon: Users,
      title: 'User Intelligence',
      description: 'Deep user profiling with transaction history, device tracking, and risk assessment.',
    },
    {
      icon: CheckCircle,
      title: 'AI Chat Assistant',
      description: 'Ask the AI why accounts were flagged and get detailed explanations instantly.',
    },
  ]

  const stats = [
    { number: '10+', label: 'Event Types' },
    { number: '92%', label: 'Model Accuracy' },
    { number: '5', label: 'Risk Levels' },
    { number: '<100ms', label: 'Prediction Time' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white overflow-hidden">
      {/* Navigation */}
      <nav className="glass border-b border-blue-500/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg">🛡️</span>
            </div>
            <h1 className="text-xl font-bold">BankShield AI</h1>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/login')}
              className="px-4 py-2 text-gray-300 hover:text-white transition"
            >
              Login
            </button>
            <button
              onClick={() => navigate('/register')}
              className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-medium transition"
            >
              Sign Up
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-20 relative">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
        </div>

        <div className="relative z-10 text-center mb-16 animate-fadeInUp">
          <h2 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
            <span className="gradient-text">AI-Powered Cyber Threat</span>
            <br />
            Correlation & Risk Intelligence
          </h2>
          <p className="text-xl text-gray-400 mb-8 max-w-3xl mx-auto">
            Intelligently correlate banking security events and detect suspicious behavior before fraud happens. 
            Real-time risk scoring powered by machine learning.
          </p>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/register')}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold text-lg transition flex items-center justify-center gap-2"
            >
              Get Started <ArrowRight size={20} />
            </button>
            <button
              onClick={() => document.getElementById('demo').scrollIntoView({ behavior: 'smooth' })}
              className="px-8 py-4 bg-slate-700/50 hover:bg-slate-600/50 rounded-lg font-bold text-lg transition border border-blue-500/20"
            >
              Watch Demo
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20">
          {stats.map((stat, idx) => (
            <div
              key={idx}
              className="glass rounded-lg p-6 border border-blue-500/10 text-center hover:border-blue-500/30 transition"
            >
              <p className="text-4xl font-bold gradient-text mb-2">{stat.number}</p>
              <p className="text-gray-400 text-sm">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h3 className="text-4xl md:text-5xl font-bold mb-4">Powerful Features</h3>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Enterprise-grade security intelligence with AI-powered threat detection and analysis.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon
            return (
              <div
                key={idx}
                className="glass rounded-lg p-8 border border-blue-500/10 hover:border-blue-500/30 transition group"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center mb-4 group-hover:scale-110 transition">
                  <Icon size={24} className="text-white" />
                </div>
                <h4 className="text-xl font-bold mb-2">{feature.title}</h4>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </section>

      {/* Demo Section */}
      <section id="demo" className="max-w-7xl mx-auto px-6 py-20">
        <div className="glass rounded-lg p-12 border border-blue-500/10 bg-gradient-to-br from-blue-500/5 to-purple-500/5">
          <h3 className="text-3xl md:text-4xl font-bold mb-6">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <div className="text-4xl font-bold text-blue-400 mb-2">1</div>
              <h4 className="text-xl font-bold mb-2">Upload Banking Logs</h4>
              <p className="text-gray-400">Import CSV files with security events from your banking infrastructure.</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-400 mb-2">2</div>
              <h4 className="text-xl font-bold mb-2">AI Correlation</h4>
              <p className="text-gray-400">Our ML models analyze and correlate 10+ event types simultaneously.</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-pink-400 mb-2">3</div>
              <h4 className="text-xl font-bold mb-2">Risk Intelligence</h4>
              <p className="text-gray-400">Get instant risk scores, threat categories, and recommended actions.</p>
            </div>
          </div>
          <button
            onClick={() => navigate('/login')}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold transition"
          >
            Try Now →
          </button>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <h3 className="text-3xl md:text-4xl font-bold mb-12 text-center">Technology Stack</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="glass rounded-lg p-6 border border-blue-500/10 text-center">
            <p className="font-bold mb-2">Frontend</p>
            <p className="text-sm text-gray-400">React • Vite • Tailwind • TypeScript</p>
          </div>
          <div className="glass rounded-lg p-6 border border-blue-500/10 text-center">
            <p className="font-bold mb-2">Backend</p>
            <p className="text-sm text-gray-400">Python • FastAPI • SQLAlchemy</p>
          </div>
          <div className="glass rounded-lg p-6 border border-blue-500/10 text-center">
            <p className="font-bold mb-2">Machine Learning</p>
            <p className="text-sm text-gray-400">Scikit-learn • Random Forest • XGBoost</p>
          </div>
          <div className="glass rounded-lg p-6 border border-blue-500/10 text-center">
            <p className="font-bold mb-2">Deployment</p>
            <p className="text-sm text-gray-400">Docker • GitHub • Cloud Ready</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="glass rounded-lg p-12 border border-blue-500/10 text-center">
          <h3 className="text-3xl md:text-4xl font-bold mb-4">Ready to Secure Your Bank?</h3>
          <p className="text-gray-400 mb-8 text-lg">Start detecting threats with AI-powered intelligence today.</p>
          <button
            onClick={() => navigate('/register')}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold text-lg transition inline-flex items-center gap-2"
          >
            Get Started Free <ArrowRight size={20} />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-blue-500/10 mt-20 py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h4 className="font-bold mb-4">BankShield AI</h4>
              <p className="text-gray-400 text-sm">AI-Powered Cyber Threat Correlation & Banking Risk Intelligence Platform</p>
            </div>
            <div>
              <h4 className="font-bold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><button onClick={() => navigate('/login')} className="hover:text-white transition">Dashboard</button></li>
                <li><a href="#" className="hover:text-white transition">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition">API Reference</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white transition">About</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Contact</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-blue-500/10 pt-8 text-center text-gray-500 text-sm">
            <p>&copy; 2024 BankShield AI. All rights reserved. Built for cybersecurity hackathons.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Landing
