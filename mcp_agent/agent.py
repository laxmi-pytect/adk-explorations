from google.adk.agents.llm_agent import Agent

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

import os

filepath=os.getenv("FILEPATH")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{filepath}/adk-exploration/genai_service_account.json"
TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")
print(TARGET_FOLDER_PATH)


root_agent = Agent(
    model='gemini-2.5-flash',
    name='filesystem_agent',
    description='You are a helpful assistant that can interact with a user\'s local file system. You can list files and read their content.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[MCPToolset(
        connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
             command='npx',
             args=["-y",   "@modelcontextprotocol/server-filesystem",os.path.abspath(TARGET_FOLDER_PATH),]
             ),
        ),
        tool_filter=['list_directory', 'read_file'],    
        )
        ],     
)



