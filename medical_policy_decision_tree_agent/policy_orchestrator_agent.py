from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from medical_policy_decision_tree_agent.medical_policy_decision_agent import (
    medical_policy_decision_agent,
)

medical_policy_storage_mcp_tool = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url="http://localhost:8080/mcp")
)

policy_orchestrator_agent = LlmAgent(
    name="policy_orchestrator_agent",
    description="Orchestrates the extraction and storage of decision tree  for medical policies",
    model="gemini-3-pro-preview",
    tools=[
        agent_tool.AgentTool(agent=medical_policy_decision_agent),
        medical_policy_storage_mcp_tool,
    ],
    global_instruction="""You are an orchestrator agent that manages the process of extracting medical policies and storing the prior authorization decision trees.     
    
    **Your responsibilities include:**
    1. Receiving the initial input, which is a URL to a medical policy document.
    2. Delegate the task of extract and convert medical policies into prior authorization decision trees to the `medical_policy_extraction_agent` tool.
    3. Using the output from the `medical_policy_extraction_agent`, call the `medical_policy_storage_mcp_tool` to store the prior authorization decision trees.
    4.Output the boolean response from the `medical_policy_storage_mcp_tool`.""",
    output_key="pa_result",
)

root_agent = policy_orchestrator_agent


# 3. Using the output from the `medical_policy_extraction_agent`, add the medical policy using the `medical policy storage tool`.
#     4.Output whether the process was successful along with any relevant details.
