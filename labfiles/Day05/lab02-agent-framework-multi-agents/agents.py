import asyncio
import os
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from agent_framework import Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential

load_dotenv()


async def main():
    data_folder = Path("data")

    # Load agent instructions
    document_verification_instructions = (
        data_folder / "document_verification_instructions.txt"
    ).read_text(encoding="utf-8")

    financial_analysis_instructions = (
        data_folder / "financial_analysis_instructions.txt"
    ).read_text(encoding="utf-8")

    credit_risk_instructions = (
        data_folder / "credit_risk_instructions.txt"
    ).read_text(encoding="utf-8")

    # Load credit-risk data
    company_documents = (
        data_folder / "company_documents.txt"
    ).read_text(encoding="utf-8")

    financial_data = (
        data_folder / "financial_data.txt"
    ).read_text(encoding="utf-8")

    credit_bureau_report = (
        data_folder / "credit_bureau_report.txt"
    ).read_text(encoding="utf-8")

    credit_risk_data = f"""
Company Documents:
{company_documents}

Financial Information:
{financial_data}

Credit Bureau Report:
{credit_bureau_report}
"""

    # Create the chat client
    credential = AzureCliCredential()

    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
    )

    # Create agents
    document_verification_agent = chat_client.as_agent(
        name="document_verification",
        instructions=document_verification_instructions,
    )

    financial_analysis_agent = chat_client.as_agent(
        name="financial_analysis",
        instructions=financial_analysis_instructions,
    )

    credit_risk_agent = chat_client.as_agent(
        name="credit_risk_assessment",
        instructions=credit_risk_instructions,
    )

    # Build sequential orchestration
    workflow = SequentialBuilder(
        participants=[
            document_verification_agent,
            financial_analysis_agent,
            credit_risk_agent,
        ],
        output_from="all",
    ).build()

    # Run the workflow
    result = await workflow.run(
        f"""
Perform a credit-risk assessment using the following information:

{credit_risk_data}
"""
    )

    # Display outputs
    outputs = result.get_outputs()
    i = 1

    for response in outputs:
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or (
                "assistant" if msg.role == "assistant" else "user"
            )

            print(
                f"{'-' * 60}\n"
                f"{i:02d} [{name}]\n"
                f"{msg.text}"
            )

            i += 1


if __name__ == "__main__":
    asyncio.run(main())