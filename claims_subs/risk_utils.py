def calculate_risk_score(age, risk_factors):
    score = 50
    if age > 60:
        score += 20
    if "smoking" in risk_factors:
        score += 30
    return score
