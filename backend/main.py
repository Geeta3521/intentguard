from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.intentguard import protect_payment

app = FastAPI(
    title="IntentGuard API",
    description="AI Agent Payment Intent Firewall",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST MODEL
# ==========================================

class PaymentRequest(BaseModel):

    user_request: str

    category: str

    amount: float

    quantity: int = 1

    merchant_trust: float = 1.0

    historical_success: float = 1.0

    previous_violations: int = 0

    intent_similarity: float = 1.0

    time_match: int = 1


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def root():

    return {
        "service": "IntentGuard",
        "status": "online",
        "message": "AI Agent Payment Intent Firewall"
    }


# ==========================================
# PAYMENT CHECK
# ==========================================

@app.post("/check")
def check_payment(
    request: PaymentRequest
):

    payment = {

        "category":
            request.category,

        "amount":
            request.amount,

        "quantity":
            request.quantity,

        "merchant_trust":
            request.merchant_trust,

        "historical_success":
            request.historical_success,

        "previous_violations":
            request.previous_violations,

        "intent_similarity":
            request.intent_similarity,

        "time_match":
            request.time_match
    }

    result = protect_payment(

        request.user_request,

        payment
    )

    return result