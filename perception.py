import google.generativeai as genai
from models import PerceptionInput, PerceptionOutput
import os
from dotenv import load_dotenv
import logging
import sys


        # Initialize Gemini model
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_intent(input_data: PerceptionInput) -> PerceptionOutput:
    """Extract user intent and entities from the input query using llm model.
        Args:
            input_data (PerceptionInput): The input data containing user query. 
            OUTPUT:
            PerceptionOutput: The output data containing user intent and entities.
    """

    prompt = f"""
        Extract the core user intent from this query.

        Return the response as python dictionary without any additional text or code block formatting.

        user_intent: brief description of users intent 
        some examples: [travel_related_query, weather_query, query_related_to_physics, query_related_to_diets etc.]
        entities: list of entities in the query : example: ['Australia','AI','physics','capital']        

        Query: {input_data.user_input}
        """
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    response_text = response_text.replace('```', '').replace('python',"") # Remove code block formatting if present
        #debugging using logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.debug(f"Response from model: {response_text}")  
    try:
        response_dict = eval(response_text)  # Convert the string to a dictionary
        logging.debug(f"Parsed response: {response_dict}")
        user_intent = response_dict.get('user_intent', None)
        entities = response_dict.get('entities', None)
    except Exception as e:
        print(f"Error parsing response: {e}")
        user_intent = None
        entities = None
    return PerceptionOutput(
        user_input=input_data.user_input,
        user_intent=user_intent,
        entities=entities
        ) 


# Example usage
if __name__ == "__main__":
    # Example input data
    data = PerceptionInput(user_input="What is the capital of Australia?")
    output_data = extract_intent(input_data=data)

    
    # Print the output data
    print(output_data)
    


