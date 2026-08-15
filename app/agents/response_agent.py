from app.utils.llm import llm
from app.prompts.response_prompt import RESPONSE_PROMPT


def response_agent(state: dict) -> dict:
    """
    Response Agent Node:
    Takes ticket and knowledge from state, uses LLM to craft a polite, 
    customer-facing reply adhering strictly to company policy.
    """
    ticket = state["ticket"]
    knowledge = state.get("knowledge", "No specific policy provided.")

    review_feedback = state.get("review", {}).get("feedback", "")

    # 1. Format prompt
    prompt = RESPONSE_PROMPT.format(
        ticket=ticket,
        knowledge=knowledge,
        review_feedback=review_feedback
    )

    # 2. Invoke LLM
    response = llm.invoke(prompt)

    # 3. Clean and return response string using response.text
    return {
        "response": response.text.strip()
    }


# Standalone Independent Test
if __name__ == "__main__":
    test_state = {
        "ticket": "I was charged twice for the same purchase.",
        "knowledge": (
            "1. Verify Transactions: Verify both transactions in the system.\n"
            "2. Check Holds: Confirm charges are not temporary authorization holds.\n"
            "3. Process Refund: If verified, initiate refund immediately.\n"
            "4. Set Expectations: Refunds take 5 business days to complete.\n"
            "5. Escalation: Escalate to Finance if duplicate charges exceed $1,000."
        )
    }

    print("\n🚀 Testing Response Agent Independently...")
    result = response_agent(test_state)

    print("\n=== CUSTOMER RESPONSE ===")
    print(result["response"])