from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Union

from .planner import Plan
from .state import PlanExecute, get_default_state

# Response model as per the example
class Response(BaseModel):
    """Response to user."""
    response: str

# Act model as per the example
class Act(BaseModel):
    """Action to perform."""
    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer or continue working, use Plan."
    )

# Replanner prompt as per the example
replanner_prompt_template_text = """You are a replanning agent. Your role is to critically review the original objective, the previous plan, the executed steps (and their outcomes/failures), and the current draft document content (if any), and then generate an updated, actionable plan OR a final response if the objective is met.

Current UTC Date: {current_utc_date}
Current UTC Time: {current_utc_time}
Current Year: {current_year}
Use this time context when replanning time-sensitive tasks or research.

# Original Objective:
{input}

# Previous Plan (that led to the last executed step):
{plan}

# Steps Already Executed (and their outcomes, including any errors or statements of inability from the executor):
{past_steps}

# Current Draft Report Content (if any exists from previous steps; this might be empty or incomplete):
{current_draft_report}

Your replanning instructions:
1. **Analyze Execution History**: Carefully examine `past_steps`.
   * **Failures/Inabilities**: If a step failed, or if the executor stated it *cannot* perform a task as planned (e.g., "cannot access documents," "tool error"), you *MUST NOT* propose the exact same problematic step again. Devise a new approach:
     - Break the task down differently.
     - Plan a step to gather missing information (e.g., using TavilySearchResults).
     - If the task was to operate on a document it couldn't see, and `current_draft_report` is empty, the next step should be to *generate* that draft first.
   * **Successes**: Note successful outputs. If a step was meant to generate/update the draft report, assume its output is now reflected in the `current_draft_report` content provided above.

2. **Work with Current Draft Report**:
   * If `current_draft_report` IS POPULATED and the objective is to refine it or add to it: Your new plan steps should guide the executor to operate on this existing content (e.g., "Review the current_draft_report content for [specific criteria] and provide a revised version," or "Add a section on [X] to the current_draft_report content using information from previous search results.").
   * If `current_draft_report` IS EMPTY (or insufficient) and the objective requires a document: The next plan step should likely be to 'Generate an initial (or improved) draft of the [document type] on [topic] using information from `past_steps`.'

3. **Tool-Oriented Steps**: If further information is *genuinely needed* to progress, plan steps that use 'TavilySearchResults'. Do not just search vaguely; search for specific information needed for the *next logical step* (e.g., to fill a gap in `current_draft_report`).

4. **Updated Plan Focus**: The updated plan must ONLY list tasks that STILL NEED to be done.

5. **Conciseness and Appropriateness**: Ensure the updated plan's detail and step count are appropriate for the *remaining* work. If only one more action is needed, the plan should be just that one step.

6. **Completion Check**: Based on `Original Objective`, `past_steps`, and the state of `current_draft_report`, determine if the objective is fully met.
   * If YES: Your action should be `Response`. The `response` field of the `Response` action should contain the finalized `current_draft_report` content if the objective was to create a report, or the direct answer if it was a question.
   * If NO: Your action should be `Plan`, providing the next logical step(s).

7. **Avoid Stagnation**: If the same type of step has failed repeatedly, or if the plan isn't progressing, radically change the approach or simplify the goal for the next step.

8. **Direct Path**: Always aim for the most direct and logical next step(s) to complete the objective based on the current state.

For time-sensitive tasks:
1. Consider the current date and time when updating research or information gathering steps
2. Ensure updated steps account for the temporal context of the information needed
3. If historical data is needed, specify the relevant time period
4. For future-oriented tasks, consider the current time as the reference point
5. If any previous steps failed due to time-related issues, ensure the updated plan addresses these appropriately"""

replanner_prompt = ChatPromptTemplate.from_template(replanner_prompt_template_text)

# LLM and replanner chain as per the example
replanner = replanner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Act)

async def replan_step(state: PlanExecute):
    """Replans the existing plan based on execution feedback."""
    # Get default state values and update with current state
    current_state = get_default_state()
    current_state.update(state)
    
    input_data_for_replanner = {
        "input": current_state["input"],
        "plan": current_state.get("plan", []),  # Previous plan
        "past_steps": current_state["past_steps"],
        "current_draft_report": current_state.get("current_draft_report", ""),  # Pass current draft
        "current_utc_date": current_state["current_utc_date"],
        "current_utc_time": current_state["current_utc_time"],
        "current_year": current_state["current_year"],
    }
    
    output_act = await replanner.ainvoke(input_data_for_replanner)

    if isinstance(output_act.action, Response):
        return {
            "response": output_act.action.response,  # This is the final answer/report
            "plan": []  # Clear plan as it's finished
        }
    elif isinstance(output_act.action, Plan):
        return {
            "plan": output_act.action.steps,  # New plan steps
            "response": ""  # Clear any old final response from state if continuing
            # current_draft_report remains in state, it's not cleared by replanner
        }
    else:
        print(f"Warning: replan_step received an unexpected action type: {type(output_act.action)}. Defaulting to empty plan.")
        # Potentially problematic, agent might get stuck.
        # Consider if it should re-try replanning or enter an error state.
        return {"plan": [], "response": "Replanning resulted in an unexpected action type."}