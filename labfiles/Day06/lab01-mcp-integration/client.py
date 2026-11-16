import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import (
    FunctionCallOutput,
    ResponseInputParam,
)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Clear the console
os.system("cls" if os.name == "nt" else "clear")


# Load environment variables from .env file
load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


async def connect_to_server(exit_stack: AsyncExitStack):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None,
    )

    # Start the MCP server
    stdio_transport = await exit_stack.enter_async_context(
        stdio_client(server_params)
    )

    stdio, write = stdio_transport

    # Create an MCP client session
    session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )

    await session.initialize()

    # List available tools
    response = await session.list_tools()
    tools = response.tools

    print(
        "\nConnected to server with tools:",
        [tool.name for tool in tools],
    )

    return session


async def chat_loop(session):
    # Connect to the Azure AI Project
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        ) as project_client,
        project_client.get_openai_client() as openai_client,
    ):

        # Get the MCP tools available from the server
        response = await session.list_tools()
        tools = response.tools

        # Build a function for each MCP tool
        def make_tool_func(tool_name):
            async def tool_func(**kwargs):
                return await session.call_tool(
                    tool_name,
                    kwargs,
                )

            tool_func.__name__ = tool_name
            return tool_func

        # Store the functions in a dictionary
        functions_dict = {
            tool.name: make_tool_func(tool.name)
            for tool in tools
        }

        # Create FunctionTool definitions for the agent
        mcp_function_tools: FunctionTool = []

        for tool in tools:
            function_tool = FunctionTool(
                name=tool.name,
                description=tool.description,
                parameters=tool.input_schema,
                strict=True,
            )

            mcp_function_tools.append(function_tool)

        # Create the Credit Risk Agent
        agent = project_client.agents.create_version(
            agent_name="credit-risk-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
                You are a credit-risk assessment assistant.

                Use the available MCP tools to assist with credit-risk
                assessment tasks.

                You can help with:
                - Verifying required company documents
                - Calculating financial ratios
                - Generating credit-risk summaries

                Use the available MCP tools when they are relevant
                to the user's request.

                Do not invent missing financial, compliance,
                document, or credit information.
                """,
                tools=mcp_function_tools,
            ),
        )

        print(
            f"Agent created (id: {agent.id}, "
            f"name: {agent.name}, version: {agent.version})"
        )

        # Create a conversation for the chat session
        conversation = openai_client.conversations.create()

        try:
            while True:
                user_input = input(
                    "Enter a prompt for the credit-risk agent. "
                    "Use 'quit' to exit.\nUSER: "
                ).strip()

                if user_input.lower() == "quit":
                    print("Exiting chat.")
                    break

                # Add the user message to the conversation
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

                # Start with an empty list for this request
                input_list: ResponseInputParam = []

                # Get the agent response
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=input_list,
                    extra_body={
                        "agent_reference": {
                            "name": agent.name,
                            "type": "agent_reference",
                        }
                    },
                )

                # Check the response status
                if response.status == "failed":
                    print(f"Response failed: {response.error}")
                    continue

                # Process function calls
                for item in response.output:

                    if item.type != "function_call":
                        continue

                    function_name = item.name
                    kwargs = json.loads(item.arguments)

                    required_function = functions_dict.get(
                        function_name
                    )

                    if required_function is None:
                        print(f"Tool not found: {function_name}")
                        continue

                    print(f"Calling tool: {function_name}")

                    # Call the MCP tool
                    output = await required_function(**kwargs)

                    # Extract text from the MCP tool result
                    tool_output = "\n".join(
                        content.text
                        for content in output.content
                        if hasattr(content, "text")
                    )

                    # Send the MCP result back to the agent
                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=tool_output,
                        )
                    )

                # Send tool results back to the same conversation
                if input_list:
                    response = openai_client.responses.create(
                        conversation=conversation.id,
                        input=input_list,
                        extra_body={
                            "agent_reference": {
                                "name": agent.name,
                                "type": "agent_reference",
                            }
                        },
                    )

                print(f"AGENT: {response.output_text}")

        finally:
            # Delete the agent when the application exits
            print("Deleting agent...")

            project_client.agents.delete_version(
                agent_name=agent.name,
                agent_version=agent.version,
            )

            print("Deleted agent.")


async def main():
    exit_stack = AsyncExitStack()

    try:
        session = await connect_to_server(exit_stack)
        await chat_loop(session)

    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())