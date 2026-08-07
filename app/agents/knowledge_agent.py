from app.rag.retriever import retrieve_relevant_documents
from app.utils.llm import llm
from app.prompts.knowledge_prompt import KNOWLEDGE_PROMPT


def build_context(documents: list) -> str:
    """
    Formats raw Document objects into a clean string context.
    """
    context = ""
    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        context += f"Source: {source}\n{doc.page_content}\n\n---\n\n"
    return context.strip()


def knowledge_agent(state: dict) -> dict:
    """
    Knowledge Agent Node:
    Extracts ticket, retrieves documents, builds context, synthesizes concise 
    internal knowledge using LLM, and returns state update.
    """
    ticket = state["ticket"]

    # 1. Retrieve raw document chunks
    documents = retrieve_relevant_documents(ticket)

    # 2. Convert chunks into a string context
    context = build_context(documents)

    # 3. Format prompt and call LLM
    prompt = KNOWLEDGE_PROMPT.format(
        ticket=ticket,
        context=context
    )

    response = llm.invoke(prompt)

    content_str = response.text

    return {
        "knowledge": content_str.strip()
    }

    # # Safely extract string content whether content is a str or a list of blocks
    # content_str = response.content if isinstance(response.content, str) else str(response.content)

    # return {
    #     "knowledge": content_str.strip()
    # }


# Standalone Independent Test
if __name__ == "__main__":
    test_state = {
        "ticket": "I was charged twice for the same purchase."
    }

    print("\n🚀 Testing Knowledge Agent with LLM Synthesis...")
    result = knowledge_agent(test_state)

    print("\n=== KNOWLEDGE RESULT ===")
    print(result["knowledge"])




# from app.rag.retriever import retrieve_relevant_documents


# def build_context(documents: list) -> str:
#     """
#     Helper function: Formats raw Document objects into a clean string context.
#     """
#     context = ""
#     for doc in documents:
#         source = doc.metadata.get("source", "Unknown")
#         context += f"Source: {source}\n{doc.page_content}\n\n---\n\n"
#     return context.strip()


# def knowledge_agent(state: dict) -> dict:
#     """
#     Knowledge Agent Node (Version 1: Retrieval + Context Building)
#     Extracts ticket, fetches relevant docs, builds string context, and returns 'knowledge'.
#     """
#     ticket = state["ticket"]

#     # 1. Retrieve raw document chunks
#     documents = retrieve_relevant_documents(ticket)

#     # 2. Build readable string context from chunks
#     context = build_context(documents)

#     # 3. Return only the state update key
#     return {
#         "knowledge": context
#     }


# # Standalone Independent Test
# if __name__ == "__main__":
#     test_state = {
#         "ticket": "I was charged twice for the same purchase."
#     }

#     print("\n🚀 Testing Knowledge Agent Independently...")
#     result = knowledge_agent(test_state)

#     print("\n=== KNOWLEDGE RESULT ===")
#     print(result["knowledge"])