# This agent is expected to run many instances in parallel, exploring different topics of interest
# for further investigation
# Available tools:
#       - Todolist
#       - WebSearch

from agents.states import ScoutOutput, ScoutState
from prompts import SCOUT_PROMPT

from typing import TypedDict, List, Annotated
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, BaseMessage
from tools.basic_tools import web_search, reddit_search
from agents.states import NewsStory
import operator
import json
import re
from pydantic import ValidationError


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    tool_iterations: int
    NewsStories: Annotated[List[NewsStory], operator.add]


# This sh
def scout_node(state: ScoutState) -> ScoutState:
    """Node for the scout agent."""
    assigned_task = state["AssignedTask"]
    system_prompt = SCOUT_PROMPT.format(
        topic=assigned_task.topic,
        additional_info=assigned_task.additional_info,
    )
    # Read model from config if available via upstream state injection
    model_name = (
        state.get("config").models.scout if state.get("config") else "gpt-5-mini"
    )
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Tools available to the agent loop
    all_tools = load_tools(["arxiv"]) + [reddit_search, web_search]

    # Agent step: run the model with tools bound
    bound_llm = llm.bind_tools(all_tools, parallel_tool_calls=False)

    def agent_step(s: AgentState):
        prior_messages = s.get("messages", [])
        ai = bound_llm.invoke([SystemMessage(system_prompt), *prior_messages])
        return {"messages": [ai]}

    # Final step: parse structured output WITHOUT tools bound
    def final_step(s: AgentState):
        messages = [SystemMessage(system_prompt), *s.get("messages", [])]
        try:
            parsed: ScoutOutput = llm.with_structured_output(ScoutOutput).invoke(
                messages
            )
        except Exception:
            # Fallback: model may include extra prose or code fences; extract JSON and validate
            raw = llm.invoke(messages)
            content = getattr(raw, "content", str(raw))

            # Remove fenced blocks and isolate first JSON object
            fence_match = re.search(
                r"```(?:json)?\s*([\s\S]*?)```", content, re.IGNORECASE
            )
            if fence_match:
                content = fence_match.group(1).strip()

            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1 and end > start:
                candidate = content[start : end + 1]
            else:
                candidate = content

            try:
                data = json.loads(candidate)
            except json.JSONDecodeError as e:
                raise ValueError(f"Scout output was not valid JSON: {e}")

            try:
                parsed = ScoutOutput.model_validate(data)
            except ValidationError as e:
                raise ValueError(f"Scout output failed validation: {e}")
        return {"NewsStories": parsed.NewsStories}

    # Control step: increment tool iteration count
    def after_tools(s: AgentState):
        count = s.get("tool_iterations", 0) + 1
        return {"tool_iterations": count}

    # Build subgraph for this node
    subgraph = StateGraph(AgentState)
    subgraph.add_node("agent", agent_step)
    subgraph.add_node("tools", ToolNode(all_tools))
    subgraph.add_node("after_tools", after_tools)
    subgraph.add_node("final", final_step)

    subgraph.add_edge(START, "agent")
    # Use prebuilt tools_condition: branch to tools if tool calls present, else to final
    subgraph.add_conditional_edges("agent", tools_condition)
    subgraph.add_edge("tools", "after_tools")
    subgraph.add_conditional_edges(
        "after_tools",
        lambda s: "agent" if s.get("tool_iterations", 0) < 3 else "final",
    )
    subgraph.add_edge("final", END)

    return subgraph.compile()
