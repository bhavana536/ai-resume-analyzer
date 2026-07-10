from flask import Flask,request,jsonify
from flask_cors import CORS 
import google.generativeai as genai 
import PyPDF2
import io 
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) 
CORS(app, origins=["https://ai-resume-analyzer-nine-swart.vercel.app", "http://localhost:3000"])

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-8b")

@app.route('/')
def home():
    return jsonify({"message":"AI Resume Analyzer Backend is running!"})

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        # Read PDF
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Build prompt
        if job_description.strip():
            prompt = f"""
            You are an expert HR recruiter and ATS specialist.
            Compare this resume against the given job description.

            SCORING RUBRIC (Total: 100 points):
            - Keyword Match (40 points)
            - Experience Relevance (30 points)
            - Skills Match (20 points)
            - Formatting & ATS-Friendliness (10 points)

            JOB DESCRIPTION:
            {job_description}

            RESUME:
            {text}

            Reply in this EXACT format:
            SCORE: (number)
            MATCH_PERCENTAGE: (number)
            MATCHING_KEYWORDS:
            - keyword 1
            MISSING_KEYWORDS:
            - keyword 1
            STRENGTHS:
            - point 1
            IMPROVEMENTS:
            - point 1
            """
        else:
            prompt = f"""
            You are an expert HR recruiter. Analyze this resume.

            SCORING RUBRIC (Total: 100 points):
            - Contact Information (5 points)
            - Professional Summary (10 points)
            - Work Experience (30 points)
            - Skills Section (15 points)
            - Education (10 points)
            - Projects (15 points)
            - Formatting (15 points)

            Resume:
            {text}

            Reply in this EXACT format:
            SCORE: (number)
            STRENGTHS:
            - point 1
            """
        response = model.generate_content(prompt)
        
        return jsonify({
            "analysis": response.text,
            "resume_text": text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500        
if __name__ == '__main__':
    app.run(debug=True)