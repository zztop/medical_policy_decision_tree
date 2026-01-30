from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
import textwrap
from pydantic import TypeAdapter

from os import path, pathsep

from medical_policy_decision_tree_agent import medical_policy_decision_agent
from medical_policy_decision_tree_agent.policy_orchestrator_agent import (
    policy_orchestrator_agent,
)

from medical_policy_decision_tree_agent.prior_auth_decision_trees import (
    PriorAuthDecisionTrees,
)

import dotenv
import asyncio


async def main():

    dotenv.load_dotenv()

    agent_response = ""
    final_response = None

    # user_input = textwrap.dedent(
    #     """
    #         https://www.bluecrossma.org/medical-policies/sites/g/files/csphws2091/files/acquiadam-assets/121%20Closure%20Devices%20for%20Patent%20Foramen%20Ovale%20and%20Atrial%20Septal%20Defects%20prn.pdf
    #     """
    # ).strip()

    sample_path = path.join(path.dirname(path.realpath(__file__)), "..", "samples")
    user_input = path.join(
        sample_path,
        "121 Closure Devices for Patent Foramen Ovale and Atrial Septal Defects prn (1).pdf",
    )
    content = UserContent(parts=[Part(text=user_input)])

    runner = InMemoryRunner(agent=policy_orchestrator_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user1"
    )

    final_response_text = "Agent did not produce a final response."  # Default
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        print(event)
        if event and event.is_final_response():
            if event.content and event.content.parts and event.content.parts[0].text:
                final_response_text = event.content.parts[0].text
                print(f"Response is : {final_response_text}")

            # if agent_response:
            #     # final_response = TypeAdapter(bool).validate_json(agent_response)
            #     print(agent_response)
            #     # print(type(final_response))

            elif (
                event.actions and event.actions.escalate
            ):  # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            # Add more checks here if needed (e.g., specific error codes)
            break  # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")


if __name__ == "__main__":
    asyncio.run(main())
