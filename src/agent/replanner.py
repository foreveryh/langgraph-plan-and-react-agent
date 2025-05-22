from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Initialize the LLM for replanning. Ensure OPENAI_API_KEY is set.
# You might want to make the model configurable.
llm = ChatOpenAI(model="gpt-4-turbo-preview")

class Replan(BaseModel):
    """Updated plan to follow."""
    plan: List[str] = Field(
        description="updated plan to follow, should be in sorted order. If no updates are needed, return the original plan."
    )

replanner_prompt_template = ChatPromptTemplate.from_template(
    """For the given objective, previous plan, and feedback from execution, \
    update the plan if necessary. If no updates are needed, return the original plan. \
    Do not add any superfluous pre and post descriptive text. \
    Return the plan as a list of strings.

    Objective: {messages}
    Previous Plan: {plan}
    Feedback from Execution: {past_steps}
    """
)

structured_llm_replanner = llm.with_structured_output(Replan)
replanner = replanner_prompt_template | structured_llm_replanner

async def replan_step(state):
    output = await replanner.ainvoke(state)
    return {"plan": output.plan}