from mcp.server.fastmcp import FastMCP
import os
import math
import sys
import time
import json

mcp =FastMCP('quickserver')

@mcp.tool()

def get_current_time() -> str:
    """
    Returns the current time in a human-readable format.
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print(get_current_time())


@mcp.tool()
def get_current_weather(location: str) -> str:
    """
    Returns the current weather for a given location.
    """
    # Placeholder implementation, replace with actual weather API call
    return f"The current weather in {location} is sunny."

@mcp.tool()
def get_list_of_restaurants(location: str) -> str:
    """
    Returns a list of restaurants in a given location.
    """
    # Placeholder implementation, replace with actual restaurant API call
    return f"Here are some restaurants in {location}: Restaurant A, Restaurant B, Restaurant C."

@mcp.tool()
def get_market_news() -> str:
    """
    Returns the latest market news.
    """
    # Placeholder implementation, replace with actual market news API call
    return "The latest market news is: Stock prices are rising." 

@mcp.tool()
def get_political_news() -> str:
    """
    Returns the latest political news.
    """
    # Placeholder implementation, replace with actual political news API call
    return "The latest political news is: Elections are coming up."

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution