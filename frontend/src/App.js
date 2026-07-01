import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [sections, setSections] = useState(null);
  const [score, setScore] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const extractScore = (text) => {
    const match = text.match(/SCORE:\s*(\d+)/);
    return match ? parseInt(match[1]) : null;
  };

  // Parses Gemini's raw text into clean sections
  const parseAnalysis = (text) => {
    const sectionNames = ['MATCHING_KEYWORDS', 'MISSING_KEYWORDS', 'STRENGTHS', 'IMPROVEMENTS', 'MISSING'];
    const result = {};

    sectionNames.forEach((name, i) => {
      const nextNames = sectionNames.slice(i + 1).join('|');
      const pattern = new RegExp(
        `${name}:([\\s\\S]*?)(?=${nextNames ? nextNames + ':|' : ''}$)`,
        'i'
      );
      const match = text.match(pattern);
      if (match) {
        const points = match[1]
          .split('\n')
          .map(line => line.replace(/^[-*]\s*/, '').replace(/\*\*/g, '').trim())
          .filter(line => line.length > 0);
        result[name] = points;
      }
    });

    return result;
  };

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please select a resume PDF first!");
      return;
    }

    setLoading(true);
    setSections(null);
    setScore(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('https://ai-resume-analyzer-backend-fdfa.onrender.com/analyze', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setScore(extractScore(data.analysis));
      setSections(parseAnalysis(data.analysis));
    } catch (error) {
      setSections({ ERROR: ["Something went wrong: " + error.message] });
    }

    setLoading(false);
  };

  const getScoreColor = (s) => {
    if (s >= 80) return '#2ecc71';
    if (s >= 60) return '#f39c12';
    return '#e74c3c';
  };

  const sectionConfig = {
    MATCHING_KEYWORDS: { title: '✅ Matching Keywords', type: 'badges', color: '#2ecc71' },
    MISSING_KEYWORDS: { title: '⚠️ Missing Keywords', type: 'badges', color: '#e74c3c' },
    STRENGTHS: { title: '💪 Strengths', type: 'list', color: '#2ecc71' },
    IMPROVEMENTS: { title: '🔧 Areas to Improve', type: 'list', color: '#f39c12' },
    MISSING: { title: '📋 Missing Sections', type: 'list', color: '#e74c3c' },
  };

  return (
    <div className="App">
      <h1>AI Resume Analyzer</h1>
      <p>Upload your resume and get instant AI feedback</p>

      <div className="upload-section">
        <label htmlFor="resume-upload" className="custom-file-upload">
          📄 {file ? file.name : "Choose Resume PDF"}
        </label>
        <input
          id="resume-upload"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
      </div>

      <div className="job-section">
        <label>Job Description (Optional - for ATS matching)</label>
        <textarea
          placeholder="Paste the job description here to get keyword matching analysis..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          rows={6}
        />
      </div>

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {score !== null && (
        <div className="score-circle-container">
          <svg width="150" height="150" viewBox="0 0 150 150">
            <circle cx="75" cy="75" r="65" fill="none" stroke="#2a2e3f" strokeWidth="12" />
            <circle
              cx="75" cy="75" r="65" fill="none"
              stroke={getScoreColor(score)}
              strokeWidth="12"
              strokeDasharray={`${(score / 100) * 408} 408`}
              strokeLinecap="round"
              transform="rotate(-90 75 75)"
            />
            <text x="75" y="85" textAnchor="middle" fontSize="32" fontWeight="bold" fill="#ffffff">
              {score}
            </text>
          </svg>
          <p className="score-label">Resume Score</p>
        </div>
      )}

      {sections && Object.entries(sections).map(([key, points]) => {
        const config = sectionConfig[key] || { title: key, type: 'list', color: '#9094a6' };
        return (
          <div key={key} className="result-card">
            <h3 style={{ color: config.color }}>{config.title}</h3>
            {config.type === 'badges' ? (
              <div className="badge-container">
                {points.map((point, i) => (
                  <span key={i} className="badge" style={{ borderColor: config.color, color: config.color }}>
                    {point}
                  </span>
                ))}
              </div>
            ) : (
              <ul>
                {points.map((point, i) => <li key={i}>{point}</li>)}
              </ul>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default App;