from typing import List, TypedDict, Annotated
import operator
from langchain_core.messages import BaseMessage

# Helper function to append messages to the state
def add_messages(left: List[BaseMessage], right: List[BaseMessage]) -> List[BaseMessage]:
    """Append messages to the list."""
    return left + right

class PlanExecute(TypedDict):
    """State for the plan-and-execute agent."""
    # The user's input, also used to accumulate agent's thoughts and tool outputs
    messages: Annotated[List[BaseMessage], add_messages]
    # The plan devised by the planner
    plan: List[str]
    # A list of (task, task_output) tuples for executed steps
    past_steps: Annotated[List[tuple], operator.add]
    # The final response or summary from the agent
    response: str