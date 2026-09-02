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
