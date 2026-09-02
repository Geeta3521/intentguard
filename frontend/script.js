const API_URL = "http://127.0.0.1:8000/check";

let transactionStats = {
    total: 0,
    allow: 0,
    review: 0,
    block: 0
};

let transactionHistory = [];


// ==========================================
// CHECK PAYMENT
// ==========================================

async function checkPayment() {

    const button = document.getElementById("checkButton");
    const resultDiv = document.getElementById("result");

    button.disabled = true;
    button.innerText = "⏳ Checking...";

    const data = {

        user_request:
            document.getElementById("userRequest").value,

        category:
            document.getElementById("category").value,

        amount:
            Number(document.getElementById("amount").value),

        quantity:
            Number(document.getElementById("quantity").value),

        merchant_trust:
            Number(document.getElementById("merchantTrust").value),

        historical_success:
            Number(document.getElementById("historicalSuccess").value),

        previous_violations: 0,

        intent_similarity:
            Number(document.getElementById("intentSimilarity").value),

        time_match: 1
    };


    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });


        if (!response.ok) {
            throw new Error("API request failed");
        }


        const result = await response.json();

        updateDashboard(result);

        addTransaction(result);

        displayResult(result);

    }

    catch (error) {

        console.error(error);

        resultDiv.innerHTML = `
            <div class="decision block">

                <h3>⚠️ API ERROR</h3>

                <p>
                    Could not connect to IntentGuard backend.
                    <br><br>
                    Make sure FastAPI is running at
                    <strong>127.0.0.1:8000</strong>.
                </p>

            </div>
        `;

    }

    finally {

        button.disabled = false;

        button.innerText = "🛡️ Check Payment";

    }
}


// ==========================================
// DISPLAY SECURITY RESULT
// ==========================================

function displayResult(result) {

    const resultDiv = document.getElementById("result");

    const decision = result.decision;

    const risk = result.risk_score;

    const policy = result.policy;

    const checks = policy.checks;


    let decisionClass = decision.toLowerCase();

    let icon = "🟢";

    if (decision === "BLOCK") {
        icon = "🔴";
    }

    else if (decision === "REVIEW") {
        icon = "🟡";
    }


    // Risk level

    let riskLevel = "LOW";

    if (risk >= 0.7) {
        riskLevel = "HIGH";
    }

    else if (risk >= 0.3) {
        riskLevel = "MEDIUM";
    }


    resultDiv.innerHTML = `

        <div class="decision ${decisionClass}">

            <h3>
                ${icon} ${decision}
            </h3>

            <p>
                IntentGuard security decision
            </p>

        </div>


        <div class="risk-box">

            <div class="risk-header">

                <span>
                    ML Risk Score
                </span>

                <span class="risk-value">
                    ${risk}
                </span>

            </div>

            <div class="risk-bar">

                <div
                    class="risk-fill"
                    style="width: ${risk * 100}%"
                ></div>

            </div>

            <p style="margin-top:10px;">
                Risk Level: <strong>${riskLevel}</strong>
            </p>

        </div>


        <div class="check-list">

            <div class="check-item">

                <span>💰 Budget</span>

                <span class="${
                    checks.budget.passed
                    ? "pass"
                    : "fail"
                }">

                    ${
                        checks.budget.passed
                        ? "✓ PASS"
                        : "✗ FAIL"
                    }

                </span>

            </div>


            <div class="check-item">

                <span>📦 Category</span>

                <span class="${
                    checks.category.passed
                    ? "pass"
                    : "fail"
                }">

                    ${
                        checks.category.passed
                        ? "✓ PASS"
                        : "✗ FAIL"
                    }

                </span>

            </div>


            <div class="check-item">

                <span>🔢 Quantity</span>

                <span class="${
                    checks.quantity.passed
                    ? "pass"
                    : "fail"
                }">

                    ${
                        checks.quantity.passed
                        ? "✓ PASS"
                        : "✗ FAIL"
                    }

                </span>

            </div>


            <div class="check-item">

                <span>🏪 Merchant Trust</span>

                <span class="${
                    checks.merchant_trust.score < 0.5
                    ? "warning"
                    : "pass"
                }">

                    ${checks.merchant_trust.score}

                </span>

            </div>


            <div class="check-item">

                <span>🎯 Intent Similarity</span>

                <span class="${
                    checks.intent_similarity.score < 0.5
                    ? "warning"
                    : "pass"
                }">

                    ${checks.intent_similarity.score}

                </span>

            </div>

        </div>


        ${showAlerts(policy)}

    `;
}


