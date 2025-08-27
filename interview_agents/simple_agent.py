"""Simple test agent without google-adk dependency."""

def simple_agent():
    """A simple agent function for testing."""
    return {
        "name": "simple_test_agent",
        "description": "A simple test agent",
        "function": lambda x: f"Processed: {x}"
    }

# Export the agent
test_agent = simple_agent()
