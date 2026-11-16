import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from routing_agent.agent import RoutingAgent

load_dotenv()

routing_agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global routing_agent

    routing_agent = await RoutingAgent.create(
        [
            f"http://{os.environ['SERVER_URL']}:{os.environ['DOCUMENT_AGENT_PORT']}",
            f"http://{os.environ['SERVER_URL']}:{os.environ['FINANCIAL_AGENT_PORT']}",
            f"http://{os.environ['SERVER_URL']}:{os.environ['CREDIT_RISK_AGENT_PORT']}",
        ]
    )

    routing_agent.create_agent()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/message")
async def handle_message(request: Request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return {"error": "No message provided."}

    try:
        response = await routing_agent.process_user_message(user_message)
    except Exception:
        return {"error": "Unable to retrieve the required credit-risk information. Please verify that the assessment data files are available and try again."}

    return {"response": response}


@app.get("/health")
async def health_check():
    return {"status": "Routing agent is running."}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("ROUTING_AGENT_PORT"))
    uvicorn.run("routing_agent.server:app", host="127.0.0.1", port=port, reload=False)