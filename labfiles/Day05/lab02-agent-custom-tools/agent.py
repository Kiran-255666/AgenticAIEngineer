
import os
import json
from dotenv import load_dotenv

# Add references
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import AzureCliCredential
from openai.types.responses.response_input_param import (
    FunctionCallOutput,
    ResponseInputParam,
)

from functions import (
    verify_documents,
    calculate_financial_ratios,
    generate_risk_summary,
)


def main():

    # Clear the console
    os.system("cls" if os.name == "nt" else "clear")

    print("1. Starting agent...")

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    print("2. Environment variables loaded")

    # Connect to the project client
    print("3. Connecting to Azure AI Project...")

    with (
        AzureCliCredential() as credential,
        AIProjectClient(
            endpoint=project_endpoint,
            credential=credential
        ) as project_client,
        project_client.get_openai_client() as openai_client,
    ):

        print("4. Connected to Azure AI Project")

        # Define the document verification function tool
        document_tool = FunctionTool(
            name="verify_documents",
            description=(
                "Verify whether the required company registration "
                "and GST documents are available for a company. "
                "Retrieve the company details using its name from "
                "the sample company data file."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": (
                            "Name of the company whose documents "
                            "need to be verified."
                        ),
                    },
                },
                "required": [
                    "company_name",
                ],
                "additionalProperties": False,
            },
            strict=True,
        )

        # Define the financial ratio calculation tool
        ratio_tool = FunctionTool(
            name="calculate_financial_ratios",
            description=(
                "Calculate the current ratio, debt-to-equity ratio, "
                "and net profit margin for a company. Retrieve its "
                "financial data using the company name from the "
                "sample company data file."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": (
                            "Name of the company whose financial "
                            "ratios need to be calculated."
                        ),
                    },
                },
                "required": [
                    "company_name",
                ],
                "additionalProperties": False,
            },
            strict=True,
        )

        # Define the risk summary function tool
        summary_tool = FunctionTool(
            name="generate_risk_summary",
            description=(
                "Generate a credit-risk assessment summary for a "
                "company using its stored financial data and the "
                "configured risk thresholds."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": (
                            "Name of the company for which the "
                            "credit-risk summary is required."
                        ),
                    },
                },
                "required": [
                    "company_name",
                ],
                "additionalProperties": False,
            },
            strict=True,
        )

        # Create a new agent with the function tools
        print("5. Creating credit-risk agent...")

        agent = project_client.agents.create_version(
            agent_name="credit-risk-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
                You are a credit-risk assessment assistant.

                Help users perform basic credit-risk assessment tasks.

                Use the available tools when document verification,
                financial calculations, or risk summaries are required.

                Always use the company name provided by the user
                to retrieve the corresponding company information.

                Do not invent company documents or financial values.
                Use only the information returned by the tools.

                Explain the results clearly, including document
                availability, financial ratios, and risk levels.
                """,
                tools=[
                    document_tool,
                    ratio_tool,
                    summary_tool,
                ],
            ),
        )

        print("6. Agent created successfully")

        # Create a conversation for the chat session
        print("7. Creating conversation...")

        conversation = openai_client.conversations.create()

        print("8. Ready for input")

        # Create a list to hold function call outputs
        input_list: ResponseInputParam = []

        while True:

            user_input = input(
                "Enter a prompt for the credit-risk agent. "
                "Use 'quit' to exit.\nUSER: "
            ).strip()

            if user_input.lower() == "quit":
                print("Exiting chat.")
                break

            # Send a prompt to the agent
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": user_input,
                    }
                ],
            )

            # Retrieve the agent's response
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={
                    "agent_reference": {
                        "name": agent.name,
                        "type": "agent_reference",
                    }
                },
                input=input_list,
            )

            # Check the run status for failures
            if response.status == "failed":
                print(f"Response failed: {response.error}")
                continue

            # Process function calls
            for item in response.output:

                if item.type == "function_call":

                    result = None

                    print(f"Calling tool: {item.name}")

                    arguments = json.loads(item.arguments)

                    if item.name == "verify_documents":
                        result = verify_documents(**arguments)

                    elif item.name == "calculate_financial_ratios":
                        result = calculate_financial_ratios(**arguments)

                    elif item.name == "generate_risk_summary":
                        result = generate_risk_summary(**arguments)

                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=result,
                        )
                    )

            # Send function call outputs back to the model
            if input_list:

                response = openai_client.responses.create(
                    input=input_list,
                    previous_response_id=response.id,
                    extra_body={
                        "agent_reference": {
                            "name": agent.name,
                            "type": "agent_reference",
                        }
                    },
                )

                # Clear processed function call outputs
                input_list.clear()

            # Display the agent's response
            print(f"AGENT: {response.output_text}")

        # Delete the agent when done
        print("Deleting agent...")

        project_client.agents.delete_version(
            agent_name=agent.name,
            agent_version=agent.version,
        )

        print("Deleted agent.")


if __name__ == "__main__":
    main()
