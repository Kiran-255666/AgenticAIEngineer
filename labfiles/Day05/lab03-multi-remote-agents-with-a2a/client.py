"""Client for the credit risk assessment application."""

import asyncio
import os

import requests
from dotenv import load_dotenv

load_dotenv()

server = os.environ["SERVER_URL"]
port = os.environ["ROUTING_AGENT_PORT"]

HELP_TEXT = """Example questions:
1. What company documents are available?
2. What financial information is available?
3. What are the financial ratios?
4. What is the external credit bureau score?
5. Assess the available credit-risk information.
"""


def send_prompt(prompt: str):
    url = f"http://{server}:{port}/message"
    payload = {"message": prompt}
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "No response from the credit risk assessment agent.")
        return "Unable to retrieve the required credit-risk information. Please verify that the assessment data files are available and try again."
    except Exception:
        return "Unable to retrieve the required credit-risk information. Please verify that the assessment data files are available and try again."


async def main():
    print("\nCredit Risk Assessment Agent")
    print("----------------------------")
    print("Enter your question or type 'help' for examples.")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nUser: ")
        if not user_input:
            continue

        command = user_input.strip().lower()
        if command == "quit":
            print("Goodbye.")
            break

        if command == "help":
            print(HELP_TEXT)
            continue

        response = send_prompt(user_input)
        print(f"\n{response}\n")


if __name__ == "__main__":
    asyncio.run(main())
