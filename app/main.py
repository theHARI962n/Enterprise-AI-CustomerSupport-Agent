from app.graph.workflow import graph

def run_test():
    print("--- Running Intent Agent Test ---")
    
    # 1. Input initial state
    initial_state = {
        "ticket": "I noticed a duplicate charge on my credit card bill."
    }
    
    print(f"Input State: {initial_state}")
    
    # 2. Invoke the graph
    final_state = graph.invoke(initial_state)
    
    # 3. Print the resulting merged state
    print("\n--- Result ---")
    print(f"Final State: {final_state}")
    print(f"Detected Intent: {final_state.get('intent')}")

if __name__ == "__main__":
    run_test()