from langchain_openai import OpenAIEmbeddings
import os


embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

def get_vector_from_embedding(text):
    return embeddings_model.embed_query(text)


