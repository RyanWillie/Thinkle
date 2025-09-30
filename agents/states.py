from pydantic import BaseModel, Field
from typing import List, TypedDict, Annotated
import operator
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from config import ThinkleConfig


class ResearchTask(BaseModel):
    """Task for the scout agent."""

    topic: str = Field(..., description="The topic to investigate")
    additional_info: str = Field(
        ..., description="Additional information about the user to be considered"
    )


class NewsStory(BaseModel):
    """Story for the scout agent."""

    title: str = Field(..., description="The title of the story")
    summary: str = Field(..., description="The summary of the story")
    source: str = Field(..., description="The source of the story")
    url: str = Field(..., description="The url of the story")
    score: int = Field(
        ..., description="The score of the story of relevance to the user"
    )
    timestamp: str = Field(..., description="The timestamp of the story")
    topic: str = Field(..., description="The topic of the story")


class PlannerOutput(BaseModel):
    """Output of the planner agent. This will each spawn a scout agent."""

    ScoutTasks: List[ResearchTask] = Field(
        ..., description="The tasks to be investigated"
    )


class PlannerState(TypedDict):
    """State for the planner agent."""

    config: ThinkleConfig
    ScoutTasks: List[ResearchTask]  # Requires a reducer to add the tasks
    NewsStories: Annotated[
        List[NewsStory], operator.add
    ]  # Requires a reducer to add the stories
    Report: str


class EvaluatorState(TypedDict):
    """State for the evaluator agent."""

    config: ThinkleConfig
    NewsStories: Annotated[List[NewsStory], operator.add]
    InvestigatorTasks: List[ResearchTask]
    followup_cycles: int
    messages: Annotated[List[BaseMessage], add_messages]


class EvaluatorOutput(BaseModel):
    """Output of the evaluator agent."""

    NewsStories: List[NewsStory] = Field(
        ..., description="The relevant news stories that have been identified"
    )
    InvestigatorTasks: List[ResearchTask] = Field(
        ..., description="The tasks to be investigated"
    )
    Explanation: str = Field(..., description="The explanation of the output")


class ScoutState(TypedDict):
    """State for the scout agent."""

    AssignedTask: ResearchTask
    config: ThinkleConfig


class ScoutOutput(BaseModel):
    """Output of the scout agent."""

    NewsStories: List[NewsStory] = Field(
        ..., description="The relevant news stories that have been identified"
    )
    Explanation: str = Field(..., description="The explanation of the output")


class WriterOutput(BaseModel):
    """Output of the writer agent."""

    Report: str = Field(..., description="The report of the output")


class WriterState(TypedDict):
    """State for the writer agent."""

    config: ThinkleConfig
    NewsStories: List[NewsStory]
    Report: str
