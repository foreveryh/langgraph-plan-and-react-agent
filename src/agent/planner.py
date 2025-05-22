from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import HumanMessage # Added for plan_step input

from .state import PlanExecute  # Added for type hinting

class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """For the given objective, devise a concise, step-by-step plan. \
The level of detail and number of steps in this plan MUST be appropriate to the complexity of the objective. For very simple objectives (e.g., ones the LLM can answer in a single step or a few direct thoughts), the plan may only require one or two steps, or even directly state the action if no complex planning is needed. \
The plan should consist of individual, actionable tasks. If executed correctly, these tasks will yield the correct answer. \
Do NOT add any superfluous steps or unnecessary granularity. Focus on the most direct path to the solution. \
The result of the final step must be the final answer to the objective. \
Ensure each step has all necessary information for its execution – do not skip essential intermediary steps, but combine steps where logical for simple tasks or when a sequence of actions is trivial for the LLM. \
""",
        ),
        ("placeholder", "{messages}"),
    ]
)

# Use the specified model and temperature directly in the chain
planner = planner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Plan)

async def plan_step(state: PlanExecute):
    # The input to the planner is the user's objective, wrapped in a HumanMessage
    # as per the new state definition and example logic.
    plan = await planner.ainvoke({"messages": [HumanMessage(content=state["input"])]})
    return {"plan": plan.steps}