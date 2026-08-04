from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Project Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_BASE_PATH = BASE_DIR / "knowledge_base"

FAISS_INDEX_PATH = BASE_DIR / "faiss_index"


# -----------------------------
# Gemini Models
# -----------------------------

LLM_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "gemini-embedding-2"


# -----------------------------
# RAG Configuration
# -----------------------------

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

TOP_K = 4


# -----------------------------
# API Keys
# -----------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")