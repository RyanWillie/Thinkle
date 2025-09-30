# This agent will receive the news stories, and the users background.
# It will review each story, combine them if needed, remove any stories that are not relevant
# It can also decide to trigger the investigator agent to investigate a topic further,
# if more information is needed or another perspective could be relevant
#
from config import ThinkleConfig
from agents.states import EvaluatorOutput, EvaluatorState, ResearchTask
from prompts import EVALUATOR_PROMPT
from agents.scout import scout_node
import json

from typing import TypedDict, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from datetime import datetime
from langgraph.types import Send
from langchain_core.messages import HumanMessage


def router_node(state: EvaluatorState):
    """Return a list of Send (one per task) or 'end' when complete; cap follow-ups to 1 cycle."""
    tasks = state.get("InvestigatorTasks", [])
    if tasks and state.get("followup_cycles", 0) < 1:
        return [
            Send(
                "scout",
                {
                    "AssignedTask": ResearchTask(
                        topic=t.topic, additional_info=t.additional_info
                    )
                },
            )
            for t in tasks
        ]
    return "end"


def llm_node(state: EvaluatorState) -> EvaluatorState:
    """Node for the evaluator agent."""
    config = state["config"]
    news_stories = state["NewsStories"]
    prior_messages = state.get("messages", [])

    user_background = config.user_profile
    system_prompt = EVALUATOR_PROMPT.format(
        interests=config.interests, user_profile=user_background
    )
    llm = ChatOpenAI(model=config.models.evaluator, temperature=0)
    structured_llm = llm.with_structured_output(EvaluatorOutput)
    stories_payload = [s.model_dump() for s in news_stories]
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=json.dumps({"NewsStories": stories_payload})),
    ] + list(prior_messages)
    if len(state.get("InvestigatorTasks", [])) > 0:
        messages.append(
            HumanMessage(
                content=json.dumps(
                    {
                        "InvestigatorTasks already completed": [
                            t.model_dump() for t in state["InvestigatorTasks"]
                        ]
                    }
                )
            )
        )
    response = structured_llm.invoke(messages)
    return {
        "NewsStories": response.NewsStories,
        "InvestigatorTasks": response.InvestigatorTasks,
    }


def clear_tasks_node(state: EvaluatorState) -> EvaluatorState:
    """Clear tasks and increment follow-up cycle count, adding a brief status message."""
    new_cycle = state.get("followup_cycles", 0) + 1
    stories = state.get("NewsStories", [])
    preview = (
        [{"title": s.title, "url": s.url} for s in stories[-3:]] if stories else []
    )
    msg = HumanMessage(
        content=json.dumps(
            {
                "followup_complete": True,
                "followup_cycles": new_cycle,
                "appended_count": len(stories),
                "appended_preview": preview,
            }
        )
    )
    return {"InvestigatorTasks": [], "followup_cycles": new_cycle, "messages": [msg]}


# This is also a subgraph,
def evaluator_node(state: EvaluatorState) -> EvaluatorState:
    """Node for the evaluator agent."""

    graph = StateGraph(EvaluatorState)
    graph.add_node("llm", llm_node)
    graph.add_node("scout", scout_node)
    graph.add_node("clear_tasks", clear_tasks_node)

    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", router_node, {"end": END})
    graph.add_edge("scout", "clear_tasks")
    graph.add_edge("clear_tasks", "llm")
    return graph.compile()
