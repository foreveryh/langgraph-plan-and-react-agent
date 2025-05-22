from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from .tools import tools # Assuming tools are defined here as in the original example context
from .state import PlanExecute # Import PlanExecute for type hinting

# Choose the LLM that will drive the agent, as per the example
llm = ChatOpenAI(model="gpt-4-turbo-preview")

# Prompt for the agent, as per the example
prompt = "You are a helpful assistant."

# Create the ReAct agent executor, as per the example
agent_executor = create_react_agent(llm, tools, prompt=prompt)

async def execute_step(state: PlanExecute):
    plan = state["plan"]
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
    task = plan[0]
    # Format the task input for the agent as per the example
    task_formatted = f"""For the following plan:
{plan_str}\n\nYou are tasked with executing step {1}, {task}."""
    
    agent_response = await agent_executor.ainvoke(
        {"messages": [("user", task_formatted)]}
    )
    # Return structure as per the example (does not modify 'plan' here)
    return {
        "past_steps": [(task, agent_response["messages"][-1].content)],
    }