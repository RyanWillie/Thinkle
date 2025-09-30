# This agent is responsible for taking in the research articles and constructing a short, informative and entertaining article
# to be read. Initially in Markdown format.

from agents.states import WriterOutput, WriterState
from prompts import WRITER_PROMPT

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from datetime import datetime
import json

def writer_node(state: WriterState) -> WriterState:
    """Node for the writer agent."""
    
    config = state["config"]
    user_background = config.user_profile
    system_prompt = WRITER_PROMPT.format(user_profile=user_background, newsletter_tone=config.newsletter.tone, include_opinions=config.newsletter.include_opinions, date=datetime.now().strftime("%Y-%m-%d"))
    llm = ChatOpenAI(model=config.models.writer, temperature=0)
    structured_llm = llm.with_structured_output(WriterOutput)
    stories_payload = [s.model_dump() for s in state["NewsStories"]]
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=json.dumps({"NewsStories": stories_payload}))
    ]
    response = structured_llm.invoke(messages)

    return {
        "Report": response.Report
    }
    