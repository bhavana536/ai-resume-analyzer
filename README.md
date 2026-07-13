# AI Resume Analyzer 🤖

An AI-powered Resume Analyzer that provides ATS keyword matching, resume scoring, and actionable feedback using Google Gemini AI.

## 🔗 Live Demo
[https://ai-resume-analyzer-nine-swart.vercel.app](https://ai-resume-analyzer-nine-swart.vercel.app)

## ✨ Features
- 📄 Upload resume as PDF
- 🎯 ATS keyword matching against job descriptions
- 📊 Visual score circle with color coding
- 💪 Strengths and improvement suggestions
- ✅ Matching and missing keyword badges
- 🌙 Modern dark-themed dashboard UI

## 🛠️ Tech Stack
- **Frontend:** React.js, CSS
- **Backend:** Python, Flask, REST API
- **AI:** Google Gemini API (gemini-3.5-flash)
- **PDF Processing:** PyPDF2
- **Deployment:** Vercel (frontend) + Render (backend)

## 🚀 How It Works
1. Upload your resume PDF
2. Optionally paste a job description for ATS matching
3. Click Analyze Resume
4. Get instant AI-powered feedback with score, strengths, improvements and keyword matching

## 📁 Project Structure
ai-resume-analyzer/
├── backend/          # Flask API + Gemini AI integration
│   ├── app.py
│   ├── requirements.txt
│   └── Procfile
├── frontend/         # React.js UI
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── README.md
