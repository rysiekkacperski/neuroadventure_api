from langgraph.graph import StateGraph, START, END

from child_chat.state import ChildState
from child_chat.nodes import generate_response
from child_chat.subgraphs import assesment_graph

workflow = StateGraph(ChildState)
workflow.add_node("assess_context", assesment_graph)
workflow.add_node("generate_response", generate_response)

workflow.add_edge(START, "assess_context")
workflow.add_edge("assess_context", "generate_response")
workflow.add_edge("generate_response", END)

graph = workflow.compile()
