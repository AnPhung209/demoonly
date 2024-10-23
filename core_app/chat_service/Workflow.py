from langgraph.graph import StateGraph
from chat_service.State import InputState, OutputState
from chat_service.SQLAgent import SQLAgent
from langgraph.graph import END

class Workflow:
    def __init__(self):
        self.sql_agent = SQLAgent()


    def create_wokflow(self) -> StateGraph:
        """Create and configure the workflow."""
        workflow = StateGraph(input=InputState, output=OutputState)

        #Add node
        workflow.add_node("parse_question", self.sql_agent.parse_question)
        workflow.add_node("get_unique_nouns", self.sql_agent.get_unique_nouns)
        workflow.add_node("generate_sql", self.sql_agent.generate_sql)
        workflow.add_node("validate_and_fix_sql", self.sql_agent.validate_and_fix_sql)
        workflow.add_node("execute_sql", self.sql_agent.execute_sql)
        workflow.add_node("format_results", self.sql_agent.format_results)
        
        #Add edges
        workflow.add_edge("parse_question", "get_unique_nouns")
        workflow.add_edge("get_unique_nouns", "generate_sql")
        workflow.add_edge("generate_sql", "validate_and_fix_sql")
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_results")
        workflow.add_edge("format_results", END)

        return workflow
    
    def returnGraph(self):
        return self.create_wokflow().compile()
    
    def run_sql_agent(self, question: str, uuid: str) -> dict:
        """Run the SQL agent workflow and return formatted answer."""
        app = self.create_wokflow().compile()
        result = app.invoke({"question": question, "uuid": uuid})
        return {"answer": result["answer"]}
