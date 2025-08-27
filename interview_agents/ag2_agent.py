"""Simple reasoning engine for deployment."""

class SimpleAgent:
    """A simple agent that works with Vertex AI."""
    
    def __init__(self):
        self.name = "simple_agent"
        self.description = "A simple agent for testing deployment"
    
    def query(self, input_data: str) -> str:
        """Simple query method."""
        return f"Processed: {input_data}"
    
    def __call__(self, input_data):
        """Make the class callable."""
        return self.query(input_data)

# Export the agent
ag2_test_agent = SimpleAgent()