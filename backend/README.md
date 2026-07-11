# BankShield AI Backend

Python FastAPI backend for BankShield AI cybersecurity platform.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
python app/main.py
```

Server runs on `http://localhost:8000`

API docs: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user
- `POST /auth/logout` - Logout user

### Events
- `GET /api/events` - Get all events
- `GET /api/events/{id}` - Get event by ID
- `POST /api/events` - Create event
- `GET /api/events/user/{user_id}` - Get user events

### Predictions
- `POST /api/predict/event` - Predict single event
- `POST /api/predict/batch` - Predict batch events
- `GET /api/predict/model/info` - Get model info

### Dashboard
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/timeline` - Threat timeline
- `GET /api/dashboard/top-suspicious-users` - Top suspicious users
- `GET /api/dashboard/risk-distribution` - Risk distribution

### Users
- `GET /api/users/{id}` - Get user profile
- `GET /api/users/{id}/risk-profile` - User risk profile
- `GET /api/users/{id}/transaction-history` - Transaction history
- `GET /api/users/{id}/login-history` - Login history
- `GET /api/users/{id}/devices` - User devices

### Reports
- `GET /api/reports/summary` - Report summary
- `GET /api/reports/export-csv` - Export events to CSV

### Chat
- `POST /api/chat/ask` - Chat with AI
- `POST /api/chat/explain-alert` - Explain alert
