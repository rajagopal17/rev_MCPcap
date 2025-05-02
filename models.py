from pydantic import BaseModel
from typing import Any, List, Optional, Dict, Union

class PerceptionInput(BaseModel):
    user_input: str

class PerceptionOutput(BaseModel):
    user_input: str
    user_intent: Optional[str]
    entities: Optional[List[str]] 

# Input/Output models for decision
class GeneratePlanInput(BaseModel): 
    perception: PerceptionOutput
    #memory_items: MemoryOutput
    tool_descriptions: Optional[str] = None
    
class GeneratePlanOutput(BaseModel): 
    output: str

# Input/Output models for action
class ToolCallResult(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Union[str, list, dict]
    raw_response: Any

class ExecuteToolInput(BaseModel): 
    session: Any
    tools: list[Any]
    response: str
    
class ParseFunctionCallInput(BaseModel):
    response: str

class ParseFunctionCallOutput(BaseModel):
    output: tuple[str, Dict[str, Any]]
