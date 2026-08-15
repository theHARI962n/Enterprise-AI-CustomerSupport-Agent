from pydantic import BaseModel, Field
from app.utils.llm import llm
from app.prompts.reviewer_prompt import REVIEWER_PROMPT


# 1. Define Pydantic Schema for Structured Output
class ReviewResult(BaseModel):
    approved: bool = Field(description="True if response is accurate and follows policy, False otherwise.")
    feedback: str = Field(description="Empty string if approved; specific actionable guidance on what to fix if rejected.")


def reviewer_agent(state: dict) -> dict:
    """
    Reviewer Agent Node:
    Evaluates draft response against ticket and knowledge using Pydantic structured output.
    Returns: {"review": {"approved": bool, "feedback": str}}
    """
    ticket = state["ticket"]
    knowledge = state["knowledge"]
    response = state["response"]

    # 2. Bind structured output schema to LLM
    structured_llm = llm.with_structured_output(ReviewResult)

    # 3. Format prompt
    prompt = REVIEWER_PROMPT.format(
        ticket=ticket,
        knowledge=knowledge,
        response=response
    )

    # 4. Invoke LLM (returns direct Pydantic ReviewResult instance)
    review_output: ReviewResult = structured_llm.invoke(prompt)

    # 5. Return dict representation for state merge
    return {
        "review": review_output.model_dump()
    }


# Standalone Independent Test
if __name__ == "__main__":
    test_ticket = "I was charged twice for the same purchase."
    test_knowledge = (
        "1. Verify Transactions: Verify both transactions in system.\n"
        "2. Check Holds: Confirm charges aren't temporary holds.\n"
        "3. Process Refund: If verified, initiate refund immediately.\n"
        "4. Set Expectations: Refunds take 5 business days."
    )

    # Test 1: Good Response (Should Approve)
    good_state = {
        "ticket": test_ticket,
        "knowledge": test_knowledge,
        "response": (
            "I am sorry to hear about the duplicate charge on your account. "
            "We will verify both transactions and confirm that they are not temporary holds. "
            "Once confirmed, we will initiate a refund, which typically takes 5 business days to process."
        )
    }

    # Test 2: Deliberately Bad Response (Should Reject)
    bad_state = {
        "ticket": test_ticket,
        "knowledge": test_knowledge,
        "response": (
            "I have verified the transactions and issued your refund. "
            "Your refund will arrive in 3 business days."
        )
    }

    print("\n🚀 Testing Reviewer Agent with Pydantic Structured Output...")

    print("\n--- Test 1: Good Response ---")
    res1 = reviewer_agent(good_state)
    print("Approved:", res1["review"]["approved"])
    print("Feedback:", res1["review"]["feedback"])

    print("\n--- Test 2: Deliberately Bad Response ---")
    res2 = reviewer_agent(bad_state)
    print("Approved:", res2["review"]["approved"])
    print("Feedback:", res2["review"]["feedback"])