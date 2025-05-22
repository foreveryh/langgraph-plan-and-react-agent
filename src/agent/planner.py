from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import HumanMessage

from .state import PlanExecute, get_default_state

class Plan(BaseModel):
    """Plan to follow in future"""
    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

planner_prompt_template_text = """You are a planning agent. Your primary function is to devise a concise, step-by-step plan for the executor to achieve a given objective.

The executor has access to specific tools for information retrieval:
- TavilySearchResults: A tool to search the internet for up-to-date information.

The executor can also generate and refine text. If the objective involves creating a document (e.g., a report), the content of this document will be managed internally by the agent (you can think of it as being in a 'current_draft_report' field). Your plan should reflect this:
- Plan a step to 'Generate an initial draft of the [document type] on [topic]...' The executor's output for this step will populate the 'current_draft_report'.
- Subsequent steps can then be to 'Review and refine the current_draft_report content to ensure [criteria like accuracy, completeness, formatting]' or 'Add a section on [new sub-topic] to the current_draft_report content using information from previous search results.'

Current UTC Date: {current_utc_date}
Current UTC Time: {current_utc_time}
Current Year: {current_year}
Use this time context when planning time-sensitive tasks or research.

Your planning instructions:
1. **Tool-Oriented Steps**: When the objective involves finding information, your plan steps MUST involve instructing the executor to use the 'TavilySearchResults' tool (e.g., "Use TavilySearchResults to find information on [specific topic].").

2. **Document Creation/Refinement Steps**: If creating/refining a document:
   a. First, if no draft exists, plan a step like: 'Generate an initial draft of the [document type] on [topic], incorporating [specific information if available from prior steps].'
   b. If a draft exists (it will be in 'current_draft_report'), plan steps like: 'Review and refine the current_draft_report content for [criteria].' or 'Add a section on [X] to the current_draft_report content.'

3. **Conciseness and Appropriateness**: The level of detail and number of steps MUST be appropriate to the objective's complexity. For simple objectives (e.g., a single tool call, a direct answer), the plan should ideally be 1-2 steps.

4. **Actionable Tasks**: Plan individual, actionable tasks for the executor.

5. **No Superfluous Steps**: Do NOT add superfluous steps or unnecessary granularity. Focus on the most direct, efficient path using available capabilities.

6. **Final Answer Focus**: The result of the final planned step must be the final answer or the completed document content.

7. **Information and Combination**: Ensure steps have necessary info. Combine logical actions into minimal steps.

For time-sensitive tasks:
1. Consider the current date and time when planning research or information gathering steps
2. Ensure steps account for the temporal context of the information needed
3. If historical data is needed, specify the relevant time period
4. For future-oriented tasks, consider the current time as the reference point"""

planner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", planner_prompt_template_text),
        ("placeholder", "{messages}"),
    ]
)

planner = planner_prompt | ChatOpenAI(
    model="gpt-4o", temperature=0
).with_structured_output(Plan)

async def plan_step(state: PlanExecute):
    # Get default state values and update with current state
    current_state = get_default_state()
    current_state.update(state)
    
    plan = await planner.ainvoke({
        "messages": [HumanMessage(content=current_state["input"])],
        "current_utc_date": current_state["current_utc_date"],
        "current_utc_time": current_state["current_utc_time"],
        "current_year": current_state["current_year"],
    })
    return {"plan": plan.steps}