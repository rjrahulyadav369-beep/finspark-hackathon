# BankShield AI

**AI-Powered Cyber Threat Correlation & Banking Risk Intelligence Platform**

An enterprise-grade cybersecurity dashboard that intelligently correlates banking security events and detects suspicious behavior before fraud happens.

## 🎯 Project Overview

Banks receive thousands of security events every second. BankShield AI correlates these events intelligently and generates actionable risk intelligence:

- **Risk Score** - Quantified threat level (0-100)
- **Threat Category** - Classification of suspicious behavior
- **Confidence Score** - Model confidence percentage
- **Human-readable Explanation** - Why the event is flagged
- **Recommended Action** - Next steps for SOC team

## 🏗️ Architecture

```
BankShield AI/
├── frontend/              # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── assets/
│   │   └── utils/
│   └── package.json
├── backend/               # Python FastAPI
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## 🚀 Tech Stack

### Frontend
- React 18+
- Vite
- TypeScript
- Tailwind CSS
- Plotly & Chart.js for visualization

### Backend
- Python FastAPI
- Scikit-learn (Random Forest, Isolation Forest)
- SQLite
- Pydantic for validation

### ML/AI
- Random Forest for classification
- Isolation Forest for anomaly detection
- Feature engineering & preprocessing

### Deployment
- Docker & Docker Compose
- GitHub Ready

## 📋 Features

✅ **Intelligent Event Correlation** - Correlates 10+ event types
✅ **Real-time Risk Scoring** - ML-powered threat detection
✅ **Beautiful Dashboard** - Professional cybersecurity SOC interface
✅ **CSV Import** - Bulk upload banking logs
✅ **Event Analytics** - Searchable, sortable event table
✅ **User Profiles** - Transaction & behavior history
✅ **Alert Center** - Manage security alerts
✅ **AI Chat Assistant** - Ask questions about flagged accounts
✅ **PDF Reports** - Generate compliance reports
✅ **Dark Mode** - Modern glassmorphism design

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 16+
- Python 3.9+
- Docker & Docker Compose (optional)

### Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/rjrahulyadav369-beep/finspark-hackathon.git
cd finspark-hackathon
```

**2. Setup Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

Backend runs on `http://localhost:8000`

**3. Setup Frontend**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

**4. Using Docker (Recommended)**
```bash
docker-compose up --build
```

## 🔑 Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | POST | User authentication |
| `/auth/register` | POST | User registration |
| `/api/upload` | POST | Upload CSV banking logs |
| `/api/events` | GET | Fetch all events with filters |
| `/api/predict` | POST | Get risk prediction for event |
| `/api/users/{id}` | GET | User profile & history |
| `/api/dashboard` | GET | Dashboard statistics |
| `/api/alerts` | GET | Fetch security alerts |
| `/api/chat` | POST | AI chat assistant |
| `/api/reports/pdf` | POST | Generate PDF report |

## 📊 Event Types Supported

The platform correlates these banking security events:

1. **Login** - User authentication
2. **Failed Login** - Authentication failures
3. **OTP Failure** - Invalid OTP attempts
4. **Device Change** - New device detected
5. **IP Address Change** - Different IP address
6. **Geo-location Change** - Location mismatch
7. **Large Transaction** - Unusual transaction amount
8. **ATM Withdrawal** - Cash withdrawal
9. **Password Reset** - Account credential change
10. **Beneficiary Added** - New payment recipient

## 🤖 AI Engine

### Risk Scoring Algorithm
```
Risk Score = (
    device_risk * 0.2 +
    location_risk * 0.2 +
    transaction_risk * 0.25 +
    velocity_risk * 0.2 +
    auth_risk * 0.15
)
```

### Risk Levels
- **0-20**: Safe
- **21-40**: Low Risk
- **41-60**: Medium Risk
- **61-80**: High Risk
- **81-100**: Critical

## 🎨 UI/UX Design

- **Theme**: Dark Mode with Glassmorphism
- **Colors**: Black, Deep Navy, Blue Neon, Purple Glow
- **Components**: Rounded cards, soft shadows, smooth animations
- **Typography**: Professional banking-grade fonts
- **Responsiveness**: Mobile to desktop

## 📈 Dashboard Features

- **KPI Cards**: Total events, critical alerts, risk score
- **Threat Timeline**: Visual event history
- **Live Event Feed**: Real-time event stream
- **Risk Distribution**: Pie chart of threat levels
- **Top Suspicious Users**: Heat map of risky accounts
- **Event Table**: Searchable, sortable, paginated

## 📁 CSV Import Format

```csv
timestamp,user_id,event_type,transaction_amount,device_id,location,ip_address,otp_attempts
2024-01-15 10:30:00,USR001,login,0,DEV001,New York,192.168.1.1,0
2024-01-15 10:31:00,USR001,transaction,5000,DEV001,New York,192.168.1.1,0
2024-01-15 10:35:00,USR001,device_change,0,DEV002,Mumbai,203.0.113.5,3
```

## 🔐 Security Features

✅ JWT-based authentication
✅ Password hashing with bcrypt
✅ CORS protection
✅ Input validation & sanitization
✅ SQL injection prevention
✅ Rate limiting on API endpoints

## 📊 Model Evaluation

The ML models are evaluated using:
- **Accuracy Score**
- **Precision & Recall**
- **ROC-AUC Score**
- **Confusion Matrix**
- **Feature Importance**

Models are saved in `backend/models/` for production use.

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### GitHub Pages (Frontend)
```bash
cd frontend
npm run build
# Deploy dist/ folder to GitHub Pages
```

### Python Backend Deployment
- **Heroku**, **Railway**, or **Render** (supports FastAPI)
- **AWS EC2**, **Google Cloud Run**, **Azure App Service**

## 📚 Documentation

- [Frontend Setup](./frontend/README.md)
- [Backend Setup](./backend/README.md)
- [API Documentation](./backend/API.md)
- [ML Model Guide](./backend/ML_GUIDE.md)

## 🤝 Contributing

1. Create a feature branch
2. Commit changes
3. Push to GitHub
4. Create Pull Request

## 📝 License

MIT License - See LICENSE file

## 👨‍💻 Authors & Team

**Team Members:**
- **Rahul Yadav** - Full Stack Development & AI/ML
- **Tanmay Choudhary** - Backend Development & Data Science

## 🏆 Hackathon Ready

This project is designed to win national-level cybersecurity hackathons with:
- Production-grade code quality
- Comprehensive documentation
- Beautiful UI/UX
- Intelligent AI engine
- Full Docker support

---

**Built with ❤️ for Banking Security**
