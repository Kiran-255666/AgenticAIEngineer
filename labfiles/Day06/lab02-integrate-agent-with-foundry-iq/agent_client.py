import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME")

if not project_endpoint or not agent_name:
    raise ValueError("PROJECT_ENDPOINT and AGENT_NAME must be set in .env file")

credential = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_managed_identity_credential=True
)

project_client = AIProjectClient(
    credential=credential,
    endpoint=project_endpoint
)

agent = project_client.agents.get(
    agent_name=agent_name
)

openai_client = project_client.get_openai_client()

conversation = openai_client.conversations.create()

print("Credit Risk Assessment Agent")
print("----------------------------")
print(f"Connected to: {agent.name}")
print("Ask questions about the credit-risk assessment.")
print("Type 'quit' or 'exit' to stop.\n")


def send_message_to_agent(user_message):
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={
            "agent_reference": {
                "name": agent.name,
                "type": "agent_reference"
            }
        },
        input=user_message
    )

    print("\nAgent:")
    print(response.output_text)


def main():
    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"quit", "exit"}:
                print("\nConversation ended.")
                break

            send_message_to_agent(user_input)

        except KeyboardInterrupt:
            print("\n\nConversation ended.")
            break

        except Exception as e:
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()