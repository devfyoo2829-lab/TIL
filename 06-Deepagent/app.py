# app.py
from dotenv import load_dotenv
load_dotenv()

from deepagents import create_deep_agent

from tools import send_slack_message
from backend import dt_backend
from state import State
from nodes import upload
from routers import check_files

from langgraph.graph import START, END, StateGraph


deep_agent = create_deep_agent(
    model='openai:gpt-5-mini',
    tools=[send_slack_message],
    backend=dt_backend,
)

workflow = StateGraph(State)
workflow.add_node('deep_agent', deep_agent)
workflow.add_node('upload', upload)

workflow.add_conditional_edges(
    START,
    check_files,
    {
        'upload': 'upload',
        'deep_agent': 'deep_agent'
    }
)
workflow.add_edge('upload', 'deep_agent')
workflow.add_edge('deep_agent', END)

graph = workflow.compile()