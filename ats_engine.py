from utils import clean_text, extract_experience


def score_resume(resume_text, jd_text, skills, required_exp):

    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    matched = [
        skill for skill in skills
        if skill in resume_text
    ]

    missing = [
        skill for skill in skills
        if skill not in resume_text
    ]

    # Skill Score
    skill_score = (
        len(matched) / len(skills)
    ) * 60 if skills else 0

    # JD Similarity
    jd_words = set(jd_text.split())
    resume_words = set(resume_text.split())

    similarity_score = (
        len(jd_words & resume_words) / len(jd_words)
    ) * 20 if jd_words else 0

    # Experience
    resume_exp = extract_experience(resume_text)

    if required_exp == 0:
        exp_score = 20
    else:
        exp_score = min(
            (resume_exp / required_exp) * 20,
            20
        )

    # Final Score
    final_score = round(
        skill_score + similarity_score + exp_score,
        2
    )

    # Skill Match %
    skill_match_percent = round(
        (len(matched) / len(skills)) * 100,
        0
    ) if skills else 0

    # Eligibility
    if final_score >= 75 and resume_exp >= required_exp:

        eligibility = "Eligible"
        recommendation = "Shortlist"

    elif final_score >= 60:

        eligibility = "Consider"
        recommendation = "Review"

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
        "recommendation": recommendation
    }