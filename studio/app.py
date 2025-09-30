"""
LangGraph Studio app entrypoint for TheThinkle.ai.

Exports a function `get_graph()` returning the compiled graph and an
`get_example_input()` returning a minimal starter state for Studio.
"""

from typing import Any, Dict

from config import load_config, ThinkleConfig
from generate_newsletter import create_thinkle_graph
from agents.states import ResearchTask, EvaluatorState
from agents.scout import scout_node
from agents.evaluator import evaluator_node
from langgraph.graph import StateGraph, START, END


def get_graph():
    """Return the compiled LangGraph graph for Studio."""
    config: ThinkleConfig = load_config()
    return create_thinkle_graph(config)


def get_example_input() -> Dict[str, Any]:
    """Return a minimal initial state for Studio runs."""
    config: ThinkleConfig = load_config()
    return {"config": config, "ScoutTasks": [], "NewsStories": []}


def get_scout_graph():
    """Return the compiled scout subgraph for Studio visualization."""
    dummy_task = ResearchTask(topic="AI trends", additional_info="Initial exploration")
    return scout_node({"AssignedTask": dummy_task})


def get_evaluator_graph():
    """Return a minimal evaluator graph (single-node) for Studio."""
    graph = StateGraph(EvaluatorState)

    def eval_node(state: EvaluatorState):
        return evaluator_node(state)

    graph.add_node("evaluator", eval_node)
    graph.add_edge(START, "evaluator")
    graph.add_edge("evaluator", END)
    return graph.compile()
