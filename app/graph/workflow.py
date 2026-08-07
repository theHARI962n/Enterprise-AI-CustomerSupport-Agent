from langgraph.graph import StateGraph, START, END

# Import your State definition
from app.graph.state import SupportState

# Import your agent node function
from app.agents.intent_agent import intent_agent
from app.agents.knowledge_agent import knowledge_agent

# Step 2: Create the Builder (deciding that all stations belong to SupportState)
builder = StateGraph(SupportState)

# Step 3: Register Nodes (mapping node names to Python functions)
builder.add_node("intent", intent_agent)
builder.add_node("knowledge", knowledge_agent)

# Step 4: Connect START to the first node
builder.add_edge(START, "intent")

# Step 5: Connect the node to END
builder.add_edge("intent", "knowledge")
builder.add_edge("knowledge", END)

# Step 6: Compile the graph into an executable application
graph = builder.compile()