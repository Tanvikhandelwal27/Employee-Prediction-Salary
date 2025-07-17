from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.linear_model import LinearRegression
import pickle
import os
import re
import PyPDF2

app = Flask(__name__)
CORS(app)

# Load trained model
model = pickle.load(open('model.pkl', 'rb'))

# Helper: Extract data from resume text
def extract_resume_data(text):
    # Experience
    exp_match = re.search(r'(\d+)\s+years?', text, re.I)
    experience = int(exp_match.group(1)) if exp_match else 0

    # Education
    if re.search(r"(master'?s|post[- ]?graduate)", text, re.I):
        education = "Master's"
    elif re.search(r"bachelor'?s", text, re.I):
        education = "Bachelor's"
    else:
        education = "Other"

    # Role
    if "software engineer" in text.lower():
        role = "Software Engineer"
    elif "data scientist" in text.lower():
        role = "Data Scientist"
    elif "product manager" in text.lower():
        role = "Product Manager"
    else:
        role = "Other"

    return experience, education, role

# Helper: Read text from uploaded PDF resume
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.route('/predict', methods=['POST'])
def predict_salary():
    # Get user-selected fields
    role = request.form.get('role')
    education = request.form.get('education')
    experience = int(request.form.get('experience'))
    
    # Resume uploaded
    resume_file = request.files.get('resume')
    extracted_info = {}

    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        exp, edu, detected_role = extract_resume_data(resume_text)
        extracted_info = {
            "experience": f"{exp} years",
            "education": edu,
            "role": detected_role
        }

        # Override manual fields with extracted ones
        experience = exp
        education = edu
        role = detected_role

    # Encode inputs
    education_map = {"Bachelor's": 0, "Master's": 1, "Other": 2}
    role_map = {"Software Engineer": 0, "Data Scientist": 1, "Product Manager": 2, "Other": 3}

    education_encoded = education_map.get(education, 2)
    role_encoded = role_map.get(role, 3)

    features = [[experience, education_encoded, role_encoded]]
    predicted_salary = model.predict(features)[0]

    return jsonify({
        "predicted_salary": round(predicted_salary, 2),
        "extracted_info": extracted_info
    })

if __name__ == '__main__':
    app.run(debug=True)
