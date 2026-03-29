from google.adk.agents.llm_agent import Agent

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.langchain_tool import LangchainTool


from .custom_agent import google_search_agent
from .other_tools import langchain_wikipedia_tool


from .custom_function import get_fx_rate


import os

filepath=os.getenv("FILEPATH")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepath}/adk-exploration/genai_service_account.json"


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[FunctionTool(get_fx_rate), AgentTool(agent=google_search_agent),  LangchainTool(langchain_wikipedia_tool)]
)

