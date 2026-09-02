import xgboost as xgb

from backend.intent_engine import extract_intent
from backend.policy_engine import evaluate_payment


MODEL_PATH = "models/intentguard_xgb.json"


# ==========================================
# LOAD ML MODEL
# ==========================================

model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)


# ==========================================
# ML RISK SCORE
# ==========================================

def calculate_ml_risk(payment):

    features = [[
        payment.get("budget", 60000),
        payment.get("amount", 0),
        payment.get("category_match", 1),
        payment.get("quantity_match", 1),
        payment.get("time_match", 1),
        payment.get("merchant_trust", 1.0),
        payment.get("historical_success", 1.0),
        payment.get("previous_violations", 0),
        payment.get("intent_similarity", 1.0)
    ]]

    authorization_probability = model.predict_proba(
        features
    )[0][1]

    ml_risk = 1.0 - authorization_probability

    return float(ml_risk)


# ==========================================
# POLICY-AWARE RISK ENGINE
# ==========================================

def calculate_final_risk(payment, policy_result, ml_risk):

    violations = policy_result.get("violations", [])
    warnings = policy_result.get("warnings", [])

    # --------------------------------------
    # HARD BLOCK
    # --------------------------------------
    # A hard policy violation must dominate
    # the ML prediction.
    
    if violations:

        risk_score = 0.95

        # Multiple violations = even higher risk
        if len(violations) >= 2:
            risk_score = 0.99

        return risk_score


    # --------------------------------------
    # WARNINGS
    # --------------------------------------

    risk_score = ml_risk

    merchant_trust = payment.get(
        "merchant_trust",
        1.0
    )

    intent_similarity = payment.get(
        "intent_similarity",
        1.0
    )

    previous_violations = payment.get(
        "previous_violations",
        0
    )

    # Suspicious merchant
    if merchant_trust < 0.50:
        risk_score = max(
            risk_score,
            0.70
        )

    # Intent drift
    if intent_similarity < 0.60:
        risk_score = max(
            risk_score,
            0.75
        )

    # Previous bad history
    if previous_violations > 0:
        risk_score = max(
            risk_score,
            0.65
        )

    # --------------------------------------
    # NORMAL SAFE PAYMENT
    # --------------------------------------

    if not warnings and risk_score < 0.50:
        risk_score = min(
            risk_score,
            0.20
        )

    return float(risk_score)


# ==========================================
# COMPLETE INTENTGUARD PIPELINE
# ==========================================

def protect_payment(
    user_request,
    payment
):

    # --------------------------------------
    # STEP 1 — EXTRACT USER INTENT
    # --------------------------------------

    intent = extract_intent(
        user_request
    )

    # --------------------------------------
    # DERIVED FEATURES
    # --------------------------------------

    payment["budget"] = (
        intent.get("max_amount")
        or 60000
    )

    requested_category = str(
        intent.get("category", "")
    ).lower()

    proposed_category = str(
        payment.get("category", "")
    ).lower()

    payment["category_match"] = int(
        requested_category != ""
        and requested_category == proposed_category
    )

    requested_quantity = intent.get(
        "quantity",
        1
    )

    proposed_quantity = payment.get(
        "quantity",
        1
    )

    payment["quantity_match"] = int(
        proposed_quantity <= requested_quantity
    )

    # --------------------------------------
    # STEP 2 — HARD POLICY CHECKS
    # --------------------------------------

    policy_result = evaluate_payment(
        intent,
        payment
    )

    # --------------------------------------
    # STEP 3 — ML RISK
    # --------------------------------------

    ml_risk = calculate_ml_risk(
        payment
    )

    # --------------------------------------
    # STEP 4 — FINAL RISK
    # --------------------------------------

    risk_score = calculate_final_risk(
        payment,
        policy_result,
        ml_risk
    )

    # --------------------------------------
    # STEP 5 — FINAL DECISION
    # --------------------------------------

    policy_decision = policy_result[
        "decision"
    ]

    if policy_decision == "BLOCK":

        final_decision = "BLOCK"

    elif policy_decision == "REVIEW":

        final_decision = "REVIEW"

    else:

        if risk_score < 0.50:
            final_decision = "ALLOW"
        else:
            final_decision = "REVIEW"

    # --------------------------------------
    # RETURN COMPLETE RESULT
    # --------------------------------------

    return {

        "decision":
            final_decision,

        "risk_score":
            round(risk_score, 4),

        "ml_risk_score":
            round(ml_risk, 4),

        "intent":
            intent,

        "payment":
            payment,

        "policy":
            policy_result
    }


# ==========================================
# DEMO
# ==========================================

if __name__ == "__main__":

    user_request = (
        "Buy me a laptop under ₹60000"
    )

    payment = {

        "category":
            "laptop",

        "amount":
            55000,

        "quantity":
            1,

        "merchant_trust":
            0.90,

        "historical_success":
            0.95,

        "previous_violations":
            0,

        "intent_similarity":
            0.40,

        "time_match":
            1
    }

    result = protect_payment(
        user_request,
        payment
    )

    print("\n")
    print("===================================")
    print("        🛡️ INTENTGUARD")
    print("===================================")

    print(
        f"\nDecision: {result['decision']}"
    )

    print(
        f"Risk Score: {result['risk_score']}"
    )

    print(
        f"ML Risk Score: {result['ml_risk_score']}"
    )

    print("\nUser Intent:")
    print(result["intent"])

    print("\nPolicy Result:")
    print(result["policy"])

    print("\n===================================")