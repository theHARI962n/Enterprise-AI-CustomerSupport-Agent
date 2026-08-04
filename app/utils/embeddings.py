from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config.settings import (
    EMBEDDING_MODEL,
    GOOGLE_API_KEY
)

embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GOOGLE_API_KEY,
)

# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Load environment variables
# load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     raise ValueError("GOOGLE_API_KEY is missing in the .env file!")

# # Single Source of Truth for Embeddings
# # We use text-embedding-004, Google's recommended embedding model
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004",
#     google_api_key=api_key
# )