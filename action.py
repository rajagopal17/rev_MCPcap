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
    """ Executes the FUNCTION_CALL using the MCP tool session.
    Args:
        input (ExecuteToolInput): The input data containing the FUNCTION_CALL string.
        Returns:
        ToolCallResult: The result of the tool execution.
    """ 
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
    if arguments_str:  # Only parse if there are arguments
        for arg in arguments_str.split('|'):
            if '=' in arg:
                key, value = arg.split('=')
                key = key.strip()
                value = value.strip()
                # Convert value to appropriate type (int, float, str, list, dict)
                try:
                    value = ast.literal_eval(value)  # Safely evaluate the string to its Python literal form
                except (ValueError, SyntaxError):
                    pass  # Keep it as a string if evaluation fails
                arguments[key] = value
    
    # Execute the tool using the MCP session
    result = await input.session.call_tool(tool_name, **arguments)
    if result.error:
        raise ValueError(f"Tool execution failed: {result.error}")
    
    return ToolCallResult(
        tool_name=tool_name,
        arguments=arguments,
        result=result.result,
        raw_response=result.raw_response
    )










