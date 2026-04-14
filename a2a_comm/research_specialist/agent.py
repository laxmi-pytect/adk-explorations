
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from google.adk.tools import google_search
from dotenv import load_dotenv
load_dotenv()



root_agent = Agent(
    model="gemini-2.5-flash",
    name="research_specialist",
    description="A specialist agent that conducts web research and fact-checking.",
    instruction="""
    You receive the call from remote A2A server,
    ignore the A2A calling context, such focus on the question user is looking for answer
    use the specified google search tool to answer the user queries
    """,
    tools=[google_search]
)

a2a_app = to_a2a(root_agent, port=8001)

