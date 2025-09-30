#!/usr/bin/env python3
"""
TheThinkle.ai Newsletter Generation System

Main entry point for the newsletter generation pipeline.
Loads configuration, creates the agent graph, and orchestrates the workflow.
"""

# Load environment variables from .env before importing other modules
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True), override=False)

import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import load_config, ThinkleConfig, ConfigParser
from agents.planner import planner_node, PlannerState
from agents.scout import scout_node
from agents.evaluator import evaluator_node
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send
from agents.writer import writer_node

import os, getpass


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")
_set_env("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "thethinkle"


def generate_scout_tasks(state: PlannerState):
    """Generate scout tasks."""
    return [
        Send("scout", {"AssignedTask": task, "config": state["config"]})
        for task in state["ScoutTasks"]
    ]


def create_thinkle_graph(config: ThinkleConfig):
    """
    Create the TheThinkle.ai agent graph.

    Args:
        config: Loaded configuration object

    Returns:
        Compiled StateGraph for newsletter generation
    """

    # Create agent nodes with configuration

    # Build the agent graph
    graph = StateGraph(PlannerState)
    graph.add_node("planner", planner_node)
    graph.add_node("scout", scout_node)
    graph.add_node("evaluator", evaluator_node)
    graph.add_node("writer", writer_node)

    # Define the workflow
    graph.add_edge(START, "planner")
    graph.add_conditional_edges("planner", generate_scout_tasks)
    graph.add_edge("scout", "evaluator")
    graph.add_edge("evaluator", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


def setup_logging(level: int = logging.INFO):
    """Set up logging configuration."""
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """
    CLI Entrypoint for TheThinkle.ai newsletter generation.

    Supports command line arguments for configuration and execution options.
    """
    parser = argparse.ArgumentParser(
        description="Generate personalized newsletters with AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate newsletter with default config
  %(prog)s --config custom.yaml     # Use custom configuration file
        """,
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file (default: config/interests.yaml)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging

    setup_logging(logging.DEBUG if args.verbose else logging.INFO)

    try:
        # Load configuration
        print("📋 Loading configuration...")
        if args.config:
            config_parser = ConfigParser(args.config)
            config = config_parser.load_config()
            print(f"✅ Loaded configuration from {args.config}")
        else:
            config = load_config()
            print("✅ Loaded default configuration")

        # Display configuration summary
        print(f"\n📊 Configuration Summary:")
        print(f"   • Interests: {len(config.interests)} topics")
        print(
            f"     - {', '.join(config.interests[:3])}{'...' if len(config.interests) > 3 else ''}"
        )
        print(f"   • Newsletter tone: {config.newsletter.tone}")
        print(f"   • Max stories: {config.newsletter.max_stories}")
        print(f"   • Output format: {config.output.format}")

        # Create and display the agent graph
        print("\n🤖 Creating AI agent workflow...")
        try:
            agent_graph = create_thinkle_graph(config)
            print("✅ Agent graph created successfully")

            # Display graph structure if possible
            try:
                print("\n📊 Agent Workflow:")
                print(agent_graph.get_graph().draw_ascii())
            except Exception as e:
                print(f"⚠️  Could not display graph: {e}")

        except RuntimeError as e:
            print(f"❌ Failed to create agent graph: {e}")
            print("💡 This is expected if LangGraph dependencies are not installed")
            return

        # TODO: Execute the newsletter generation pipeline
        print("\n🚀 Newsletter generation pipeline ready!")
        print("📝 Pipeline execution not yet implemented.")

        # Future: Invoke the graph with initial state
        initial_state: dict = {
            "config": config,
            "ScoutTasks": [],
            "NewsStories": [],
            "Report": "",
        }
        result = agent_graph.invoke(initial_state)
        # Print the news stories
        print(f"📰 News Stories: {result['NewsStories']}")
        print(f"📝 Report: {result['Report']}")

        # Save markdown report to output folder
        output_dir = Path("data/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        md_path = output_dir / f"newsletter-{ts}.md"
        md_path.write_text(result.get("Report", ""), encoding="utf-8")
        print(f"💾 Saved report to {md_path}")
    except FileNotFoundError as e:
        print(f"❌ Configuration file not found: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"❌ Configuration validation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
