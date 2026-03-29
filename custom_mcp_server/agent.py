from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import sys
import traceback

import os

filepath=os.getenv("FILEPATHs")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepath}/adk-exploration/genai_service_account.json"

#PATH_TO_SERVER = os.path.abspath("./custom_mcp_server/cart_server.py")
### us it for session_id
PATH_TO_SERVER = os.path.abspath("./custom_mcp_server/cart_server_with_session.py")

print(PATH_TO_SERVER)
def get_session_id(tool_context) -> dict:
    """Returns the current session ID."""
    session_id = tool_context.session_id
    print(f"[Client]: session_id = {session_id}", file=sys.stderr)
    return {"session_id": session_id}


root_agent = Agent(
    model='gemini-2.5-flash',
    name='shopping_agent',
    instruction="""You are a shopping assistant. 
    IMPORTANT: Always call get_session_id first to get the session_id
    Then pass that session_id when mcp tool call happens
    Help the user by adding items to their cart and showing them their cart contents.""",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,   ##'python3',
                    args=[PATH_TO_SERVER],
                ),
            ),
        )
    ],
)