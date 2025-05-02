import asyncio
import time
import os
import datetime

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from perception import Perception, PerceptionInput, PerceptionOutput
from decision import generate_plan
from action import execute_tool

from models import * 


max_steps = 3



# Create a function to output the date and time in a specific format
def get_current_time() -> str:
    """Get the current date and time in a specific format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def main(user_input: str):
    try:
        print("[agent] Starting agent...")
        print(f"[agent] Current working directory: {os.getcwd()}")
        
        server_params = StdioServerParameters(
            command="python",
            args=["tools.py"],
            
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                print("Connection established, creating session...")
                try:
                    async with ClientSession(read, write) as session:
                        print("[agent] Session created, initializing...")
 
                        try:
                            await session.initialize()
                            print("[agent] MCP session initialized")

                            # Your reasoning, planning, perception etc. would go here
                            tools = await session.list_tools()
                            print("Available tools:", [t.name for t in tools.tools])
                            
                            # Get available tools
                            print("Requesting tool list...")
                            tools_result = await session.list_tools()
                            tools = tools_result.tools
                            tool_descriptions = "\n".join(
                                f"- {tool.name}: {getattr(tool, 'description', 'No description')}" 
                                for tool in tools
                            )
                            print("Available tools:", tool_descriptions)
                        except Exception as e:
                            print(f"[agent] Error during session initialization: {e}")
                except Exception as e:
                    print(f"[agent] Error creating session: {e}")
                
        except Exception as e:
            print(f"[agent] Error during connection: {e}")
    except Exception as e:
        print(f"[agent] Error in main function: {e}")

                            
# Example usage
if __name__ == "__main__":
    user_input = "What is the weather like today?"
    asyncio.run(main(user_input))
#               
                            


    

