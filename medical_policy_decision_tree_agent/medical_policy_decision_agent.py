from google.adk.agents import LlmAgent
from google.genai import types

# from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from medical_policy_decision_tree_agent.prior_auth_decision_trees import (
    PriorAuthDecisionTrees,
)
from medical_policy_decision_tree_agent.tools.medical_policy_extractor_tool import (
    medical_policy_extractor,
)

# mcp_tools = MCPToolset(
#     connection_params=StreamableHTTPConnectionParams(url="http://localhost:8080")
# )
medical_policy_decision_agent = LlmAgent(
    name="medical_policy_extraction_agent",
    description="Extract and convert medical policies into prior authorization decision trees",
    model="gemini-3-pro-preview",
    instruction="""As an agent to create decision trees from medical policies for prior authorization, you process a given medical policy and extract prior authorization decision trees.

    **Here is the breakdown of your responsibility:**
    1. **Recieve Information:** You will be provided a url for a given online medical policy document.
    2. Extract the medical policy from the medical document policy url
    3. Carefully review all the decisions in the medical policy
    4. For each medical condition consider whether Prior Authorization is required based on the following:-
        - If "MEDICALLY NECESSARY" then Prior Authorization is required
        - If "INVESTIGATIONAL then Prior Authorization is not required
    5. Create a decision tree, which can be used by a medical practitioner or nurse to determine if a Prior Authorization is required""",
    tools=[medical_policy_extractor],
    output_key="extracted_pa",
    output_schema=PriorAuthDecisionTrees,
    # disallow_transfer_to_parent=True,
    # disallow_transfer_to_peers=True,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # More deterministic output
    ),
)
