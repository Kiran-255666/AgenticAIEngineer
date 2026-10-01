import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()


def load_file(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()


async def main():
    os.system("cls" if os.name == "nt" else "clear")

    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    company_data = load_file(data_dir / "data.txt")
    instructions = load_file(data_dir / "instructions.txt")

    await process_credit_risk_assessment(
        company_data,
        instructions,
    )


async def process_credit_risk_assessment(
    company_data: str,
    instructions: str,
):
    project = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    agent = project.agents.create_version(
        agent_name="credit-risk-assessment-agent",
        definition=PromptAgentDefinition(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            instructions=instructions,
        ),
    )

    openai = project.get_openai_client(
        agent_name=agent.name
    )

    conversation = openai.conversations.create()

    try:
        while True:
            user_prompt = input(
                "\nWhat would you like me to assess?\n"
                "Type 'quit' or 'exit' to stop.\n\n"
            )

            if user_prompt.strip().lower() in {"quit", "exit"}:
                break

            response = openai.responses.create(
                conversation=conversation.id,
                input=f"""
Company data:

{company_data}

Assessment request:

{user_prompt}
""",
            )

            print("\nCredit Risk Assessment")
            print("----------------------")
            print(response.output_text)

    except KeyboardInterrupt:
        print("\n\nExiting...")

    finally:
        project.agents.delete_version(
            agent_name=agent.name,
            agent_version=agent.version,
        )

        print("Agent deleted.")
        print("Run python agent-framework.py again to use the agent.")


if __name__ == "__main__":
    asyncio.run(main())