import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

from xgboost import XGBClassifier


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv(
    "data/intentguard_dataset.csv"
)

print("Dataset loaded!")
print(f"Total rows: {len(df)}")


# ==========================================
# 2. SELECT FEATURES
# ==========================================

features = [
    "budget",
    "amount",
    "category_match",
    "quantity_match",
    "time_match",
    "merchant_trust",
    "historical_success",
    "previous_violations",
    "intent_similarity"
]

X = df[features]

y = df["authorized"]


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ==========================================
# 4. CREATE MODEL
# ==========================================

model = XGBClassifier(

    n_estimators=200,

    max_depth=5,

    learning_rate=0.05,

    random_state=42,

    eval_metric="logloss"
)


# ==========================================
# 5. TRAIN
# ==========================================

print("\nTraining IntentGuard model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


# ==========================================
# 6. PREDICTIONS
# ==========================================

predictions = model.predict(
    X_test
)

probabilities = model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# 7. EVALUATION
# ==========================================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(
    classification_report(
        y_test,
        predictions
    )
)


print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


print("\n==============================")
print("ROC-AUC")
print("==============================")

auc = roc_auc_score(
    y_test,
    probabilities
)

print(f"{auc:.4f}")


# ==========================================
# 8. SAVE MODEL
# ==========================================

model.save_model(
    "models/intentguard_xgb.json"
)

print("\n==============================")
print("MODEL SAVED")
print("==============================")

print(
    "models/intentguard_xgb.json"
)