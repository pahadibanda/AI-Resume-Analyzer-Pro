from modules.resume_parser import extract_text
from modules.skill_extractor import extract_skills
from modules.match_score import calculate_match_score
from modules.resume_score import calculate_resume_score

# Resume text read
resume_text = extract_text("Resume/resume.pdf")

# Skills extract
resume_skills = extract_skills(resume_text)

# Resume Score
resume_score = calculate_resume_score(resume_skills)

# Example Job Skills
job_skills = [
    "Python",
    "SQL",
    "Power BI",
    "Excel",
    "Tableau",
    "Statistics"
]

# Match Score
match_score, matched, missing = calculate_match_score(
    resume_skills,
    job_skills
)

print("\n========== RESUME SCORE ==========")
print(f"Resume Score : {resume_score}/100")

print("\n========== AI JOB MATCH ==========")
print(f"Match Score : {match_score}%")

print("\nMatched Skills")
for skill in matched:
    print("✅", skill)

print("\nMissing Skills")
for skill in missing:
    print("❌", skill)