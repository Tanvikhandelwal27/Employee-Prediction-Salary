from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

# ✅ Load trained model
model = joblib.load("model.pkl")  # Make sure this is correct path

# ✅ Role and Education mappings
role_mapping = {
    1: 0,  # Software Engineer
    2: 1,  # Data Scientist
    3: 2,  # Manager
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,
    9: 8,
    10: 9
}

edu_mapping = {
    1: 0,  # Bachelor
    2: 1,  # Master
    3: 2   # PhD
}


# 📄 Extract text from resume
def extract_text_from_file(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# 📊 Extract experience (years)
def extract_experience(text):
    match = re.search(r'(\d+)\s+years?\s+(?:of\s+)?experience', text, re.IGNORECASE)
    return int(match.group(1)) if match else 2

# 🎓 Extract education level
def extract_education_level(text):
    text = text.lower()
    if "phd" in text:
        return 3
    elif "master" in text or "m.tech" in text:
        return 2
    elif "bachelor" in text or "b.tech" in text:
        return 1
    return 1

# 💼 Extract role
def extract_role(text):
    text = text.lower()
    if "data scientist" in text:
        return 2
    elif "manager" in text:
        return 3
    elif "software engineer" in text or "developer" in text:
        return 1
    return 1

# 🎯 Salary Prediction API
# 🎯 Updated Salary Prediction API – Requires Resume
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # ✅ Check if resume is uploaded
        resume_file = request.files.get("resume")
        if not resume_file:
            return jsonify({"error": "Please upload resume for prediction"}), 400

        # 📄 Extract text from resume
        text = extract_text_from_file(resume_file)

        # 🧠 Extract fields
        experience = extract_experience(text)
        education_level = extract_education_level(text)
        role = extract_role(text)

        # 🔄 Map values using mapping
        exp = float(experience)
        edu = int(edu_mapping[education_level])
        role = int(role_mapping[role])

        # 🔢 Predict salary
        prediction = model.predict([[exp, role, edu]])
        return jsonify({"predicted_salary": round(float(prediction[0]), 2)})

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 400



# 📎 Resume Upload & Field Extraction
@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    file = request.files["resume"]
    text = extract_text_from_file(file)

    experience = extract_experience(text)
    education = extract_education_level(text)
    role = extract_role(text)

    print("Extracted:", experience, education, role)

    return jsonify({
        "experience": experience,
        "education_level": education,
        "role": role
    })

# 🚀 Run app
if __name__ == "__main__":
    app.run(debug=True)
