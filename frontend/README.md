# 🚀 AIWAR – Meeting War Room

> **Status:** ✅ Version 1 Complete

Enterprise Multi-Agent AI platform that analyzes meeting transcripts using specialized AI agents, Machine Learning, and Historical Intelligence to generate executive-ready insights and project risk assessments.

---

## 📌 Project Overview

AIWAR (AI War Room) is an AI-powered meeting intelligence platform built using a **Multi-Agent AI architecture**. Instead of relying on a single LLM response, the system orchestrates multiple AI agents specializing in **Product, Engineering, Finance, Risk, and Executive Coordination** to analyze meeting transcripts from different business perspectives.

The platform combines AI-generated insights with a Machine Learning risk prediction model and Historical Intelligence to produce comprehensive executive reports, identify recurring project blockers, and support data-driven decision-making.

---

## ✨ Features

- 🤖 Multi-Agent AI Workflow using LangGraph
- 🧠 Product, Engineering, Finance & Risk AI Agents
- 📊 Machine Learning Risk Prediction
- 📈 Historical Intelligence using MongoDB
- 🤝 Consensus-Based Decision Engine
- 📄 Executive PDF Report Generation
- 📚 Meeting History Dashboard
- 📤 PDF/TXT File Upload Support
- 📝 Manual Transcript Analysis
- ☁️ Cloud Deployment (Vercel + Railway)

---

## 🏗️ AI Pipeline

```text
Meeting Transcript
        │
        ▼
 Product Agent
        │
        ▼
 Engineering Agent
        │
        ▼
 Finance Agent
        │
        ▼
 Risk Agent
        │
        ▼
 Machine Learning Risk Prediction
        │
        ▼
 Consensus Engine
        │
        ▼
 Historical Intelligence
        │
        ▼
 Coordinator Agent
        │
        ▼
 Executive Report
        │
        ▼
 Dashboard & PDF
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Frontend | Next.js 16, React, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, Pydantic |
| AI Orchestration | LangGraph |
| LLM | Google Gemini API |
| Machine Learning | Scikit-learn, Decision Tree Classifier |
| Database | MongoDB Atlas |
| PDF Generation | ReportLab |
| Deployment | Vercel, Railway |

---

## 🧠 Multi-Agent Architecture

| Agent | Responsibility |
|--------|---------------|
| Product Agent | Product analysis, action items, delivery risks |
| Engineering Agent | Technical blockers, API issues, infrastructure |
| Finance Agent | Budget analysis and financial risks |
| Risk Agent | Timeline, dependency and operational risks |
| Coordinator Agent | Executive summary, final decision and priority actions |

---

## 📊 Core Capabilities

- Multi-Agent AI Decision Making
- Machine Learning Risk Prediction
- Consensus-Based Analysis
- Historical Project Intelligence
- Executive Report Generation
- Meeting History Tracking
- Cloud Deployment

---

## 📁 Project Structure

```text
AIWAR
│
├── frontend
│   ├── app
│   ├── components
│   └── public
│
├── backend
│   ├── agents
│   ├── api
│   ├── db
│   ├── graph
│   ├── ml
│   ├── services
│   ├── utils
│   └── main.py
│
└── README.md
```

---

## 🚀 Installation

### Backend

```bash
cd backend
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables

### Backend (.env)

```env
GEMINI_API_KEY=YOUR_API_KEY
MONGODB_URI=YOUR_MONGODB_URI
DATABASE_NAME=meeting_war_room
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## 🔗 API Endpoints

| Method | Endpoint |
|---------|----------|
| GET | `/api/health` |
| POST | `/api/analyze` |
| POST | `/api/analyze-upload` |
| GET | `/api/dashboard` |
| GET | `/api/meetings` |
| GET | `/api/meetings/{meeting_id}` |
| DELETE | `/api/meetings/{meeting_id}` |
| POST | `/api/report/pdf` |

---

## 🔮 Future Improvements

- Retrieval-Augmented Generation (RAG)
- Microsoft Teams Integration
- Slack Integration
- Zoom Integration
- Authentication & Role-Based Access
- Docker Support
- CI/CD Pipeline
- LLM Monitoring & Evaluation

---

## 👨‍💻 Author

**Vishal Nagare**  
B.Tech Computer Science & Engineering  
MIT World Peace University, Pune

---

## 📄 License

This project was developed for educational, research, and portfolio purposes.