from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from .tools import tools
from .state import PlanExecute, get_default_state

# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-4-turbo-preview")

async def execute_step(state: PlanExecute):
    # Get default state values and update with current state
    current_state = get_default_state()
    current_state.update(state)
    
    if not current_state["plan"]:
        return {
            "past_steps": [("No task to execute", "Plan was empty.")],
            "current_draft_report": current_state.get("current_draft_report")
        }

    task = current_state["plan"][0]
    
    time_context = (
        f"Current UTC Date is {current_state['current_utc_date']}, "
        f"Current UTC Time is {current_state['current_utc_time']} (Year: {current_state['current_year']})."
    )

    executor_system_prompt = f"""You are a diligent ReAct agent. Your goal is to execute a single given task using the tools available to you.

Available Tools:
- TavilySearchResults: Use this for searching the internet. When searching for recent information, ALWAYS use the current date and time to evaluate relevance: {time_context}.

Task Execution Guidelines:
1. Understand your current task fully.

2. If the task involves searching, use TavilySearchResults. Provide concise, factual summaries of information found.

3. If the task involves generating, reviewing, or refining document content:
   a. If you are asked to generate an initial draft, produce the text for that draft.
   b. If existing document text is provided to you as part of your input (labeled as 'EXISTING DRAFT CONTENT'), you MUST perform the required action (e.g., review, refine, add to, summarize) on THAT GIVEN TEXT. Your output should be the new or modified text for the document.

4. Your final answer for this step should be the direct result of executing the task (e.g., a summary of search findings, a generated piece of text, a revised document portion).

5. If you absolutely cannot perform the task with the provided tools or information, clearly state why and what is missing. Do not attempt tasks you are not equipped for (e.g., directly accessing external files unless a tool for it is listed).

6. Focus ONLY on the current task. Do not try to complete the entire overall plan."""

    # Create the ReAct agent executor with the enhanced system prompt
    agent_executor = create_react_agent(llm, tools, prompt=executor_system_prompt)

    current_task_description = current_state["plan"][0]
    
    # Prepare input for the ReAct agent, including draft report if relevant
    task_input_for_agent_messages = current_task_description
    current_draft_content = current_state.get("current_draft_report")

    # Heuristic to decide if the task implies working with the draft report
    task_is_document_related = any(kw in current_task_description.lower() for kw in [
        "draft", "report", "summary", "document", "review", "refine", "generate", 
        "write", "add to", "organize", "create", "compile", "structure"
    ])

    if task_is_document_related and current_draft_content:
        task_input_for_agent_messages = f"""Current Task: {current_task_description}

You MUST operate on or use the following EXISTING DRAFT CONTENT:
--- EXISTING DRAFT CONTENT START ---
{current_draft_content}
--- EXISTING DRAFT CONTENT END ---
"""
    elif task_is_document_related:  # Task is document related but no draft yet
        task_input_for_agent_messages = f"""Current Task: {current_task_description}
(There is no existing draft content yet. You are likely creating an initial draft if the task implies generation.)
"""

    agent_response_obj = await agent_executor.ainvoke(
        {"messages": [("user", task_input_for_agent_messages)]}
    )
    
    agent_final_output = agent_response_obj["messages"][-1].content

    # Determine if the output should update the current_draft_report
    new_draft_report_content = current_draft_content
    if task_is_document_related:  # If the task was about a document, assume its output is the new draft
        new_draft_report_content = agent_final_output
    
    return {
        "past_steps": [(current_task_description, agent_final_output)],
        "current_draft_report": new_draft_report_content,
    }