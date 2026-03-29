import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import traceback
#from google.exceptions import ExceptionGroup

PATH_TO_SERVER = os.path.abspath("./cart_server.py")


def unwrap_exception(exc, indent=0):
    prefix = "  " * indent
    if isinstance(exc, ExceptionGroup):
        print(f"{prefix}❌ ExceptionGroup: {exc.message}", file=sys.stderr)
        for sub in exc.exceptions:
            unwrap_exception(sub, indent + 1)
    else:
        print(f"{prefix}❌ {type(exc).__name__}: {exc}", file=sys.stderr)
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        for line in tb.splitlines():
            print(f"{prefix}  {line}", file=sys.stderr)


async def test():
    print(f"Connecting to server at: {PATH_TO_SERVER}", file=sys.stderr)
    print(f"Using Python: {sys.executable}", file=sys.stderr)
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[PATH_TO_SERVER],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            print("✅ stdio_client connected", file=sys.stderr)
            async with ClientSession(read, write) as session:
                print("✅ ClientSession created", file=sys.stderr)
                await session.initialize()
                print("✅ Session initialized", file=sys.stderr)
                tools = await session.list_tools()
                print(f"✅ Tools found: {[t.name for t in tools.tools]}", file=sys.stderr)
    except Exception as eg:
        print("\n[Test]: Unwrapping ExceptionGroup...", file=sys.stderr)
        unwrap_exception(eg)
        # for exc in eg.exceptions:

        #     print(f"❌ Sub-exception: {type(exc).__name__}: {exc}", file=sys.stderr)
        #     import traceback
        #     traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

asyncio.run(test())