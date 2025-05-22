from typing import List, Tuple, TypedDict, Annotated, Optional
import operator
import datetime

class PlanExecute(TypedDict, total=False):
    """State for the plan-and-execute agent."""
    input: str  # The user's input
    # The plan devised by the planner
    plan: List[str]
    # A list of (task, task_output) tuples for executed steps
    past_steps: Annotated[List[Tuple], operator.add]
    # The final response or summary from the agent
    response: str
    # Time context fields
    current_utc_date: str  # Current UTC date in YYYY-MM-DD format
    current_utc_time: str  # Current UTC time in HH:MM:SS format
    current_year: str  # Current year
    # New field for the draft report
    current_draft_report: Optional[str]  # Content of the report being drafted

def get_default_state() -> dict:
    """Get default state values."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return {
        "plan": [],
        "past_steps": [],
        "response": "",
        "current_utc_date": now_utc.strftime('%Y-%m-%d'),
        "current_utc_time": now_utc.strftime('%H:%M:%S'),
        "current_year": str(now_utc.year),
        "current_draft_report": None,
    }