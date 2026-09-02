import random
import pandas as pd

random.seed(42)

categories = [
    "laptop",
    "smartphone",
    "headphones",
    "shoes",
    "hotel",
    "flight",
    "groceries",
    "books"
]

violation_types = [
    "budget_violation",
    "category_mismatch",
    "quantity_violation",
    "time_violation",
    "merchant_violation"
]

rows = []

for i in range(5000):

    category = random.choice(categories)

    budget = random.randint(1000, 100000)

    # 30% of transactions contain an intent violation
    violation = random.random() < 0.30

    if violation:

        violation_type = random.choice(violation_types)

        if violation_type == "budget_violation":

            amount = int(budget * random.uniform(1.05, 1.8))

            category_match = 1
            quantity_match = 1
            time_match = 1

        elif violation_type == "category_mismatch":

            amount = int(budget * random.uniform(0.5, 1.0))

            category_match = 0
            quantity_match = 1
            time_match = 1

        elif violation_type == "quantity_violation":

            amount = int(budget * random.uniform(0.5, 1.0))

            category_match = 1
            quantity_match = 0
            time_match = 1

        elif violation_type == "time_violation":

            amount = int(budget * random.uniform(0.5, 1.0))

            category_match = 1
            quantity_match = 1
            time_match = 0

        else:

            amount = int(budget * random.uniform(0.5, 1.0))

            category_match = 1
            quantity_match = 1
            time_match = 1

    else:

        violation_type = "none"

        amount = int(budget * random.uniform(0.3, 1.0))

        category_match = 1
        quantity_match = 1
        time_match = 1

    merchant_trust = round(
        random.uniform(0.3, 1.0),
        2
    )

    historical_success = round(
        random.uniform(0.4, 1.0),
        2
    )

    previous_violations = random.randint(0, 5)

    intent_similarity = round(
        random.uniform(0.2, 0.7)
        if violation
        else random.uniform(0.8, 1.0),
        2
    )

    authorized = int(
        not violation
        and category_match
        and quantity_match
        and time_match
        and amount <= budget
    )

    rows.append({

        "transaction_id":
            f"TXN{i+1:05d}",

        "category":
            category,

        "budget":
            budget,

        "amount":
            amount,

        "category_match":
            category_match,

        "quantity_match":
            quantity_match,

        "time_match":
            time_match,

        "merchant_trust":
            merchant_trust,

        "historical_success":
            historical_success,

        "previous_violations":
            previous_violations,

        "intent_similarity":
            intent_similarity,

        "violation_type":
            violation_type,

        "authorized":
            authorized
    })


df = pd.DataFrame(rows)

df.to_csv(
    "data/intentguard_dataset.csv",
    index=False
)

print("===================================")
print("IntentGuard Dataset Created!")
print("===================================")
print(f"Total transactions: {len(df)}")
print()
print("Authorization distribution:")
print(df["authorized"].value_counts())
print()
print("Violation distribution:")
print(df["violation_type"].value_counts())