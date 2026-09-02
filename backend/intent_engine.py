import re


def extract_intent(user_request: str):
    """
    Extract structured payment intent
    from a natural-language request.
    """

    request = user_request.lower().strip()

    intent = {
        "raw_request": user_request,
        "category": None,
        "max_amount": None,
        "currency": "INR",
        "quantity": 1
    }

    # -----------------------------------------
    # CATEGORY DETECTION
    # -----------------------------------------

    category_aliases = {
        "laptop": [
            "laptop",
            "notebook computer"
        ],

        "smartphone": [
            "smartphone",
            "smartphones",
            "mobile",
            "mobiles",
            "phone",
            "phones"
        ],

        "headphones": [
            "headphones",
            "headphone",
            "earphones",
            "earbuds"
        ],

        "shoes": [
            "shoes",
            "shoe",
            "running shoes"
        ],

        "hotel": [
            "hotel",
            "hotels"
        ],

        "flight": [
            "flight",
            "flights",
            "air ticket"
        ],

        "groceries": [
            "groceries",
            "grocery"
        ],

        "books": [
            "books",
            "book"
        ]
    }

    for category, keywords in category_aliases.items():

        for keyword in keywords:

           if re.search(
               r"\b" + re.escape(keyword) + r"\b",
               request):
               intent["category"] = category
               break

    # -----------------------------------------
    # AMOUNT DETECTION
    # -----------------------------------------

    patterns = [
        r"(?:under|below|less than|maximum|max)\s*[₹rs\.]*\s*([\d,]+)",
        r"(?:₹|rs\.?)\s*([\d,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            request
        )

        if match:

            amount = match.group(1)

            amount = amount.replace(",", "")

            intent["max_amount"] = float(amount)

            break

    # -----------------------------------------
    # QUANTITY DETECTION
    # -----------------------------------------

    quantity_match = re.search(
        r"(?:buy|get|purchase)\s+(\d+)",
        request
    )

    if quantity_match:

        intent["quantity"] = int(
            quantity_match.group(1)
        )

    return intent


# =========================================
# TEST THE INTENT ENGINE
# =========================================

if __name__ == "__main__":

    examples = [

        "Buy me a laptop under ₹60000",

        "Get me headphones below 5000",

        "Purchase 2 smartphones under ₹50000",

        "Buy running shoes less than ₹8000",

        "Buy a phone under ₹30000",

        "Get earbuds below ₹3000"
    ]

    for example in examples:

        print("\nUSER:")
        print(example)

        print("\nEXTRACTED INTENT:")

        result = extract_intent(
            example
        )

        print(result)