"""
Prompt module - Prompt management

This module handles:
- Agent system prompts 
"""

from .prompts import (
    PLANNER_PROMPT,
    EVALUATOR_PROMPT,
    SCOUT_PROMPT,
    WRITER_PROMPT,
)

__all__ = [
    'PLANNER_PROMPT',
    'EVALUATOR_PROMPT',
    'SCOUT_PROMPT',
    'WRITER_PROMPT',
]
