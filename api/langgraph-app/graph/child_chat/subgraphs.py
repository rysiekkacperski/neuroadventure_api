from langgraph.graph import StateGraph, START, END

from child_chat.state import ChildState
from child_chat.nodes import assess_social_context, assess_emotional_context, analyze_mood

asssessment_workflow = StateGraph(ChildState)

asssessment_workflow.add_node("assess_social_cotext", assess_social_context)
asssessment_workflow.add_node("assess_emotional_cotext", assess_emotional_context)
asssessment_workflow.add_node("analyze_mood", analyze_mood)

asssessment_workflow.add_edge(START, "assess_social_cotext")
asssessment_workflow.add_edge(START, "assess_emotional_cotext")
asssessment_workflow.add_edge(START, "analyze_mood")
asssessment_workflow.add_edge("assess_social_cotext", END)
asssessment_workflow.add_edge("assess_emotional_cotext", END)
asssessment_workflow.add_edge("analyze_mood", END)

assesment_graph = asssessment_workflow.compile()