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
                         │
                         ▼
                ┌─────────────────┐
                │ Intent Extraction│
                └────────┬────────┘
                         │
                         ▼
                Payment Proposal
                         │
                         ▼
                ┌─────────────────┐
                │  Policy Engine  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ XGBoost Risk ML │
                └────────┬────────┘
                         │
                         ▼
               Security Decision
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          🟢 ALLOW    🟡 REVIEW    🔴 BLOCK


🔐 Security Checks

IntentGuard evaluates multiple signals before approving a payment.

Check	Purpose
💰 Budget	Prevents spending above the requested limit
📦 Category	Detects product/category substitution
🔢 Quantity	Prevents unauthorized quantity increases
🏪 Merchant Trust	Identifies suspicious merchants
🎯 Intent Similarity	Detects deviation from the original request
📈 Historical Success	Provides transaction history context
⚠️ Previous Violations	Tracks previous security violations
⏱️ Time Match	Checks transaction timing consistency
🤖 Machine Learning

IntentGuard uses an XGBoost classification model to estimate payment authorization risk.

The model receives the following features:

Budget
Payment Amount
Category Match
Quantity Match
Time Match
Merchant Trust
Historical Success
Previous Violations
Intent Similarity

The model produces an authorization probability.

Authorization Probability
            │
            ▼
Risk Score = 1 - Authorization Probability
Example: Low Risk
ML Risk Score

░░░░░░░░░░  0.04%

Risk Level: LOW
Example: High Risk
ML Risk Score

██████████  99.92%

Risk Level: HIGH

The risk score is displayed in the IntentGuard dashboard.

🛡️ Decision Logic

IntentGuard combines hard security policies with the machine-learning risk score.

🟢 ALLOW

A payment can be allowed when:

Budget check passes
Category matches
Quantity is within the requested amount
No hard policy violation exists
ML risk is acceptable
Example

User Request

Buy me a laptop under ₹60,000

Payment

Category: Laptop
Amount: ₹55,000
Quantity: 1
Merchant Trust: 0.95
Intent Similarity: 0.96

Decision

🟢 ALLOW
🟡 REVIEW

A payment may require review when there is a suspicious signal but no hard policy violation.

Example
Merchant Trust: 0.25

The payment is within budget and matches the requested category, but the merchant trust score is low.

Decision

🟡 REVIEW

Reason: Suspicious merchant

Another example is low intent similarity:

Intent Similarity: 0.40

Decision

🟡 REVIEW

Reason: Payment has low similarity to the user's original intent.
🔴 BLOCK

A payment is blocked when a hard security policy is violated.

Example: Budget Attack
Requested Limit:   ₹60,000
Attempted Payment: ₹68,500

Excess: ₹8,500

Decision

🔴 BLOCK

Reason: Budget exceeded
Example: Quantity Attack
Requested Quantity: 1
Attempted Quantity: 3

Decision

🔴 BLOCK

Reason: Payment quantity exceeds the user's requested quantity.
Example: Category Attack
Requested Category: Laptop
Proposed Category:  Smartphone

Decision

🔴 BLOCK

Reason: Payment category does not match the user's requested category.
🧪 Attack Scenarios

IntentGuard includes six built-in scenarios for testing different AI-agent behaviours.

Scenario	Expected Result
🟢 Safe Purchase	ALLOW
🔴 Budget Attack	BLOCK
🔴 Category Attack	BLOCK
🔴 Quantity Attack	BLOCK
🟡 Suspicious Merchant	REVIEW
🟡 Intent Drift	REVIEW

These scenarios demonstrate how the firewall responds to different types of potentially unsafe agent behaviour.

🖥️ Dashboard

The IntentGuard web dashboard provides an interactive interface for testing payment decisions.

Dashboard features
📊 Transaction statistics
💳 Payment input
🎯 User intent
🔍 Security decision
🤖 ML risk score
🔐 Individual policy checks
📜 Transaction history
🧪 Attack scenario testing
⚠️ Warning and violation explanations

The dashboard communicates with the FastAPI backend through the /check API endpoint.

📊 Transaction Monitoring

The dashboard tracks payment decisions during the current session.

┌──────────────────────┐
│ Total Transactions   │
│         6            │
└──────────────────────┘

