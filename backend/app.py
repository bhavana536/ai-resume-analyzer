from flask import Flask,request,jsonify
from flask_cors import CORS 
import google.generativeai as genai 
import PyPDF2
import io 
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) 
CORS(app)

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('/')
def home():
    return jsonify({"message":"AI Resume Analyzer Backend is running!"})

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Build prompt based on whether job description was provided
    if job_description.strip():
        prompt = f"""
        You are an expert HR recruiter and ATS (Applicant Tracking System) specialist.
        Compare this resume against the given job description.

        SCORING RUBRIC (Total: 100 points):
        - Keyword Match (40 points): How many important job description keywords appear in resume
        - Experience Relevance (30 points): How well experience aligns with job requirements
        - Skills Match (20 points): Technical/soft skills overlap
        - Formatting & ATS-Friendliness (10 points): Clean structure, readable

        JOB DESCRIPTION:
        {job_description}

        RESUME:
        {text}

        Reply in this EXACT format:
        SCORE: (number)
        MATCH_PERCENTAGE: (number)
        MATCHING_KEYWORDS:
        - keyword 1
        - keyword 2
        - keyword 3
        MISSING_KEYWORDS:
        - keyword 1
        - keyword 2
        - keyword 3
        STRENGTHS:
        - point 1
        - point 2
        - point 3
        IMPROVEMENTS:
        - point 1
        - point 2
        - point 3
        """
    else:
        prompt = f"""
        You are an expert HR recruiter and resume reviewer. Analyze this resume using the EXACT scoring rubric below.

        SCORING RUBRIC (Total: 100 points):
        - Contact Information (5 points): Has email, phone, LinkedIn
        - Professional Summary/Objective (10 points): Clear and relevant
        - Work Experience (30 points): Quantified achievements, action verbs, relevant roles
        - Skills Section (15 points): Relevant technical and soft skills listed
        - Education (10 points): Degree, institution, relevant coursework
        - Projects (15 points): Relevant projects with technologies used
        - Formatting & ATS-Friendliness (15 points): Clean structure, no graphics issues, readable

        Resume:
        {text}

        Reply in this EXACT format:
        SCORE: (number)
        STRENGTHS:
        - point 1
        - point 2
        - point 3
        IMPROVEMENTS:
        - point 1
        - point 2
        - point 3
        MISSING:
        - point 1
        """
    
    response = model.generate_content(prompt)
    
    return jsonify({
        "analysis": response.text,
        "resume_text": text
    })

if __name__ == '__main__':
    app.run(debug=True)