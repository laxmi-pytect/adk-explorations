# In cart_server.py (Starter Code)
import asyncio
import json
from mcp import types as mcp_types
from mcp.server.lowlevel import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import sys



# --- Server State ---

SESSION_CARTS = []

# --- MCP Server Setup ---
app = Server("shopping_cart_mcp_server")

@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """Defines the 'menu' of tools our server offers."""
    print("[Server]: Client asked for the list of tools.")
    
    add_item_tool = mcp_types.Tool(name='add_item_to_cart', description='helps in adding items to cart', 
                                   inputSchema = {
                                       "type": "object",
                                     "properties": {"item": {"type": "string", "description": "The item to add to the cart."}},
                                    "required": ["item"],},)


    view_cart_tool = mcp_types.Tool(name='view_cart', description='helps in listing items in the cart', 
                                    inputSchema={"type": "object", "properties": {}},)
    
    return [add_item_tool, view_cart_tool]

@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    """Handles the execution of our tools."""
    #ctx = get_context()
    #session_id = id(ctx.session)
    #print(f"[Server]: Client called tool '{name}' for session '{session_id}'.")
    #print("sessionid", session_id)

    # if session_id not in SESSION_CARTS:
    #     SESSION_CARTS[session_id] = []

    if name == "add_item_to_cart":
        item = arguments.get("item")
        if item:
            #SESSION_CARTS[session_id].append(item)
            SESSION_CARTS.append(item)
            response_text = json.dumps({"status": "success", "message": f"Added '{item}' to the cart."}) 
        else:
            response_text = json.dumps({"status": "error", "message": "No item provided."})
        
        return [mcp_types.TextContent(type="text", text=response_text)]
    elif name == "view_cart":
        #cart_contents = SESSION_CARTS[session_id]
        response_text = json.dumps({"status": "success", "cart": SESSION_CARTS})
        return [mcp_types.TextContent(type="text", text=response_text)]

    else:
        response_text = json.dumps({"status": "error", "message": f"Tool '{name}' not found."}) 
        return [mcp_types.TextContent(type="text", text=response_text)]
   


# --- MCP Server Runner (Provided for you) ---
async def run_mcp_stdio_server():
    print("[Server]: Entered run_mcp_stdio_server", file=sys.stderr)
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("[Server]: Waiting for client...", file=sys.stderr)
        print("[Server]: Waiting for a client to connect...")
        print(f"[Server]: Running with {sys.executable}", file=sys.stderr)
        await app.run(read_stream, write_stream, InitializationOptions(server_name=app.name, server_version="0.1.0",  
                capabilities=mcp_types.ServerCapabilities(tools=mcp_types.ToolsCapability(listChanged=False),)))
        print("[Server]: app.run() returned", file=sys.stderr) 

if __name__ == "__main__":
    print("[Server]: Starting Shopping Cart MCP Server...")

    print("[Server]: Starting...", file=sys.stderr)
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        print("\n[Server]: Shutting down.")
        print("\n[Server]: Shutting down.", file=sys.stderr)
    