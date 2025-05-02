import ast
import asyncio
from models import ExecuteToolInput, ToolCallResult, ParseFunctionCallInput, ParseFunctionCallOutput 

def parse_function_call(input: ParseFunctionCallInput) -> ParseFunctionCallOutput: 
    """Parses FUNCTION_CALL string into tool name and arguments."""
    # Extract the FUNCTION_CALL string from the input
    function_call_str = input.response.strip()
    
    # Check if the string starts with FUNCTION_CALL:
    if not function_call_str.startswith("FUNCTION_CALL:"):
        raise ValueError("Invalid FUNCTION_CALL format")
    
    # Remove the FUNCTION_CALL: prefix and split by '|'
    function_call_str = function_call_str[len("FUNCTION_CALL:"):].strip()
    parts = function_call_str.split('|')
    
    # Extract tool name and arguments
    tool_name = parts[0].strip()
    arguments_str = '|'.join(parts[1:]).strip()
    
    # Parse arguments into a dictionary
    arguments = {}
    for arg in arguments_str.split('|'):
        key, value = arg.split('=')
        key = key.strip()
        value = value.strip()
        # Convert value to appropriate type (int, float, str, list, dict)
        try:
            value = ast.literal_eval(value)  # Safely evaluate the string to its Python literal form
        except (ValueError, SyntaxError):
            pass  # Keep it as a string if evaluation fails
    
        arguments[key] = value
    
    return ParseFunctionCallOutput(output=(tool_name, arguments))


async def execute_tool(input: ExecuteToolInput) -> ToolCallResult:
    """Executes the tool with the provided arguments and returns the result."""
    # Get the session and tools from the input
    session = input.session 
    tools = input.tools
    response = input.response.strip()
    # parse the ParseFunctionCallInput response to get the tool name and arguments
    parsed_response = parse_function_call(ParseFunctionCallInput(response=response))
    tool_name, arguments = parsed_response.output
    # Find the tool in the list of tools    
    tool = next((tool for tool in tools if tool.name == tool_name), None)
    if tool is None:
        raise ValueError(f"Tool '{tool_name}' not found in the provided tools.")
    result = await tool.execute(session, **arguments)  # Execute the tool with the arguments
    return ToolCallResult(
        tool_name=tool_name,
        arguments=arguments,
        result=result,
        raw_response=response
    )


# Example usage
if __name__ == "__main__":
    # Example tool and session (replace with actual implementations)
    class ExampleTool:
        name = "add"
        
        async def execute(self, session, **kwargs):
            return {"result": "success", "data": kwargs}
    
    class ExampleSession:
        pass
    
    async def main():
        tools = [ExampleTool()]
        session = ExampleSession()
        
        # Example input
        input_data = ExecuteToolInput(
            session=session,
            tools=tools,
            response="FUNCTION_CALL: add|param1=10|param2=42"
        )
        
        # Execute the tool
        result = await execute_tool(input_data)
        print(result)  # Print the result of the tool execution

    # Run the async main function
    asyncio.run(main())








