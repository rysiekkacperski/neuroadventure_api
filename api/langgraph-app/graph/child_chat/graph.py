from langgraph.graph import StateGraph, START, END

from child_chat.state import ChildState
from child_chat.nodes import assess_social_context, assess_emotional_context, analyze_mood, generate_response

workflow = StateGraph(ChildState)
workflow.add_node("assess_social_cotext", assess_social_context)
workflow.add_node("assess_emotional_cotext", assess_emotional_context)
workflow.add_node("analyze_mood", analyze_mood)
workflow.add_node("generate_response", generate_response)

workflow.add_edge(START, "assess_social_cotext")
workflow.add_edge("assess_social_cotext", "assess_emotional_cotext")
workflow.add_edge("assess_emotional_cotext", "analyze_mood")
workflow.add_edge("analyze_mood", "generate_response")
workflow.add_edge("generate_response", END)

graph = workflow.compile()
