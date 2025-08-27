"""Test deployment without extra packages."""

import os
import sys
import vertexai
from absl import app, flags
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from simple_test_agent import create_simple_agent

FLAGS = flags.FLAGS
flags.DEFINE_bool("create", False, "Creates a new test deployment.")

def create_test_deployment():
    """Create a test deployment."""
    # Create simple agent
    root_agent = create_simple_agent()
    print(f"✅ Created test agent: {root_agent.name}")

    # Wrap in AdkApp
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    # Deploy without extra packages
    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
        ],
        # No extra_packages
    )
    print(f"Created remote app: {remote_app.resource_name}")

def main(argv=None):
    """Main function."""
    if argv is None:
        argv = flags.FLAGS(sys.argv)
    else:
        argv = flags.FLAGS(argv)

    load_dotenv()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("REGION")
    bucket = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")

    if not project_id or not location:
        print("Missing required environment variables")
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket,
    )

    if FLAGS.create:
        create_test_deployment()
    else:
        print("Use --create to deploy test agent")

if __name__ == "__main__":
    app.run(main)
