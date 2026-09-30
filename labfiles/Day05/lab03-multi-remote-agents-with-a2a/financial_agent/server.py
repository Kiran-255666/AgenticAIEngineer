import os

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from financial_agent.agent_executor import create_foundry_agent_executor

load_dotenv()

host = os.environ["SERVER_URL"]
port = os.environ["FINANCIAL_AGENT_PORT"]

skills = [
    AgentSkill(
        id="analyze_financial_metrics",
        name="Analyze Financial Metrics",
        description="Calculates the standard financial ratios and summarizes the available financial information for credit-risk review.",
        tags=["financial data", "ratios", "debt", "liquidity"],
        examples=[
            "What financial information is available?",
            "What are the financial ratios?",
        ],
    )
]

agent_card = AgentCard(
    name="Financial Analysis Agent",
    description="A credit-risk financial specialist that reads the financial data and documents the available financial metrics and ratios for the assessment.",
    url=f"http://{host}:{port}/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=skills,
)

agent_executor = create_foundry_agent_executor(agent_card)
request_handler = DefaultRequestHandler(
    agent_executor=agent_executor,
    task_store=InMemoryTaskStore(),
)

a2a_app = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

routes = a2a_app.routes()


async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Financial Analysis Agent is running.")


routes.append(Route(path="/health", methods=["GET"], endpoint=health_check))
app = Starlette(routes=routes)


def main():
    uvicorn.run(app, host=host, port=int(port), log_level="warning")


if __name__ == "__main__":
    main()
