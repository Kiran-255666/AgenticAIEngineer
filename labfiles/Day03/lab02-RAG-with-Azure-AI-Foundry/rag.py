import os
from dotenv import load_dotenv
import glob

# Import namespaces
from openai import OpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider


def main():
    # Clear the console before starting the application.
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Load environment variables from the .env file.
        load_dotenv()

        # Get the Azure OpenAI endpoint from the environment configuration.
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        # Get the deployed model name from the environment configuration.
        model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

        # Create an Azure CLI credential provider for authentication.
        token_provider = get_bearer_token_provider(
            AzureCliCredential(),
            "https://ai.azure.com/.default"
        )

        # Initialize the Azure OpenAI client using token-based authentication.
        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        # Create the credit risk knowledge base and upload the PDF documents.
        print("Creating credit risk knowledge base and uploading documents...")

        # Create a vector store that will contain the credit risk documents.
        vector_store = openai_client.vector_stores.create(
            name="credit-risk-knowledge-base"
        )

        # Find all PDF files inside the knowledge_base folder.
        file_streams = [
            open(f, "rb")
            for f in glob.glob("knowledge_base/*.pdf")
        ]

        # Stop the program if no PDF documents are found.
        if not file_streams:
            print("No PDF files found in the knowledge_base folder!")
            return

        # Upload the PDFs and wait until processing is complete.
        file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )

        # Close all opened PDF file streams.
        for f in file_streams:
            f.close()

        # Display the number of successfully uploaded documents.
        print(
            f"Uploaded {file_batch.file_counts.completed} "
            "knowledge documents successfully."
        )

        # Store the previous response ID to maintain conversation context.
        last_response_id = None

        # Keep accepting questions until the user chooses to exit.
        while True:

            # Ask the user for a credit risk related question.
            input_text = input(
                '\nEnter a question (or type "quit" to exit): '
            ).strip()

            # Exit the application when the user types quit.
            if input_text.lower() == "quit":
                break

            # Ask the user to enter something if the input is empty.
            if not input_text:
                print("Please enter a question.")
                continue

            # Generate an answer using the credit risk knowledge base.
            response = openai_client.responses.create(
                model=model_deployment,

                # Define the assistant's role and response behavior.
                instructions="""
You are a Credit Risk Assessment Assistant.

Answer questions using the uploaded credit risk knowledge base.

Always use file_search to retrieve relevant information before answering.

Rules:
- Answer the user's question directly.
- Use only information supported by the knowledge base.
- Do not invent or assume information.
- Keep answers concise and specific.
- Do not provide unrelated information.
- Use bullet points when listing multiple items.
- Clearly show scores, credit limits, thresholds, payment terms, or other
  numerical values when they are relevant.
- Include conditions or exceptions when they directly affect the answer.
- If the knowledge base does not contain enough information, say:
  "The knowledge base does not provide enough information to answer this."

Response format:

Answer:
<direct answer>

Details:
- <only the most relevant supporting points>

Only include the Details section when additional information is useful.
Do not repeat the answer in the Details section.
Do not provide general explanations unless the user asks for them.
""",

                # Pass the user's question to the model.
                input=input_text,

                # Continue the previous conversation when available.
                previous_response_id=last_response_id,

                # Give the model access to the uploaded credit risk documents.
                tools=[
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id]
                    }
                ]
            )

            # Display the answer in a clean format for the lab demo.
            print("\n" + "=" * 80)
            print("CREDIT RISK ASSESSMENT")
            print("=" * 80)
            print(response.output_text)
            print("=" * 80)

            # Save the response ID for the next question.
            last_response_id = response.id

    # Catch and display any errors that occur during execution.
    except Exception as ex:
        print(f"\nError: {ex}")


# Run the main function when this file is executed directly.
if __name__ == '__main__':
    main()