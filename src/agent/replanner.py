from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Union

from .planner import Plan  # Import Plan model from planner.py, assuming it's compatible
from .state import PlanExecute # Import PlanExecute for type hinting

# Response model as per the example
class Response(BaseModel):
    """Response to user."""
    response: str

# Act model as per the example
class Act(BaseModel):
    """Action to perform."""
    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )

# Replanner prompt as per the example
replanner_prompt = ChatPromptTemplate.from_template(
    """Review the original objective, the original plan, and the steps already executed along with their outcomes. Then, update the plan.

# Original Objective:
{input}

# Original Plan:
{plan}

# Steps Already Executed (and their outcomes, if relevant):
{past_steps}

Instructions for Updating the Plan:
1.  The updated plan must be a simple, step-by-step guide consisting of only those tasks that STILL NEED to be done to achieve the Original Objective. Do not include previously completed steps in the new plan.
2.  Critically evaluate the outcomes of the ** Steps Already Executed **. If any step failed or produced unexpected results, ensure the updated plan addresses these issues effectively.
3.  The level of detail and number of steps in this updated plan MUST be appropriate to the complexity of the *remaining* work. For objectives that are now very close to completion, or were simple to begin with, the updated plan may only require one or two further steps, or even a direct action if appropriate.
4.  Each step must be actionable and, if executed correctly, contribute directly to yielding the final answer.
5.  Do NOT add any superfluous steps or unnecessary granularity to the updated plan. Focus on the most direct path to the solution based on the current situation.
6.  The result of the final step in the updated plan must be the final answer to the Original Objective.
7.  Ensure each new step has all necessary information for its execution – do not skip essential intermediary steps, but combine steps where logical for simple remaining tasks or when a sequence of actions is trivial for the LLM.
8.  If, after reviewing the executed steps and their outcomes, you determine that no more steps are needed and the objective is complete, or the answer can be directly provided, then respond with the final answer or a completion message. Otherwise, provide the updated plan.
"""
)

# LLM and replanner chain as per the example
replanner = replanner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Act)

async def replan_step(state: PlanExecute):
    """Replans the existing plan based on execution feedback."""
    # The replanner prompt expects 'input', 'plan', and 'past_steps' directly from the state.
    output = await replanner.ainvoke(state)  # output is an instance of Act

    # Check the type of action in the Act model
    if isinstance(output.action, Response):
        # If it's a Response, the plan is considered complete
        return {"response": output.action.response}
    elif isinstance(output.action, Plan):
        # If it's a Plan, return the updated plan's steps
        return {"plan": output.action.steps}
    else:
        # Fallback or error handling, though ideally Act should always contain Response or Plan.
        # This case should be rare if Pydantic models and LLM output are aligned.
        # For safety, return current plan if action is not recognized.
        # Matching original example's implicit assumption, but adding a warning for robustness.
        print(f"Warning: replan_step received an unexpected action type: {type(output.action)}. Returning current plan.")
        return {"plan": state.get("plan", [])}