"""Credit risk assessment agent that reads assessment documents at runtime."""

import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import Agent, ListSortOrder, MessageRole
from azure.identity import DefaultAzureCredential

from credit_risk_data import (
    compute_financial_ratios,
    get_company_document_data,
    get_credit_bureau_data,
    get_credit_risk_rules,
    get_financial_data,
    get_context_for_question,
)


class CreditRiskAssessmentAgent:

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

    async def create_agent(self) -> Agent:
        if self.agent:
            return self.agent

        try:
            self.agent = self.client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="credit-risk-assessment-agent",
                instructions="""
                You are a credit-risk assessment specialist.

                Use only the information contained in the provided credit-risk documents.
                Never invent missing financial, document, or credit bureau information.
                If a value is not available in the provided information, clearly say it is unavailable.

                When summarizing, use clear sections such as:
                - Company Information
                - Financial Information
                - Financial Ratios
                - Credit Bureau Information
                - Industry Risk
                - Assessment Rules
                - Assessment Summary

                Distinguish between facts from the documents, calculations derived from the financial values, and any conclusion that is actually supported by the available information.
                """,
            )
            return self.agent
        except Exception:
            self.azure_available = False
            return None

    def _fallback_answer(self, user_message: str) -> str:
        question = user_message.lower()
        company_docs = get_company_document_data()
        financial = get_financial_data()
        bureau = get_credit_bureau_data()
        ratios = compute_financial_ratios()
        rules = get_credit_risk_rules()

        sections = []

        if any(term in question for term in ["document", "company documents", "registration", "gst", "certificate"]):
            sections.append("Company Information")
            for key, value in company_docs.items():
                sections.append(f"{key}: {value}")

        if any(term in question for term in ["financial", "ratio", "revenue", "profit", "debt", "liability", "equity", "asset"]):
            sections.append("")
            sections.append("Financial Information")
            for key, value in financial.items():
                if key in {"Current Assets", "Current Liabilities", "Total Debt", "Shareholders' Equity", "Revenue", "Net Profit"}:
                    sections.append(f"{key}: {value}")

            sections.append("")
            sections.append("Financial Ratios")
            for key, value in ratios.items():
                sections.append(f"{key}: {value}")

        if any(term in question for term in ["bureau", "credit", "industry", "risk", "score", "assessment"]):
            sections.append("")
            sections.append("Credit Bureau Information")
            for key, value in bureau.items():
                sections.append(f"{key}: {value}")

            sections.append("")
            sections.append("Industry Risk")
            sections.append(f"Industry: {bureau.get('Industry', 'Not available in the provided documents.')}")

            sections.append("")
            sections.append("Assessment Rules")
            sections.append(rules)

        if not sections:
            sections = [
                "Credit Risk Assessment",
                "----------------------",
                "Company Information",
            ]
            for key, value in company_docs.items():
                sections.append(f"{key}: {value}")

            sections.append("")
            sections.append("Financial Information")
            for key, value in financial.items():
                if key in {"Current Assets", "Current Liabilities", "Total Debt", "Shareholders' Equity", "Revenue", "Net Profit"}:
                    sections.append(f"{key}: {value}")

            sections.append("")
            sections.append("Financial Ratios")
            for key, value in ratios.items():
                sections.append(f"{key}: {value}")

            sections.append("")
            sections.append("Credit Bureau Information")
            for key, value in bureau.items():
                sections.append(f"{key}: {value}")

        result = "\n".join(sections)
        if "Assessment Summary" not in result:
            result += "\n\nAssessment Summary\n-------------------\n"
            result += "The information above is based on the documents available in the assessment data set. "
            result += "The financial ratios were calculated from the documented values, and the bureau information was taken from the credit bureau report. "
            result += "A final credit decision cannot be confirmed without additional information beyond the provided documents."
        return result

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
                content=f"Use only the provided credit-risk data.\n\n{get_context_for_question(user_message)}\n\nQuestion: {user_message}",
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
            responses: list[str] = []
            for msg in messages:
                if msg.role == MessageRole.AGENT and msg.text_messages:
                    for text_msg in msg.text_messages:
                        responses.append(text_msg.text.value)
                    break
            return responses if responses else [self._fallback_answer(user_message)]
        except Exception:
            return [self._fallback_answer(user_message)]


async def create_credit_risk_agent() -> CreditRiskAssessmentAgent:
    agent = CreditRiskAssessmentAgent()
    await agent.create_agent()
    return agent
