from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from .tools import tools

# Initialize the LLM for the execution agent. Ensure OPENAI_API_KEY is set.
# You might want to make the model configurable.
llm = ChatOpenAI(model="gpt-4-turbo-preview")

# Define the prompt for the execution agent
prompt = "You are a helpful assistant. Execute the current step of the plan."

# Create the ReAct agent executor
agent_executor = create_react_agent(llm, tools, prompt=prompt)

async def execute_step(state):
    task = state["plan"][0]
    # Invoke the agent executor with the current task
    # The input to the agent_executor should be a dictionary with a "messages" key,
    # containing a list of messages. Here, we'll pass the task as a user message.
    agent_response = await agent_executor.ainvoke({"messages": [("user", task)]})
    return {
        "past_steps": (task, agent_response["messages"][-1].content),
        "plan": state["plan"][1:]  # Remove the executed step from the plan
    }