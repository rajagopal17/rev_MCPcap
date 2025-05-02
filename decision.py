from models import GeneratePlanInput,GeneratePlanOutput
from typing import Any, Dict, List, Optional, Tuple, Union
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging  
from perception import Perception, PerceptionInput, PerceptionOutput
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
    perceptionoutput= input_data.perception
    # Extracting user input, intent, and entities from the perception output    
    
    tool_descriptions = input_data.tool_descriptions

    tool_context = f"\nYou have access to the following tools:\n{tool_descriptions}" if tool_descriptions else ""

    prompt = f"""
    You are a decision-making agent. Based on the perception output and tool descriptions, generate a plan to achieve the user's goal.
    You have  access to tools {tool_context}. Your job is to solve the user's request step-by-step by:
    
    1. If using a tool, respond in this format:
        FUNCTION_CALL: tool_name|param1=value1|param2=value2
    2. After each step, self-verify your intermediate reasoning for sanity or consistency.
    3. If the result is final, respond in this format:
        FINAL_ANSWER: [your final result]
    4. If you're uncertain, a tool fails, or an answer cannot be computed reliably, explain why and stop with:
        ERROR: [explanation of the issue]
    5. Before solving, briefly identify the reasoning type involved (e.g., arithmetic, logic, lookup, planning, classification). This helps select the right tool or reasoning approach.

    Guidelines:
    - Respond using EXACTLY ONE of the formats above per step.
    - Do NOT include extra text, explanation, or formatting.
    - Use nested keys (e.g., input.string) and square brackets for lists.
    - You can reference these relevant memories:
    
    
    Input Summary:
    - User Input: {perceptionoutput.user_input}
    - User Intent: {perceptionoutput.user_intent}
    - Entities: {perceptionoutput.entities}
    
    
    ✅ Examples:
    - Reasoning Type: arithmetic  
    - FUNCTION_CALL: add|a=5|b=3
    - FUNCTION_CALL: strings_to_chars_to_int|input.string=INDIA
    - FUNCTION_CALL: int_list_to_exponential_sum|input.int_list=[73,78,68,73,65]
    - FINAL_ANSWER: [42]
    """

    
   
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    #debugging using logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.debug(f"Response from model: {response_text}\n\n") 
    logging.debug(f"tools_identified: {tool_descriptions}") 
    
    return GeneratePlanOutput(output=response_text)

#example usage
if __name__ == "__main__":
    async def main():
        perception = Perception()
        perception_input = PerceptionInput(user_input="addition of 42 and 41?")
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.debug(f"Perception input: {perception_input.user_input}\n\n")   
        perception_output = perception.extract_intent(perception_input)
        logging.debug(f"\nPerception output: {perception_output.user_input}, {perception_output.user_intent}, {perception_output.entities}\n\n")
        
        tool_descriptions = "get_current_time, get_current_weather, get_list_of_restaurants, get_market_news, get_political_news."
        
        generate_plan_input = GeneratePlanInput(perception=perception_output, tool_descriptions=tool_descriptions)
        plan_output = generate_plan(generate_plan_input)
        
        print(plan_output.output)  # Print the generated plan output

    asyncio.run(main())


