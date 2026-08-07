from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.config.settings import FAISS_INDEX_PATH, TOP_K
from app.utils.embeddings import embeddings


def load_vector_store() -> FAISS:
    """
    Load the persisted FAISS vector store from disk.
    """
    if not FAISS_INDEX_PATH.exists():
        raise FileNotFoundError(
            f"FAISS index directory not found at '{FAISS_INDEX_PATH}'. "
            "Please run `python -m app.rag.ingest` first to create the index!"
        )

    print(f"📥 Loading FAISS index from {FAISS_INDEX_PATH}...")
    
    # allow_dangerous_deserialization is required by FAISS for local pickle loading
    vector_store = FAISS.load_local(
        folder_path=str(FAISS_INDEX_PATH),
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    print("   ↳ Vector store loaded successfully.")
    return vector_store


def retrieve_relevant_documents(query: str, top_k: int = TOP_K) -> List[Document]:
    """
    Search the vector store for the top K most relevant document chunks matching the query.
    """
    print(f"🔍 Searching knowledge base for: '{query}'")
    
    vector_store = load_vector_store()
    
    # Perform Similarity Search
    results = vector_store.similarity_search(
        query=query,
        k=top_k
    )
    
    print(f"   ↳ Retrived {len(results)} relevant chunk(s).")
    return results


def main():
    """
    Quick local test to inspect retrieved context.
    """
    test_query = "How do I reset my password?"  # Replace with a query relevant to your markdown files
    
    try:
        documents = retrieve_relevant_documents(test_query)
        
        print("\n--- Retrieved Context Chunks ---")
        for i, doc in enumerate(documents, start=1):
            print(f"\n Chunk {i}:")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content: {doc.page_content[:200]}...")  # Show preview of content
            
    except FileNotFoundError as err:
        print(f"\n⚠️ {err}")


if __name__ == "__main__":
    main()