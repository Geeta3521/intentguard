# 🛡️ IntentGuard

### AI Agent Payment Intent Firewall

> **A security layer that verifies whether an AI agent's proposed payment actually matches the user's original intent before authorization.**

IntentGuard is an AI-powered payment security system designed to protect users from unauthorized, manipulated, or risky payment actions performed by AI agents.

It combines **intent extraction, deterministic policy checks, and an XGBoost machine-learning risk model** to produce one of three security decisions:

**🟢 ALLOW · 🟡 REVIEW · 🔴 BLOCK**

---

## 🚨 Problem

AI agents are increasingly capable of performing actions on behalf of users, including shopping and making payments.

While this improves automation, it also introduces security risks.

An AI agent could:

- 💰 Increase the payment amount beyond the user's budget
- 📦 Substitute the requested product category
- 🔢 Increase the requested quantity
- 🏪 Use a suspicious or untrusted merchant
- 🎯 Drift away from the user's original intent
- 🤖 Perform an unauthorized payment action

### Example

**User request:**

> "Buy me a laptop under ₹60,000."

An agent may attempt:

> "Buy a laptop for ₹68,500."

Although the agent is still attempting to purchase a laptop, the transaction violates the user's maximum budget.

**IntentGuard detects the violation before the payment is authorized.**

---

# 💡 Solution

IntentGuard acts as a **payment intent firewall** between an AI agent and a payment system.

```text
User Request
      ↓
Intent Extraction
      ↓
Payment Proposal
      ↓
Policy Engine
      ↓
XGBoost Risk Model
      ↓
Security Decision
      ↓
┌─────────┬─────────┬─────────┐
│  ALLOW  │ REVIEW  │  BLOCK  │
└─────────┴─────────┴─────────┘

🏗️ Architecture
                    ┌──────────────────┐
                    │    User Intent   │
                    │ "Laptop < ₹60K"  │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Intent Extraction│
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │ Payment Proposal │
                    └────────┬─────────┘
                             ↓
             ┌───────────────┴───────────────┐
             ↓                               ↓
    ┌──────────────────┐           ┌──────────────────┐
    │   Policy Engine  │           │  XGBoost Model   │
    │                  │           │                  │
    │ Budget           │           │ Risk Prediction  │
    │ Category         │           │                  │
    │ Quantity         │           │                  │
    │ Merchant Trust   │           │                  │
    │ Intent Similarity│           │                  │
    └────────┬─────────┘           └────────┬─────────┘
             └───────────────┬──────────────┘
                             ↓
                    ┌──────────────────┐
                    │ IntentGuard      │
                    │ Decision Engine   │
                    └────────┬─────────┘
                             ↓
                    ALLOW / REVIEW / BLOCK

🔐 Security Checks
IntentGuard evaluates multiple signals.

| Check                  | Purpose                                     |
| ---------------------- | ------------------------------------------- |
| 💰 Budget              | Prevents spending above the requested limit |
| 📦 Category            | Detects product/category substitution       |
| 🔢 Quantity            | Prevents unauthorized quantity increases    |
| 🏪 Merchant Trust      | Identifies suspicious merchants             |
| 🎯 Intent Similarity   | Detects deviation from the original request |
| 📈 Historical Success  | Provides transaction history context        |
| ⚠️ Previous Violations | Tracks previous security violations         |
| ⏱️ Time Match          | Checks transaction timing consistency       |

🤖 Machine Learning
IntentGuard uses an XGBoost classification model to estimate payment authorization risk.

The model receives features including:
Budget
Payment Amount
Category Match
Quantity Match
Time Match
Merchant Trust
Historical Success
Previous Violations
Intent Similarity

The system calculates:
Authorization Probability
            │
            ▼
Risk Score = 1 - Authorization Probability
Example:
ML Risk Score

██████████  99.92%

Risk Level: HIGH
🛡️ Decision Logic
IntentGuard combines machine-learning risk with hard security policies.

🟢 ALLOW

The payment satisfies the required policy checks and has an acceptable ML risk score.

Example:

User Request:
Buy me a laptop under ₹60,000

Payment:
Laptop
₹55,000
Quantity: 1

Decision: ALLOW
🟡 REVIEW

The payment does not violate a hard policy rule but contains a suspicious signal.

Example:

Merchant Trust: 0.25
```

