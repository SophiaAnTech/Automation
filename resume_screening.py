# install this lib first: pip install pypdf google.genai openpyxl

import json
import os
from pypdf import PdfReader
import openpyxl
from google import genai
from pathlib import Path

RESUMES_FOLDER = Path("/users/abc/resumes")
OUTPUT_FILE    = "resume_summary.xlsx"
ROLE           = "Software Engineer"

# get an API key at aistudio.google.com and replace they key below
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "AIzsssCEL36-fcZdddB-HOvDKZJLSiUv-EzphoA"))

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text() + "\n"
    return text

def extract_info(resume_text):
    prompt = (
        "Extract info from this resume for a " + ROLE + " role. "
        "Return ONLY a JSON object with keys: name, years_of_experience, key_skills, education, previous_companies. "
        "Use comma-separated strings for key_skills and previous_companies. "
        "Use N/A if not found.\n\nResume:\n" + resume_text
    )

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    clean = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(clean)


pdf_files = list(RESUMES_FOLDER.glob("*.pdf"))
print("Found " + str(len(pdf_files)) + " resumes\n")

results = []
for pdf_path in pdf_files:
    print("Processing: " + pdf_path.name)
    info         = extract_info(extract_text(pdf_path))
    info["file"] = pdf_path.name
    results.append(info)

wb = openpyxl.Workbook()
ws = wb.active
ws.append(["File", "Name", "Years of Experience", "Key Skills", "Education", "Previous Companies"])

for result in results:
    ws.append([
        result.get("file"),
        result.get("name"),
        result.get("years_of_experience"),
        result.get("key_skills"),
        result.get("education"),
        result.get("previous_companies"),
    ])

wb.save(OUTPUT_FILE)
print("Saved to " + OUTPUT_FILE)
