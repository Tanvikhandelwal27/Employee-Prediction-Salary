async function predictSalary() {
  const experience = parseInt(document.getElementById('experience').value);
  const education = document.getElementById('education').value;
  const role = document.getElementById('job_role').value;

  // Validate input
  if (isNaN(experience) || !education || !role) {
    document.getElementById('result').innerText = "❗Please fill all fields properly.";
    return;
  }

  const data = {
    experience: experience,
    education_level: education,  // ✅ use exact key backend expects
    role: role                   // ✅ use exact key backend expects
  };

  try {
    const res = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok && result.predicted_salary) {
      document.getElementById('result').innerText = `💰 Predicted Salary: ₹${result.predicted_salary}`;
    } else {
      document.getElementById('result').innerText = "❌ Prediction failed.";
      console.error("Prediction Error Response:", result);
    }
  } catch (error) {
    console.error("Error calling /predict API:", error);
    document.getElementById('result').innerText = "❌ Server error. Please try again.";
  }
}
