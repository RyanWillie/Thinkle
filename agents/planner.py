# This agent generates the plan for what should be investigated to generate
# The newsletter

from config import ThinkleConfig
from agents.states import PlannerOutput, PlannerState, ResearchTask
from prompts import PLANNER_PROMPT

from typing import TypedDict, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from datetime import datetime


def planner_node(state: PlannerState) -> PlannerState:
    """Node for the planner agent."""
    config = state["config"]
    user_background = config.user_profile
    system_prompt = PLANNER_PROMPT.format(
        interests=config.interests,
        background=user_background,
        date=datetime.now().strftime("%Y-%m-%d"),
        max_tasks=config.max_tasks,
    )
    llm = ChatOpenAI(model=config.models.planner, temperature=0)
    structured_llm = llm.with_structured_output(PlannerOutput)
    response = structured_llm.invoke([SystemMessage(content=system_prompt)])

    # Dummy response
    # response = PlannerOutput(ScoutTasks=[ResearchTask(topic="Topic 1", additional_info="Additional info 1"), ResearchTask(topic="Topic 2", additional_info="Additional info 2")])
    return {"ScoutTasks": response.ScoutTasks}