// ==========================================
// SECURITY EXPLANATION
// ==========================================

function showAlerts(policy) {

    let html = "";


    if (policy.violations.length > 0) {

        policy.violations.forEach(violation => {

            html += `

                <div class="alert block-alert">

                    🚫 <strong>Security Violation</strong>

                    <br>

                    ${violation}

                </div>

            `;

        });

    }


    if (policy.warnings.length > 0) {

        policy.warnings.forEach(warning => {

            html += `

                <div class="alert warning-alert">

                    ⚠️ <strong>Security Warning</strong>

                    <br>

                    ${warning}

                </div>

            `;

        });

    }


    return html;
}


// ==========================================
// DASHBOARD STATISTICS
// ==========================================

function updateDashboard(result) {

    const decision = result.decision;

    transactionStats.total++;


    if (decision === "ALLOW") {
        transactionStats.allow++;
    }

    else if (decision === "REVIEW") {
        transactionStats.review++;
    }

    else if (decision === "BLOCK") {
        transactionStats.block++;
    }


    document.getElementById("totalTransactions").innerText =
        transactionStats.total;

    document.getElementById("allowCount").innerText =
        transactionStats.allow;

    document.getElementById("reviewCount").innerText =
        transactionStats.review;

    document.getElementById("blockCount").innerText =
        transactionStats.block;
}


// ==========================================
// TRANSACTION HISTORY
// ==========================================

function addTransaction(result) {

    const category =
        document.getElementById("category").value;

    const amount =
        Number(document.getElementById("amount").value);


    const now = new Date();

    const time =
        now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        });


    transactionHistory.unshift({

        time: time,

        category: category,

        amount: amount,

        decision: result.decision

    });


    // Keep latest 10 transactions

    transactionHistory =
        transactionHistory.slice(0, 10);


    renderHistory();
}


// ==========================================
// DISPLAY HISTORY
// ==========================================

function renderHistory() {

    const historyDiv =
        document.getElementById("history");


    if (transactionHistory.length === 0) {

        historyDiv.innerHTML = `
            <div class="empty-history">
                No transactions yet.
            </div>
        `;

        return;
    }


    let html = "";


    transactionHistory.forEach(transaction => {

        let icon = "🟢";

        if (transaction.decision === "BLOCK") {
            icon = "🔴";
        }

        else if (transaction.decision === "REVIEW") {
            icon = "🟡";
        }


        html += `

            <div class="check-item">

                <span>
                    ${transaction.time}
                </span>

                <span>
                    ${transaction.category}
                </span>

                <span>
                    ₹${transaction.amount.toLocaleString("en-IN")}
                </span>

                <span>
                    ${icon} ${transaction.decision}
                </span>

            </div>

        `;

    });


    historyDiv.innerHTML = html;
}


// ==========================================
// ATTACK SCENARIOS
// ==========================================

function loadScenario(type) {

    const category =
        document.getElementById("category");

    const amount =
        document.getElementById("amount");

    const quantity =
        document.getElementById("quantity");

    const merchantTrust =
        document.getElementById("merchantTrust");

    const intentSimilarity =
        document.getElementById("intentSimilarity");


    if (type === "safe") {

        category.value = "laptop";

        amount.value = 55000;

        quantity.value = 1;

        merchantTrust.value = 0.95;

        intentSimilarity.value = 0.96;

    }


    else if (type === "budget") {

        category.value = "laptop";

        amount.value = 68500;

        quantity.value = 1;

        merchantTrust.value = 0.95;

        intentSimilarity.value = 0.96;

    }


    else if (type === "category") {

        category.value = "smartphone";

        amount.value = 45000;

        quantity.value = 1;

        merchantTrust.value = 0.95;

        intentSimilarity.value = 0.50;

    }


    else if (type === "quantity") {

        category.value = "laptop";

        amount.value = 55000;

        quantity.value = 3;

        merchantTrust.value = 0.95;

        intentSimilarity.value = 0.95;

    }


    else if (type === "merchant") {

        category.value = "laptop";

        amount.value = 58000;

        quantity.value = 1;

        merchantTrust.value = 0.25;

        intentSimilarity.value = 0.92;

    }


    else if (type === "drift") {

        category.value = "laptop";

        amount.value = 55000;

        quantity.value = 1;

        merchantTrust.value = 0.90;

        intentSimilarity.value = 0.40;

    }


    // Automatically check scenario

    checkPayment();
}