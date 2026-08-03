INTENT_PROMPT = """
You are an AI support ticket classifier.

Classify the following customer ticket into exactly one category.

Possible categories:
- Billing
- Login
- Subscription
- Technical

Return ONLY the category name.

Customer Ticket:
{ticket}
"""

