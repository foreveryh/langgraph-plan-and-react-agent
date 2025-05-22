from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Initialize the LLM for planning. Ensure OPENAI_API_KEY is set.
# You might want to make the model configurable.
llm = ChatOpenAI(model="gpt-4-turbo-preview")

class Plan(BaseModel):
    """Plan to follow in future."""
    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

planner_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will help achieve the objective. Do not add any superfluous pre and post descriptive text. \
Return the plan as a list of strings.
""",
        ),
        ("placeholder", "{messages}"),
    ]
)

structured_llm_planner = llm.with_structured_output(Plan)
planner = planner_prompt_template | structured_llm_planner

async def get_plan(state):
    plan = await planner.ainvoke(state)
    return {"plan": plan.steps}