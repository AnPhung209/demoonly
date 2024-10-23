from typing import List, Any, Dict, Optional
from typing_extensions import TypedDict


class InputState(TypedDict):
    question: str
    uuid: str
    parsed_question: Dict[str, Any]
    sql_query: str
    results: List[Any]

class OutputState(TypedDict):
    parsed_question: Dict[str, Any]
    unique_noun: List[str]
    sql_query: str
    sql_valid: bool
    sql_issue: str 
    results: List[Any]
    error: str
    