#graph.py
import os
from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from rag import DocumentRAG
from csv_tools import CSVManager
# Shared state between agents
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    query: str
    rag_context: str
    csv_context: str
    final_answer: str
 
# Initialize shared components
rag = DocumentRAG()
csv_manager = CSVManager()
 

print("MODEL:", os.getenv("OLLAMA_MODEL"))
print("KEY EXISTS:", bool(os.getenv("OLLAMA_API_KEY")))
print("BASE URL:", "https://ollama.com") 
# LLM (Ollama Cloud)
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url="https://ollama.com",
    temperature=0.2,
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"
        }
    }
)
 
# ========== Agent Nodes ==========
 
def researcher_node(state: AgentState):
    """Retrieves relevant information from uploaded documents (RAG)"""
    query = state["query"]
    context = rag.retrieve(query)
    return {"rag_context": context}
 
 
def data_analyst_node(state: AgentState):
    """Gets information from the uploaded CSV (e.g. Titanic)"""
    info = csv_manager.get_info()
    return {"csv_context": info}
 
 
def critic_node(state: AgentState):
    """Reviews the collected information"""
    prompt = f"""You are a careful critic.
User question: {state['query']}
 
Document context:
{state.get('rag_context', 'None')}
 
CSV context:
{state.get('csv_context', 'None')}
 
Briefly point out if anything important is missing or unclear. Keep it short."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [response]}
 
 
def synthesizer_node(state: AgentState):
    """Creates the final answer"""
    prompt = f"""You are a helpful research assistant. Answer the user's question clearly using the available context.
 
User Question: {state['query']}
 
--- Document Context ---
{state.get('rag_context', 'No documents uploaded')}
 
--- CSV / Dataset Context ---
{state.get('csv_context', 'No CSV uploaded')}
 
Write a clear and well-structured final answer."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "final_answer": response.content,
        "messages": [response]
    }
 
 
# ========== Build the Graph ==========
 
workflow = StateGraph(AgentState)
 
workflow.add_node("researcher", researcher_node)
workflow.add_node("data_analyst", data_analyst_node)
workflow.add_node("critic", critic_node)
workflow.add_node("synthesizer", synthesizer_node)
 
# Flow: Researcher → Data Analyst → Critic → Synthesizer
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "data_analyst")
workflow.add_edge("data_analyst", "critic")
workflow.add_edge("critic", "synthesizer")
workflow.add_edge("synthesizer", END)
 
# Compile the graph
graph = workflow.compile()