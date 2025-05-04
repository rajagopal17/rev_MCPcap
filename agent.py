import asyncio
import time
import os
import datetime
import logging

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from perception import extract_intent, PerceptionInput, PerceptionOutput
from decision import generate_plan
from action import execute_tool

from models import * 


max_steps = 3



# Create a function to output the date and time in a specific format
def get_current_time() -> str:
    """Get the current date and time in a specific format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def main(user_input: str):
    print("[agent] Starting agent...")
    print(f"[agent] Current working directory: {os.getcwd()}")
    
    server_params = StdioServerParameters(
        command="python",
        args=["tools.py"],
    )

    async with stdio_client(server_params) as (read, write):
        print(f"[agent] Connected to MCP server at {get_current_time()}")
        async with ClientSession(read,write) as session:
            print(f"[agent] Session started at {get_current_time()}")
            await session.initialize()
            print(f"[agent] Session initialized at {get_current_time()}")
            
            #Get the tools list from the MCP server
            tools_response = await session.list_tools()
            tools = tools_response.tools  # Access the tools list from the response
            print(f"[agent] Tools list: {tools}")
            tool_descriptions = "\n".join([f"{tool.name}: {getattr(tool, 'description', 'No description')}" for tool in tools])
            print(f"[agent] Tool descriptions: {tool_descriptions}")

            # get session id
            session_id = f"session-{int(time.time())}"
            print(f"[agent] Session ID: {session_id}")
            query = user_input
            step = 0
            while step < max_steps:
                print(f"[agent] Step {step + 1}/{max_steps} at {get_current_time()}")
                # Step 1: Perception - Extract user intent and entities
                perception_input = PerceptionInput(user_input=query)
                perception_output = extract_intent(perception_input)
                print(f"[agent] Perception output: {perception_output}")

                # Step 2: Decision - Generate a plan based on the perception output and tool descriptions
                decision_input = GeneratePlanInput(
                    perception=perception_output,
                    tool_descriptions=tool_descriptions
                )
                decision_output = generate_plan(decision_input)
                print(f"[agent] Decision output: {decision_output.output}")
                if decision_output.output.startswith("FINAL_ANSWER:"):
                    final_answer = decision_output.output[len("FINAL_ANSWER:"):].strip()
                    print(f"[agent] Final answer: {final_answer}")
                    break
                # Step 3: Action - Execute the tool call
                action_input = ExecuteToolInput(
                    session=session,
                    tools=tools,
                    response=decision_output.output
                )
                action_output = await execute_tool(action_input)
                print(f"[agent] Action output: {action_output}")
                #log("tool", f"{result.tool_name} returned: {result.result}")
                # Check for final answer or error in the action output
                if action_output.result.startswith("FINAL_ANSWER:"):
                    final_answer = action_output.result[len("FINAL_ANSWER:"):].strip()
                    print(f"[agent] Final answer: {final_answer}")
                    break
                elif action_output.result.startswith("ERROR:"):
                    error_message = action_output.result[len("ERROR:"):].strip()
                    print(f"[agent] Error encountered: {error_message}")
                    break


             






        

    
 


        
        


                   
                    
           
                     

                    




                            
# Example usage
if __name__ == "__main__":
    user_input = input("What is 10 added to 42?")
    asyncio.run(main(user_input))
#





