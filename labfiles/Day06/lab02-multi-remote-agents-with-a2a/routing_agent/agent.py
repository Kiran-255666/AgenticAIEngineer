import asyncio
import json
import os
import time
import uuid
from collections.abc import Callable
from typing import Any

import httpx
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Task,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
)
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ListSortOrder, MessageRole
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

TaskCallbackArg = Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
TaskUpdateCallback = Callable[[TaskCallbackArg, AgentCard], Task]


class RemoteAgentConnections:
    """Hold the A2A connection information for a remote agent."""

    def __init__(self, agent_card: AgentCard, agent_url: str):
        self._httpx_client = httpx.AsyncClient(timeout=30)
        self.agent_client = A2AClient(self._httpx_client, agent_card, url=agent_url)
        self.card = agent_card

    def get_agent(self) -> AgentCard:
        return self.card

    async def send_message(self, message_request: SendMessageRequest) -> SendMessageResponse:
        return await self.agent_client.send_message(message_request)


class RoutingAgent:

    def __init__(self, task_callback: TaskUpdateCallback | None = None):
        self.task_callback = task_callback
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}
        self.agents: str = ""

        self.agents_client = AgentsClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True,
            ),
        )

        self.azure_agent = None
        self.current_thread = None
        self.azure_available = True

    @classmethod
    async def create(
        cls,
        remote_agent_addresses: list[str],
        task_callback: TaskUpdateCallback | None = None,
    ) -> "RoutingAgent":
        instance = cls(task_callback)
        await instance._async_init_components(remote_agent_addresses)
        return instance

    def list_remote_agents(self) -> str:
        if not self.remote_agent_connections:
            return "[]"

        lines = [f"{card.name}: {card.description}" for card in self.cards.values()]
        return "[\n  " + ",\n  ".join(lines) + "\n]"

    async def _async_init_components(self, remote_agent_addresses: list[str]) -> None:
        async with httpx.AsyncClient(timeout=30) as client:
            for address in remote_agent_addresses:
                card_resolver = A2ACardResolver(client, address)
                try:
                    card = await card_resolver.get_agent_card()
                    remote_connection = RemoteAgentConnections(agent_card=card, agent_url=address)
                    self.remote_agent_connections[card.name] = remote_connection
                    self.cards[card.name] = card
                except Exception:
                    continue

    def determine_agent(self, user_message: str) -> str:
        question = user_message.lower()

        if any(term in question for term in ["document", "registration", "gst", "certificate", "company documents"]):
            return "Document Verification Agent"

        if any(term in question for term in ["ratio", "financial", "revenue", "profit", "debt", "liability", "equity", "asset"]):
            return "Financial Analysis Agent"

        if any(term in question for term in ["assess", "credit", "risk", "industry", "bureau", "score"]):
            return "Credit Risk Assessment Agent"

        return "Credit Risk Assessment Agent"

    async def send_message(self, agent_name: str, task: str):
        if agent_name not in self.remote_agent_connections:
            raise ValueError(f"Agent {agent_name} not found")

        client = self.remote_agent_connections[agent_name]
        if not client:
            raise ValueError(f"Client not available for {agent_name}")

        message_id = str(uuid.uuid4())
        payload: dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": task}],
                "messageId": message_id,
            }
        }

        message_request = SendMessageRequest(
            id=message_id,
            params=MessageSendParams.model_validate(payload),
        )

        send_response: SendMessageResponse = await client.send_message(message_request=message_request)

        if not isinstance(send_response.root, SendMessageSuccessResponse):
            return None

        if not isinstance(send_response.root.result, Task):
            return None

        return send_response.root.result

    def create_agent(self):
        try:
            functions = FunctionTool({self.send_message})
            self.azure_agent = self.agents_client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                name="routing-agent",
                instructions=f"""
                You are an expert credit-risk routing agent.

                Your job is to analyze the user's question and route it to the most relevant remote credit-risk specialist.

                Available agents:
                {self.list_remote_agents()}

                Use the appropriate specialist agent for:
                - document verification questions
                - financial information and ratio questions
                - credit risk assessment and bureau questions

                If a question requires information that is not available in the documents, clearly state that it is unavailable.
                """,
                tools=functions.definitions,
            )

            self.current_thread = self.agents_client.threads.create()
            self.azure_available = True
            return self.azure_agent
        except Exception:
            self.azure_available = False
            self.azure_agent = None
            self.current_thread = None
            return None

    @staticmethod
    def _extract_task_text(task: Any) -> str:
        if task is None:
            return ""

        if hasattr(task, "status") and task.status is not None:
            status = task.status
            if hasattr(status, "message") and status.message is not None:
                message = status.message
                if hasattr(message, "parts"):
                    for part in message.parts:
                        if getattr(part, "root", None) is not None and hasattr(part.root, "text"):
                            return str(part.root.text)
                        if hasattr(part, "text"):
                            return str(part.text)
            if hasattr(status, "state"):
                return str(status.state)

        if hasattr(task, "artifacts"):
            for artifact in task.artifacts:
                if hasattr(artifact, "parts"):
                    for part in artifact.parts:
                        if getattr(part, "root", None) is not None and hasattr(part.root, "text"):
                            return str(part.root.text)
                        if hasattr(part, "text"):
                            return str(part.text)

        if hasattr(task, "model_dump"):
            try:
                return str(task.model_dump())
            except Exception:
                pass

        return ""

    async def process_user_message(self, user_message: str) -> str:
        if not self.azure_available or not self.azure_agent or not self.current_thread:
            agent_name = self.determine_agent(user_message)
            if agent_name not in self.remote_agent_connections:
                return "Unable to retrieve the required credit-risk information. Please verify that the assessment data files are available and try again."

            result = await self.send_message(agent_name, user_message)
            extracted = self._extract_task_text(result)
            if extracted:
                return extracted
            return "Unable to retrieve the required credit-risk information. Please verify that the assessment data files are available and try again."

        try:
            self.agents_client.messages.create(
                thread_id=self.current_thread.id,
                role=MessageRole.USER,
                content=user_message,
            )

            run = self.agents_client.runs.create(
                thread_id=self.current_thread.id,
                agent_id=self.azure_agent.id,
            )

            while run.status in ["queued", "in_progress", "requires_action"]:
                time.sleep(1)
                run = self.agents_client.runs.get(thread_id=self.current_thread.id, run_id=run.id)

                if run.status == "requires_action":
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []

                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        if function_name == "send_message":
                            try:
                                result = await self.send_message(
                                    agent_name=function_args["agent_name"],
                                    task=function_args["task"],
                                )
                                output = json.dumps(
                                    result.model_dump() if hasattr(result, "model_dump") else str(result)
                                )
                            except Exception:
                                output = json.dumps({"error": "Unable to retrieve the required credit-risk information."})
                        else:
                            output = json.dumps({"error": f"Unknown function: {function_name}"})

                        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

                    self.agents_client.runs.submit_tool_outputs(
                        thread_id=self.current_thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs,
                    )

            if run.status == "failed":
                last_error = getattr(run, "last_error", None)
                return f"Unable to process the request. The required credit-risk information could not be retrieved."

            messages = self.agents_client.messages.list(
                thread_id=self.current_thread.id,
                order=ListSortOrder.DESCENDING,
            )
            for msg in messages:
                if msg.role == MessageRole.AGENT and msg.text_messages:
                    last_text = msg.text_messages[-1]
                    return last_text.text.value

            return "No response received from the credit-risk agent."

        except Exception:
            return "Unable to retrieve the required credit-risk information. Please verify that the assessment data files are available and try again."


async def _get_initialized_routing_agent_sync() -> RoutingAgent:
    async def _async_main() -> RoutingAgent:
        routing_agent_instance = await RoutingAgent.create(
            remote_agent_addresses=[
                f"http://{os.environ['SERVER_URL']}:{os.environ['DOCUMENT_AGENT_PORT']}",
                f"http://{os.environ['SERVER_URL']}:{os.environ['FINANCIAL_AGENT_PORT']}",
                f"http://{os.environ['SERVER_URL']}:{os.environ['CREDIT_RISK_AGENT_PORT']}",
            ]
        )
        routing_agent_instance.create_agent()
        return routing_agent_instance

    return await _async_main()