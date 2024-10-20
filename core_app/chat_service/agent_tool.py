from core_app.models import InternalKnowledge, ExternalKnowledge, Conversation
from langchain_community.tools import WikipediaQueryRun, tool, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.pydantic_v1 import BaseModel, Field
import requests
from pgvector.django import CosineDistance
from core_app.embedding.embedding_by_openai import get_vector_from_embedding
from venv import logger

class QueryDatabase(BaseModel):
    query: str = Field(description="query to look up in the external knowledge table")
 
@tool("query_external_knowledge", args_schema=QueryDatabase)
def query_external_knowledge(query: str) -> str:
    """Find similar content information by a query string"""
    try:
        query_embedding = get_vector_from_embedding(query)
        knowledges = ExternalKnowledge.objects.annotate(
            distance=CosineDistance("content_embedding", query_embedding)
        )
        
        if not knowledges.exists():
            return "No similar content found"
        
        results = []
        for knowledge in knowledges:
            results.append(knowledge.content)        

    except Exception as e:
        # Log error message for debugging
        logger.error(f"Error during external content search: {e}")
        return f"An error occurred: {str(e)}"

tool_mapping = {
    "query_external_knowledge": query_external_knowledge,
    }


