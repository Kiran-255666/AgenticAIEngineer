"""Financial analysis agent for the credit-risk assessment workflow."""

import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import Agent, ListSortOrder, MessageRole
from azure.identity import DefaultAzureCredential

from credit_risk_data import compute_financial_ratios, get_context_for_question, get_financial_analysis_rules, get_financial_data


class FinancialAnalysisAgent:

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
                name="financial-analysis-agent",
                instructions="""
                You are a credit-risk financial analysis specialist.

                Review the financial data in the provided documents and calculate the required ratios only when values are available.
                If any required financial data is missing, say it is unavailable in the provided documents.
                Do not invent financial values.
                """,
            )
            return self.agent
        except Exception:
            self.azure_available = False
            return None

    def _fallback_answer(self, user_message: str) -> str:
        financial = get_financial_data()
        ratios = compute_financial_ratios()
        rules = get_financial_analysis_rules()

        sections = [
            "Financial Information",
            "--------------------",
        ]

        for key, value in financial.items():
            if key in {"Current Assets", "Current Liabilities", "Total Debt", "Shareholders' Equity", "Revenue", "Net Profit"}:
                sections.append(f"{key}: {value}")

        sections.extend([
            "",
            "Financial Ratios",
        ])

        for key, value in ratios.items():
            sections.append(f"{key}: {value}")

        sections.extend([
            "",
            "Calculation Rules",
            rules,
            "",
            "Assessment Summary",
            "The ratios above are calculated only from values present in the provided financial document. Missing data, if any, is noted as unavailable.",
        ])
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
                content=f"Use only the provided financial data.\n\n{get_context_for_question(user_message)}\n\nQuestion: {user_message}",
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


async def create_foundry_financial_agent() -> FinancialAnalysisAgent:
    agent = FinancialAnalysisAgent()
    await agent.create_agent()
    return agent
