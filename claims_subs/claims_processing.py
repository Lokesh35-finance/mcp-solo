import logging
from db_utils import fetch_policy, update_policy, log_audit
from risk_utils import calculate_risk_score

logger = logging.getLogger(__name__)

def process_claim(claim_id, policy_id, claim_amount):
    policy = fetch_policy(policy_id)
    if not policy:
        logger.error(f"Policy {policy_id} not found")
        return None

    risk = calculate_risk_score(policy["holder_age"], policy["risk_factors"])
    approved = validate_claim(claim_amount, risk)

    if approved:
        payout = calculate_payout(claim_amount, risk)
        update_policy(policy_id, {"status": "settled", "last_payout": payout})
        log_audit("CLAIM_APPROVED", {"claim_id": claim_id, "policy_id": policy_id, "amount": payout})
        return payout
    else:
        update_policy(policy_id, {"status": "rejected"})
        log_audit("CLAIM_REJECTED", {"claim_id": claim_id, "policy_id": policy_id})
        return 0

def validate_claim(claim_amount, risk_score):
    return not (risk_score > 70 and claim_amount > 50000)

def calculate_payout(amount, risk_score):
    base = amount * 0.8
    if risk_score < 30:
        return base * 1.1
    elif risk_score > 80:
        return base * 0.7
    return base

def configure_source_db():
    return {"host": "src-db", "port": 5432, "schema": "claims"}

def configure_target_db():
    return {"host": "tgt-db", "port": 5432, "schema": "analytics"}
