from langgraph.graph import StateGraph, START, END

# Import your State definition
from app.graph.state import SupportState

# Import your agent node function
from app.agents.intent_agent import intent_agent
from app.agents.knowledge_agent import knowledge_agent
from app.agents.response_agent import response_agent
from app.agents.reviewer_agent import reviewer_agent


def review_router(state: SupportState):
    if state["review"]["approved"]:
        return "approved"

    return "rejected"

# def bad_response_test_node(state: SupportState) -> dict:
#     return {
#         "response": (
#             "I have verified both transactions and issued your refund. "
#             "Your refund will arrive in 3 business days."
#         )
#     }

# Step 2: Create the Builder (deciding that all stations belong to SupportState)
builder = StateGraph(SupportState)

# Step 3: Register Nodes (mapping node names to Python functions)
builder.add_node("intent", intent_agent)
builder.add_node("knowledge", knowledge_agent)
builder.add_node("response", response_agent)
builder.add_node("reviewer", reviewer_agent)
# builder.add_node("bad_response", bad_response_test_node)

# Step 4: Connect START to the first node
builder.add_edge(START, "intent")

# Step 5: Connect the node to END
builder.add_edge("intent", "knowledge")
builder.add_edge("knowledge", "response")
builder.add_edge("response", "reviewer")
# builder.add_edge("knowledge", "bad_response")

# builder.add_edge("bad_response", "reviewer")

builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "approved": END,
        "rejected": "response"
    }
)


# Step 6: Compile the graph into an executable application
graph = builder.compile()

# -----------------------------
# Graph test
# -----------------------------

if __name__ == "__main__":

    initial_state = {
        "ticket": "I was charged twice for the same purchase."
    }

    print("\n🚀 Running Customer Support Graph...")

    result = graph.invoke(initial_state)

    print("\n==============================")
    print("       FINAL RESULT")
    print("==============================")

    print("\nIntent:")
    print(result["intent"])

    print("\nKnowledge:")
    print(result["knowledge"])

    print("\nResponse:")
    print(result["response"])

    print("\nReview:")
    print(result["review"])