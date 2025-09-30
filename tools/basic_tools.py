# Basic tools available to all agents
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from typing import Annotated, TypedDict, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
import requests
from typing import List, Dict

class Todo(TypedDict):
    """Todo to track."""

    content: str
    status: Literal["pending", "in_progress", "completed"]
# Todo list

# Web search tool
@tool
def web_search(query: str) -> str:
    """Search the web for the query."""
    tavily_search = TavilySearchResults(max_results=5)
    return tavily_search.invoke(query)

# Youtube transcript tool

# Reddit tool
@tool
def reddit_search(
    query: str,
    subreddit: str = "all",
    limit: int = 5
) -> List[Dict]:
    """
    Search Reddit posts using the Pushshift API.

    Args:
        query (str): Search term
        subreddit (str): Subreddit to search (default: 'all')
        limit (int): Number of posts to return

    Returns:
        List[Dict]: A list of Reddit posts with title, url, score, and subreddit
    """
    url = "https://api.pushshift.io/reddit/search/submission"
    params = {
        "q": query,
        "subreddit": subreddit,
        "size": limit,
        "sort": "desc",
        "sort_type": "score"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json().get("data", [])

    return [
        {
            "title": post.get("title", "No title"),
            "url": f"https://www.reddit.com{post.get('permalink', '')}",
            "score": post.get("score", 0),
            "subreddit": post.get("subreddit", ""),
            "created_utc": post.get("created_utc")
        }
        for post in data
    ]