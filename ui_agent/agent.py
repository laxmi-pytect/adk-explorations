from google.adk.agents.llm_agent import Agent

import os

filepath=os.getenv("FILEPATHs")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepath}/adk-exploration/genai_service_account.json"

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
