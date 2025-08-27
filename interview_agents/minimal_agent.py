"""Minimal agent for testing deployment."""

def minimal_agent():
    """A minimal agent function."""
    return {
        "name": "minimal_test_agent",
        "description": "A minimal test agent for deployment",
        "model": "gemini-2.0-flash",
        "instruction": "You are a helpful assistant. Respond to user queries.",
        "tools": []
    }

# Export the agent
minimal_test_agent = minimal_agent()
