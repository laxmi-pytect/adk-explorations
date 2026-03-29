from google.adk.agents.llm_agent import Agent
from datetime import datetime
from google.adk.tools import FunctionTool, google_search_agent_tool, google_search

#from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool
import os

filepath=os.getenv('FILEPATH')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepath}/adk-exploration/genai_service_account.json"


def format_research_notes(topic: str, findings: str) -> dict:
    """Formats research findings into a document."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    document = f"""
    # Research Report: {topic}
    Generated: {timestamp}

    ## Findings
    {findings}
        """.strip()
    return {"status": "success", "document": document}

def extract_key_facts(text: str, num_facts: int = 5) -> list[str]:
    """Extract key facts from text (simplified)."""
    sentences = text.split('.')
    return [s.strip() for s in sentences if s.strip()][:num_facts]


# --- Agent Definition ---
search_agent = Agent(
    model="gemini-2.5-flash",
    name="search_specialist",
    instruction="You are a specialist in web search. Use the search tool to find facts. use the wikipedia , science journel like crediable sources . Also add the citations in the results",
    tools=[google_search] # This is the built-in search tool
)

# TODO: 1. Create an instance of the GoogleSearchAgentTool.
search_tool = google_search_agent_tool.GoogleSearchAgentTool(agent=search_agent)


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Conducts web search and compiles the data.',
    instruction="""
    You are research assistant, who gathers information and compiles the results
    1. for search_tool to find the information
    2. use extract_key_facts on search tool
    3. Use format_research_notes on the extracted facts
    4. Present final documents as the answer
    
    """,
    tools=[search_tool, FunctionTool(extract_key_facts), FunctionTool(format_research_notes)]
)



