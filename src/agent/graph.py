from langgraph.graph import StateGraph, END

from .state import PlanExecute
from .planner import plan_step  # Updated import
from .executor import execute_step
from .replanner import replan_step

# Define the graph
workflow = StateGraph(PlanExecute)

# Add the nodes
workflow.add_node("planner", plan_step)  # Updated function mapping
workflow.add_node("executor", execute_step)
workflow.add_node("replanner", replan_step)

# Set the entrypoint
workflow.set_entry_point("planner")

# Define the edges
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "replanner")

# Define conditional logic for continuing or finishing after replanning
def should_end(state: PlanExecute):  # Renamed and logic adjusted
    """Determines whether to end the process or continue to the agent (executor)."""
    if "response" in state and state["response"]:
        return END
    else:
        # Corresponds to 'agent' in the example, which is our 'executor' node
        return "executor"  

workflow.add_conditional_edges(
    "replanner",
    should_end,  # Updated function
    {
        END: END,
        "executor": "executor", 
    }
)


# Compile the graph
# memory = SqliteSaver.from_conn_string(":memory:") # Example for in-memory checkpointer
# graph = workflow.compile(checkpointer=memory)

# For local testing without a persistent checkpointer initially:
graph = workflow.compile(name="Plan and Execute Agent")

# To make the agent runnable, you'd typically expose `graph`
# and provide a way to invoke it, e.g., via a FastAPI endpoint or a CLI.

# The configuration part from the original template might need to be adapted
# if you want to make parts of this plan-and-execute agent configurable
# (e.g., the models used in planner, executor, replanner).
# For now, the models are hardcoded in their respective files.
