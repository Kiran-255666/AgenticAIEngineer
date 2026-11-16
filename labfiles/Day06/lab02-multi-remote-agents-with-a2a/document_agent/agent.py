"""Document verification agent for the credit-risk assessment workflow."""

import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import Agent, ListSortOrder, MessageRole
from azure.identity import DefaultAzureCredential

from credit_risk_data import get_company_document_data, get_context_for_question, get_document_verification_rules


class DocumentVerificationAgent:

    def __init__(self):
        self.client = AgentsClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True,
            ),
        )
        self.agent: Agent | None = None
        self.azure_available = True

    async def create_agent(self) -> Agent | None:
        if self.agent:
            return self.agent

        try:
            self.agent = self.client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="document-verification-agent",
                instructions="""
                You are a credit-risk document verification specialist.

                Use only the provided company document file and the verification rules.
                Clearly report required documents, company-name consistency, and any missing information.
                Do not invent missing documents or values.
                """,
            )
            return self.agent
        except Exception:
            self.azure_available = False
            return None

    def _fallback_answer(self, user_message: str) -> str:
        company_docs = get_company_document_data()
        rules = get_document_verification_rules()

        sections = [
            "Document Verification",
            "---------------------",
            "Company Information",
        ]

        for key, value in company_docs.items():
            sections.append(f"{key}: {value}")

        sections.extend([
            "",
            "Verification Rules",
            rules,
        ])

        if "company name" in user_message.lower() or "match" in user_message.lower():
            sections.append("")
            sections.append("Company Name Match Check")
            registration_name = company_docs.get("Company name on Registration Certificate", "Not available in the provided documents.")
            gst_name = company_docs.get("Company name on GST Certificate", "Not available in the provided documents.")
            sections.append(f"Registration Certificate: {registration_name}")
            sections.append(f"GST Certificate: {gst_name}")
            if registration_name == gst_name:
                sections.append("Result: The company name matches across the required documents.")
            else:
                sections.append("Result: The company name does not match across the required documents.")

        sections.append("")
        sections.append("Assessment Summary")
        sections.append("The document verification status is based only on the documents available in the assessment data set. Missing information, if any, is explicitly reported as unavailable.")
        return "\n".join(sections)

    async def run_conversation(self, user_message: str) -> list[str]:
        if not self.agent and self.azure_available:
            try:
                await self.create_agent()
            except Exception:
                self.azure_available = False

        if not self.azure_available or self.agent is None:
            return [self._fallback_answer(user_message)]

        try:
            thread = self.client.threads.create()
            self.client.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content=f"Use only the provided credit-risk documents.\n\n{get_context_for_question(user_message)}\n\nQuestion: {user_message}",
            )

            run = self.client.runs.create_and_process(
                thread_id=thread.id,
                agent_id=self.agent.id,
            )

            if run.status == "failed":
                return [self._fallback_answer(user_message)]

            messages = self.client.messages.list(
                thread_id=thread.id,
                order=ListSortOrder.DESCENDING,
            )
            responses = []
            for msg in messages:
                if msg.role == MessageRole.AGENT and msg.text_messages:
                    for text_msg in msg.text_messages:
                        responses.append(text_msg.text.value)
                    break
            return responses if responses else [self._fallback_answer(user_message)]
        except Exception:
            return [self._fallback_answer(user_message)]


async def create_foundry_document_agent() -> DocumentVerificationAgent:
    agent = DocumentVerificationAgent()
    await agent.create_agent()
    return agent