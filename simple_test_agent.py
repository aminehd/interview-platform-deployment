"""Simple test agent without custom packages."""

from google.adk.agents import Agent

def create_simple_agent():
    """Create a simple test agent."""
    return Agent(
        name="simple_test_agent",
        description="A simple test agent",
        instruction="You are a helpful assistant.",
        model="gemini-2.5-pro"
    )