The payment is within budget and matches the requested category, but the merchant trust score is low.

Decision: REVIEW
Reason: Suspicious merchant
🔴 BLOCK

A hard policy violation is detected.

Example:

Requested limit: ₹60,000
Attempted payment: ₹68,500

Excess: ₹8,500

Decision: BLOCK
Reason: Budget exceeded
🧪 Attack Scenarios

IntentGuard includes six built-in scenarios for testing different AI-agent behaviours.

| Scenario | Expected Result |
|---|---|
| 🟢 Safe Purchase | ALLOW |
| 🔴 Budget Attack | BLOCK |
| 🔴 Category Attack | BLOCK |
| 🔴 Quantity Attack | BLOCK |
| 🟡 Suspicious Merchant | REVIEW |
| 🟡 Intent Drift | REVIEW |

These scenarios demonstrate how the firewall responds to different types of potentially unsafe agent behaviour.

---

## 🖥️ Dashboard

The web interface provides:

📊 Transaction statistics
💳 Payment input
🎯 User intent
🔍 Security decision
🤖 ML risk score
🔐 Policy checks
📜 Transaction history
🧪 Attack scenario testing
🛠️ Tech Stack
Backend
Python
FastAPI
Pydantic
XGBoost
Frontend
HTML
CSS
JavaScript
Machine Learning
XGBoost
Classification
Risk scoring
📁 Project Structure
intentguard/
│
├── backend/
│   ├── agent_simulator.py
│   ├── intent_engine.py
│   ├── intentguard.py
│   ├── main.py
│   ├── policy_engine.py
│   └── train_model.py
│
├── data/
│   ├── generate_dataset.py
│   └── intentguard_dataset.csv
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── models/
│   └── intentguard_xgb.json
│
├── requirements.txt
├── .gitignore
└── README.md
🚀 Running Locally
1. Clone the repository
git clone https://github.com/Geeta3521/intentguard.git
cd intentguard
2. Create virtual environment
python -m venv .venv
3. Activate environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
5. Start FastAPI
python -m uvicorn backend.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
6. Start frontend

Open a second terminal.

```bash
cd frontend
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500
🔌 API
Check Payment
POST /check

Example request:

{
  "user_request": "Buy me a laptop under ₹60000",
  "category": "laptop",
  "amount": 55000,
  "quantity": 1,
  "merchant_trust": 0.95,
  "historical_success": 0.95,
  "previous_violations": 0,
  "intent_similarity": 0.96,
  "time_match": 1
}

The API returns:

Decision
Risk Score
Extracted Intent
Payment Information
Policy Checks
Warnings
Violations
🎯 Project Goal

The goal of IntentGuard is to demonstrate how AI agents can be given an additional security layer before performing high-impact financial actions.

Instead of blindly trusting an AI agent's proposed transaction, IntentGuard verifies whether the transaction is consistent with the user's original request.

The core security question is:

> "Does this payment actually match what the user asked for?"

---

## 🔮 Future Improvements

Potential future improvements include:

🔐 Authentication and authorization
💳 Real payment gateway integration
🧠 Transformer-based intent similarity
📊 Persistent transaction database
📈 Advanced analytics dashboard
🚨 Real-time fraud monitoring
🔑 Cryptographic payment authorization
☁️ Cloud deployment
🔄 Continuous model retraining
👩‍💻 Author

Developed as an AI/ML security project demonstrating:

AI Agents + Machine Learning + Payment Security + FastAPI

⭐ If you find this project interesting

Consider starring the repository ⭐


