import os
from dotenv import load_dotenv

from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from openai.types.responses.response_input_param import (
    McpApprovalResponse,
    ResponseInputParam,
)


# Load environment variables from .env file
load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


# Connect to the Azure AI Project
with (
    AzureCliCredential() as credential,
    AIProjectClient(
        endpoint=project_endpoint,
        credential=credential,
    ) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Initialize the MCP tool
    mcp_tool = MCPTool(
        server_label="credit-risk",
        server_url="https://your-mcp-server-url/mcp",
        require_approval="always",
    )

    # Create a credit-risk agent with the MCP tool
    agent = project_client.agents.create_version(
        agent_name="credit-risk-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=(
                "You are a credit-risk assessment assistant. "
                "Use the available MCP tools to verify company documents, "
                "calculate financial ratios, and generate credit-risk summaries. "
                "Use the appropriate tool when required and do not invent "
                "missing information."
            ),
            tools=[mcp_tool],
        ),
    )

    print(
        f"Agent created "
        f"(id: {agent.id}, name: {agent.name}, version: {agent.version})"
    )

    # Create a conversation
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Send the initial request
    response = openai_client.responses.create(
        conversation=conversation.id,
        input=(
            "Verify whether the company registration certificate and GST "
            "certificate are available for Apex Manufacturing Pvt Ltd."
        ),
        extra_body={
            "agent_reference": {
                "name": agent.name,
                "type": "agent_reference",
            }
        },
    )

    # Process MCP approval requests
    while True:
        input_list: ResponseInputParam = []

        for item in response.output:
            if item.type == "mcp_approval_request":
                if item.server_label == "credit-risk" and item.id:
                    input_list.append(
                        McpApprovalResponse(
                            type="mcp_approval_response",
                            approve=True,
                            approval_request_id=item.id,
                        )
                    )

        # No more approvals are required
        if not input_list:
            break

        # Send the approval response and retrieve the next response
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

    print(f"\nAgent response: {response.output_text}")

    # Clean up the agent version created during this run
    project_client.agents.delete_version(
        agent_name=agent.name,
        agent_version=agent.version,
    )

    print("Agent deleted")