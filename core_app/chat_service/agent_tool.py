from core_app.models import ExternalKnowledge
from langchain_community.tools import tool
from pydantic import BaseModel, Field
from pgvector.django import CosineDistance
from core_app.embedding.embedding_by_openai import get_vector_from_embedding
from venv import logger

class ContentInput(BaseModel):
    query: str = Field(description="use this query to find similar contents")

@tool("external_content_search", args_schema=ContentInput)
def external_content_search(query: str, max_results: int = 3) -> str:
    """Find similar content information by a query string"""
    try:
        embedded = get_vector_from_embedding(query)
        
        external_knowledge_qs = ExternalKnowledge.objects.annotate(
            content_distance=CosineDistance("content_embedding", embedded),
            title_distance=CosineDistance("title_embedding", embedded)
        ).order_by("content_distance", "title_distance")[:max_results]
        
        if not external_knowledge_qs.exists():
            return "No similar content found for your query."
        
        results = []
        for knowledge in external_knowledge_qs:
            results.append(
                f"Title: {knowledge.title}\n"
                f"Distance: {knowledge.content_distance:.2f} (Content), "
                f"{knowledge.title_distance:.2f} (Title)\n"
            )

        return results
    
    except Exception as e:
        # Log error message for debugging
        logger.error(f"Error during external content search: {e}")
        return f"An error occurred: {str(e)}"

tool_mapping = {
    "external_content_search": external_content_search,
    }


