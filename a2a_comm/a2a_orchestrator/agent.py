# In a2a_orchestrator/agent.py (Starter Code)
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from dotenv import load_dotenv
import os

load_dotenv()

filepaths=os.getenv("FILEPATH")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepaths}/adk-exploration/genai_service_account.json"


# TODO: 1. Create a `RemoteA2aAgent` instance named `remote_researcher`.
# - Give it a name and a description.
# - Point its `agent_card` URL to the specialist server you will be running.
#   (Using the `AGENT_CARD_WELL_KNOWN_PATH` constant is recommended).
remote_researcher = RemoteA2aAgent(
    name="remote_researcher",
    description="A remote specialist that can conduct web research and fact-checking.",
    agent_card=f"http://127.0.0.1:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)



# TODO: 2. Define the `root_agent` as an orchestrator.
# - Its instruction should tell it to delegate research tasks to the `remote_researcher`.
# - Add the `remote_researcher` to its `sub_agents` list.
root_agent = Agent(
    model="gemini-2.5-flash",
    name="orchestrator_agent",
    description="A coordinator agent that delegates tasks to remote specialists.",
    instruction=""" you are helpful agent, who helps with user's query resolution
    1. if there is generic question you can answer it
    2. for any specific question route it to remote_researcher which is the sub_agent.
    """,
    sub_agents=[remote_researcher]
)
