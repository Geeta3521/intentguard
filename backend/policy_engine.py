from typing import Dict, Any


def evaluate_payment(
    intent: Dict[str, Any],
    payment: Dict[str, Any]
) -> Dict[str, Any]:

    violations = []
    warnings = []
    checks = {}

    # =========================================
    # 1. BUDGET CHECK
    # =========================================

    max_amount = intent.get("max_amount")
    payment_amount = payment.get("amount")

    if max_amount is not None and payment_amount is not None:

        budget_ok = payment_amount <= max_amount

        checks["budget"] = {
            "passed": budget_ok,
            "requested_limit": max_amount,
            "payment_amount": payment_amount
        }

        if not budget_ok:

            violations.append(
                "Payment exceeds the user's maximum budget."
            )

    # =========================================
    # 2. CATEGORY CHECK
    # =========================================

    requested_category = intent.get("category")
    payment_category = payment.get("category")

    if requested_category and payment_category:

        category_ok = (
            requested_category.lower()
            == payment_category.lower()
        )

        checks["category"] = {
            "passed": category_ok,
            "requested": requested_category,
            "proposed": payment_category
        }

        if not category_ok:

            violations.append(
                "Payment category does not match "
                "the user's requested category."
            )

    # =========================================
    # 3. QUANTITY CHECK
    # =========================================

    requested_quantity = intent.get(
        "quantity",
        1
    )

    payment_quantity = payment.get(
        "quantity",
        1
    )

    quantity_ok = (
        payment_quantity <= requested_quantity
    )

    checks["quantity"] = {
        "passed": quantity_ok,
        "requested": requested_quantity,
        "proposed": payment_quantity
    }

    if not quantity_ok:

        violations.append(
            "Payment quantity exceeds "
            "the user's requested quantity."
        )

    # =========================================
    # 4. MERCHANT TRUST
    # =========================================

    merchant_trust = payment.get(
        "merchant_trust",
        1.0
    )

    checks["merchant_trust"] = {
        "score": merchant_trust
    }

    if merchant_trust < 0.5:

        warnings.append(
            "Merchant trust score is low."
        )

    # =========================================
    # 5. INTENT SIMILARITY
    # =========================================

    intent_similarity = payment.get(
        "intent_similarity",
        1.0
    )

    checks["intent_similarity"] = {
        "score": intent_similarity
    }

    if intent_similarity < 0.7:

        warnings.append(
            "Payment has low similarity "
            "to the user's original intent."
        )

    # =========================================
    # 6. FINAL DECISION
    # =========================================

    if len(violations) > 0:

        decision = "BLOCK"

    elif len(warnings) > 0:

        decision = "REVIEW"

    else:

        decision = "ALLOW"

    return {

        "decision": decision,

        "checks": checks,

        "warnings": warnings,

        "violations": violations
    }


# ============================================
# DEMONSTRATION
# ============================================

if __name__ == "__main__":

    user_intent = {

        "raw_request":
            "Buy me a laptop under ₹60000",

        "category":
            "laptop",

        "max_amount":
            60000,

        "currency":
            "INR",

        "quantity":
            1
    }

    # =========================================
    # TEST 1 — SAFE
    # =========================================

    safe_payment = {

        "category":
            "laptop",

        "amount":
            55000,

        "quantity":
            1,

        "merchant_trust":
            0.95,

        "intent_similarity":
            0.96
    }

    result = evaluate_payment(
        user_intent,
        safe_payment
    )

    print("\n==============================")
    print("TEST 1 — SAFE")
    print("==============================")

    print(result)

    # =========================================
    # TEST 2 — BUDGET ATTACK
    # =========================================

    budget_attack = {

        "category":
            "laptop",

        "amount":
            68500,

        "quantity":
            1,

        "merchant_trust":
            0.95,

        "intent_similarity":
            0.90
    }

    result = evaluate_payment(
        user_intent,
        budget_attack
    )

    print("\n==============================")
    print("TEST 2 — BUDGET ATTACK")
    print("==============================")

    print(result)

    # =========================================
    # TEST 3 — SUSPICIOUS MERCHANT
    # =========================================

    suspicious_merchant = {

        "category":
            "laptop",

        "amount":
            58000,

        "quantity":
            1,

        "merchant_trust":
            0.35,

        "intent_similarity":
            0.92
    }

    result = evaluate_payment(
        user_intent,
        suspicious_merchant
    )

    print("\n==============================")
    print("TEST 3 — SUSPICIOUS MERCHANT")
    print("==============================")

    print(result)

    # =========================================
    # TEST 4 — INTENT DRIFT
    # =========================================

    intent_drift = {

        "category":
            "laptop",

        "amount":
            55000,

        "quantity":
            1,

        "merchant_trust":
            0.90,

        "intent_similarity":
            0.45
    }

    result = evaluate_payment(
        user_intent,
        intent_drift
    )

    print("\n==============================")
    print("TEST 4 — INTENT DRIFT")
    print("==============================")

    print(result)