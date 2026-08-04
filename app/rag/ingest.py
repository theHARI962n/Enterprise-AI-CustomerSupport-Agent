from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Import infrastructure settings & shared embeddings
from app.config.settings import (
    KNOWLEDGE_BASE_PATH,
    FAISS_INDEX_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from app.utils.embeddings import embeddings

def load_documents() -> List[Document]:
    """
    Step 1: Load all Markdown files from the knowledge base directory.
    """
    print(f"📄 Step 1: Loading documents from {KNOWLEDGE_BASE_PATH}...")
    
    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(f"Knowledge base directory '{KNOWLEDGE_BASE_PATH}' does not exist!")

    loader = DirectoryLoader(
        str(KNOWLEDGE_BASE_PATH),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},  # Prevents OS-specific character encoding errors
        show_progress=True
    )
    documents = loader.load()
    print(f"   ↳ Successfully loaded {len(documents)} document(s).")
    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Step 2: Split large documents into smaller semantic chunks.
    """
    print(f"✂️ Step 2: Splitting documents (Chunk Size: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP})...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"   ↳ Split into {len(chunks)} chunk(s).")
    return chunks

def build_vector_store(chunks: List[Document]) -> FAISS:
    """
    Steps 3 & 4: Embed document chunks using our shared embedding model and build FAISS index.
    """
    print("🧠 Step 3 & 4: Generating embeddings and constructing FAISS vector store...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("   ↳ FAISS vector store successfully created in memory.")
    return vector_store

def save_vector_store(vector_store: FAISS) -> None:
    """
    Step 5: Persist the FAISS index to disk.
    """
    print(f"💾 Step 5: Saving FAISS index locally to {FAISS_INDEX_PATH}...")
    vector_store.save_local(str(FAISS_INDEX_PATH))
    print("   ↳ Saved successfully!")

def main():
    """
    Orchestrate the ingestion pipeline step-by-step.
    """
    print("🚀 Starting RAG Ingestion Pipeline...\n")
    
    # 1. Load
    documents = load_documents()
    if not documents:
        print("⚠️ No documents found. Ingestion aborted.")
        return

    # 2. Split
    chunks = split_documents(documents)
    if not chunks:
        print("⚠️ No text chunks generated from documents. Ingestion aborted.")
        return

    # 3 & 4. Embed & Build Vector Store
    vector_store = build_vector_store(chunks)

    # 5. Save Index
    save_vector_store(vector_store)

    print("\n✅ Knowledge Base Ingestion Pipeline Finished Successfully!")

    # print(f"Documents: {len(documents)}")
    # print(f"Chunks: {len(chunks)}")
    # print(chunks[0].page_content)
    # print(chunks[0].metadata)
    
if __name__ == "__main__":
    main()