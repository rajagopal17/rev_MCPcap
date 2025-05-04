from models import GeneratePlanInput,GeneratePlanOutput
from typing import Any, Dict, List, Optional, Tuple, Union
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging  
from perception import extract_intent, PerceptionInput, PerceptionOutput
import sys
import asyncio

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

#create a function to generate a plan based on the perception output and tool descriptions
def generate_plan(input_data: GeneratePlanInput) -> GeneratePlanOutput:
    """Generate a plan based on the perception output and tool descriptions.
    
    Args:
        input_data (GeneratePlanInput): The input data containing perception output and tool descriptions.
        
    Returns:
        GeneratePlanOutput: The generated plan.
    """
    perceptionoutput = input_data.perception
    tool_descriptions = input_data.tool_descriptions

    tool_context = f"\nYou have access to the following tools:\n{tool_descriptions}" if tool_descriptions else ""

    prompt = f"""
    You are a decision-making agent. Based on the perception output and tool descriptions, generate a plan to achieve the user's goal.
    You have access to tools {tool_context}. Your job is to solve the user's request step-by-step by:
    
    1. If using a tool, ONLY respond with:
        FUNCTION_CALL: tool_name|param1=value1|param2=value2
    2. If the result is final, ONLY respond with:
        FINAL_ANSWER: [your final result]
    3. If you're uncertain or an answer cannot be computed, ONLY respond with:
        ERROR: [explanation of the issue]

    IMPORTANT: 
    - Your response must start with exactly one of: FUNCTION_CALL:, FINAL_ANSWER:, or ERROR:
    - Do not include any other text or explanation in your response
    - For function calls, use | to separate parameters
    - For string values, do not use quotes unless they're part of the string

    Input Summary:
    - User Input: {perceptionoutput.user_input}
    - User Intent: {perceptionoutput.user_intent}
    - Entities: {perceptionoutput.entities}

    ✅ Valid Response Examples:
    FUNCTION_CALL: get_current_time
    FUNCTION_CALL: get_current_weather|location=New York
    FUNCTION_CALL: get_list_of_restaurants|location=New York
    FUNCTION_CALL: get_market_news|topic=stock market
    FINAL_ANSWER: The result is 42
    ERROR: No appropriate tool found for this request
    """
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    # Ensure response starts with one of the valid prefixes
    valid_prefixes = ["FUNCTION_CALL:", "FINAL_ANSWER:", "ERROR:"]
    if not any(response_text.startswith(prefix) for prefix in valid_prefixes):
        # Default to ERROR if response format is invalid
        response_text = f"ERROR: Invalid response format - {response_text}"
    
    logging.debug(f"Response from model: {response_text}")
    logging.debug(f"Tools available: {tool_descriptions}")
    
    return GeneratePlanOutput(output=response_text)

#example usage
if __name__ == "__main__":
    output = generate_plan(GeneratePlanInput(
        perception=PerceptionOutput(user_input="What is 10 added to 20", user_intent="math_query", entities=["10", "20"]),
        tool_descriptions="add"
    ))
    print(output.output)