┌────────────┐ ┌────────────┐ ┌────────────┐
│ 🟢 ALLOW   │ │ 🟡 REVIEW  │ │ 🔴 BLOCK   │
│     1      │ │     2      │ │     3      │
└────────────┘ └────────────┘ └────────────┘

Transaction history can show:

Time	Category	Amount	Decision
13:20	Laptop	₹55,000	🟢 ALLOW
13:22	Laptop	₹68,500	🔴 BLOCK
13:24	Smartphone	₹45,000	🔴 BLOCK
13:26	Laptop	₹58,000	🟡 REVIEW
🔌 API

IntentGuard exposes a FastAPI REST API.

Health Check
GET /

Example response:

{
  "service": "IntentGuard",
  "status": "online",
  "message": "AI Agent Payment Intent Firewall"
}
Check Payment
POST /check
Example Request
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
API Response

The API returns:

Decision
Risk Score
Extracted Intent
Payment Information
Policy Checks
Warnings
Violations
Example Response
{
  "decision": "ALLOW",
  "risk_score": 0.0004,
  "intent": {
    "raw_request": "Buy me a laptop under ₹60000",
    "category": "laptop",
    "max_amount": 60000,
    "currency": "INR",
    "quantity": 1
  },
  "policy": {
    "decision": "ALLOW",
    "warnings": [],
    "violations": []
  }
}
🛠️ Tech Stack
Backend
Python
FastAPI
Pydantic
Uvicorn
Machine Learning
XGBoost
Classification
Risk scoring
Frontend
HTML5
CSS3
JavaScript
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

Replace YOUR_USERNAME with your GitHub username.

git clone https://github.com/YOUR_USERNAME/intentguard.git
cd intentguard
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment
Windows PowerShell
.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Start the FastAPI backend

From the project root:

python -m uvicorn backend.main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
6. Start the frontend

Open a second terminal.

cd frontend
python -m http.server 5500

Open:

http://127.0.0.1:5500
🧪 Testing the System

After starting both servers:

Test 1 — Safe Purchase
Category: Laptop
Amount: ₹55,000
Quantity: 1
Merchant Trust: 0.95
Intent Similarity: 0.96

Expected:

🟢 ALLOW
Test 2 — Budget Attack
Category: Laptop
Amount: ₹68,500
Quantity: 1

Expected:

🔴 BLOCK

Reason:

Payment exceeds the user's maximum budget.
Test 3 — Category Substitution
Requested: Laptop
Proposed: Smartphone

Expected:

🔴 BLOCK
Test 4 — Quantity Escalation
Requested Quantity: 1
Payment Quantity: 3

Expected:

🔴 BLOCK
Test 5 — Suspicious Merchant
Merchant Trust: 0.25

Expected:

🟡 REVIEW
Test 6 — Intent Drift
Intent Similarity: 0.40

Expected:

🟡 REVIEW
🎯 Project Goal

The goal of IntentGuard is to demonstrate how AI agents can be given an additional security layer before performing high-impact financial actions.

Instead of blindly trusting an AI agent's proposed transaction, IntentGuard verifies whether the transaction is consistent with the user's original request.

The core security question is:

"Does this payment actually match what the user asked for?"

🔮 Future Improvements

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
🔒 Security Philosophy

IntentGuard follows a simple principle:

AI Agent Proposal
       │
       ▼
   Don't Trust
   Automatically
       │
       ▼
 Verify User Intent
       │
       ▼
 Apply Security Policies
       │
       ▼
 Evaluate ML Risk
       │
       ▼
 Make Authorization Decision

This creates an additional protection layer between autonomous AI agents and high-impact financial actions.

👩‍💻 Author

Developed as an AI/ML security project demonstrating:

AI Agents + Machine Learning + Payment Security + FastAPI

⭐ Project

If you find IntentGuard interesting, consider starring the repository ⭐

📌 Disclaimer

IntentGuard is a demonstration and educational security project.

It is not intended to process real financial transactions or replace production-grade payment security, fraud detection, authentication, authorization, or compliance systems.


### After replacing your README

Save with **Ctrl + S**, then run:

```powershell
git add README.md
git commit -m "Add professional project README"
git push
