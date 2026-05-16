from utils import clean_text, extract_experience


def score_resume(resume_text, jd_text, skills, required_exp):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    normalized_skills = [clean_text(skill).strip() for skill in skills if skill]

    matched = [skill for skill in normalized_skills if skill and skill in resume_clean]
    missing = [skill for skill in normalized_skills if skill and skill not in resume_clean]

    skill_match_percent = round((len(matched) / len(normalized_skills)) * 100, 0) if normalized_skills else 0
    skill_score = skill_match_percent * 0.55

    jd_words = set(word for word in jd_clean.split() if len(word) > 2)
    resume_words = set(word for word in resume_clean.split() if len(word) > 2)
    similarity = (len(jd_words & resume_words) / len(jd_words)) * 100 if jd_words else 0
    similarity_score = similarity * 0.2

    resume_exp = extract_experience(resume_text)
    required = required_exp[0] if isinstance(required_exp, (tuple, list)) else required_exp
    if not required:
        exp_score = 20
    else:
        exp_score = min(resume_exp / required, 1) * 20

    keyword_density = min(len(resume_words & set(normalized_skills)) * 2, 5)
    final_score = round(min(skill_score + similarity_score + exp_score + keyword_density, 100), 2)

    if final_score >= 75 and skill_match_percent >= 60 and resume_exp >= required:
        eligibility = "Eligible"
        recommendation = "Shortlist"
    elif final_score >= 55 or skill_match_percent >= 45:
        eligibility = "Consider"
        recommendation = "Panel Review"
    else:
        eligibility = "Rejected"
        recommendation = "Reject"

    return {
        "score": final_score,
        "matched": matched,
        "missing": missing,
        "experience": resume_exp,
        "skill_match": skill_match_percent,
        "eligibility": eligibility,
        "recommendation": recommendation,
        "similarity": round(similarity, 1),
    }

