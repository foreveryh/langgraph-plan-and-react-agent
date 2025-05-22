from typing import List, Tuple, TypedDict, Annotated
import operator

class PlanExecute(TypedDict):
    """State for the plan-and-execute agent."""
    input: str  # The user's input
    # The plan devised by the planner
    plan: List[str]
    # A list of (task, task_output) tuples for executed steps
    past_steps: Annotated[List[Tuple], operator.add]
    # The final response or summary from the agent
    response: str