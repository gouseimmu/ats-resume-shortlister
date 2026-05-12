import os
import re
import docx
import pdfplumber

# -------------------------------
# Function to clean text
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# -------------------------------
# Read DOCX file
# -------------------------------
def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


# -------------------------------
# Read PDF file
# -------------------------------
def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# -------------------------------
# Score Resume
# -------------------------------
def score_resume(resume_text, role_data):
    resume_text = clean_text(resume_text)

    score = 0
    details = {}

    # Skill Match (30 marks)
    matched_skills = []
    for skill in role_data["required_skills"]:
        if skill.lower() in resume_text:
            matched_skills.append(skill)

    skill_score = (len(matched_skills) / len(role_data["required_skills"])) * 30 if role_data["required_skills"] else 0
    score += skill_score
    details["Skill Match"] = round(skill_score, 2)

    # Responsibilities Match (25 marks)
    matched_resp = []
    for resp in role_data["responsibilities"]:
        if resp.lower() in resume_text:
            matched_resp.append(resp)

    resp_score = (len(matched_resp) / len(role_data["responsibilities"])) * 25 if role_data["responsibilities"] else 0
    score += resp_score
    details["Responsibilities Match"] = round(resp_score, 2)

    # Project Keywords Match (20 marks)
    matched_projects = []
    for keyword in role_data["project_keywords"]:
        if keyword.lower() in resume_text:
            matched_projects.append(keyword)

    project_score = (len(matched_projects) / len(role_data["project_keywords"])) * 20 if role_data["project_keywords"] else 0
    score += project_score
    details["Project Match"] = round(project_score, 2)

    # Tools Match (10 marks)
    matched_tools = []
    for tool in role_data["tools"]:
        if tool.lower() in resume_text:
            matched_tools.append(tool)

    tool_score = (len(matched_tools) / len(role_data["tools"])) * 10 if role_data["tools"] else 0
    score += tool_score
    details["Tools Match"] = round(tool_score, 2)

    # Certifications Match (5 marks)
    matched_certs = []
    for cert in role_data["certifications"]:
        if cert.lower() in resume_text:
            matched_certs.append(cert)

    cert_score = (len(matched_certs) / len(role_data["certifications"])) * 5 if role_data["certifications"] else 0
    score += cert_score
    details["Certifications"] = round(cert_score, 2)

    # Resume Quality (10 marks)
    quality_score = 0
    if len(resume_text.split()) > 200:
        quality_score += 5
    if "experience" in resume_text and "education" in resume_text:
        quality_score += 5

    score += quality_score
    details["Resume Quality"] = round(quality_score, 2)

    return round(score, 2), details, matched_skills


# -------------------------------
# Load Resumes from Folder
# -------------------------------
def load_resumes_from_folder(folder_path):
    resumes = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.lower().endswith(".pdf"):
            text = read_pdf(file_path)
            resumes.append((file_name, text))

        elif file_name.lower().endswith(".docx"):
            text = read_docx(file_path)
            resumes.append((file_name, text))

    return resumes


# -------------------------------
# Main Program
# -------------------------------
def main():
    print("\n===== AUTO RESUME SCORING SYSTEM (PDF/DOCX) =====\n")

    role_name = input("Enter Job Role Name: ")

    responsibilities = input("\nEnter Responsibilities (comma separated): ").split(",")
    required_skills = input("\nEnter Required Skills (comma separated): ").split(",")
    project_keywords = input("\nEnter Project Keywords (comma separated): ").split(",")
    tools = input("\nEnter Tools/Technologies (comma separated): ").split(",")
    certifications = input("\nEnter Certifications (comma separated, optional): ").split(",")

    responsibilities = [r.strip() for r in responsibilities if r.strip()]
    required_skills = [s.strip() for s in required_skills if s.strip()]
    project_keywords = [p.strip() for p in project_keywords if p.strip()]
    tools = [t.strip() for t in tools if t.strip()]
    certifications = [c.strip() for c in certifications if c.strip()]

    role_data = {
        "role": role_name,
        "responsibilities": responsibilities,
        "required_skills": required_skills,
        "project_keywords": project_keywords,
        "tools": tools,
        "certifications": certifications
    }

    folder_path = input("\nEnter folder path where resumes are stored: ")

    if not os.path.exists(folder_path):
        print("❌ Folder not found. Please check the path.")
        return

    resumes = load_resumes_from_folder(folder_path)

    if len(resumes) == 0:
        print("❌ No PDF/DOCX resumes found in folder.")
        return

    results = []

    for file_name, resume_text in resumes:
        score, details, matched_skills = score_resume(resume_text, role_data)
        results.append((file_name, score, details, matched_skills))

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n\n===== FINAL RESULTS =====")
    print(f"\nRole: {role_name}\n")

    for rank, (file_name, score, details, matched_skills) in enumerate(results, start=1):
        print(f"\n🏆 Rank {rank} -> {file_name}")
        print(f"Score: {score}/100")
        print("Breakdown:", details)
        print("Matched Skills:", matched_skills)

    print("\n===== END =====\n")


if __name__ == "__main__":
    main()