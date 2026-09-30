"""Runs the A2A credit risk assessment services and starts the CLI."""

import asyncio
import os
import signal
import subprocess
import sys
import threading
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

server_url = os.environ["SERVER_URL"]
servers = [
    {
        "name": "Document Verification Agent",
        "module": "document_agent.server:app",
        "port": os.environ["DOCUMENT_AGENT_PORT"],
    },
    {
        "name": "Financial Analysis Agent",
        "module": "financial_agent.server:app",
        "port": os.environ["FINANCIAL_AGENT_PORT"],
    },
    {
        "name": "Credit Risk Assessment Agent",
        "module": "credit_risk_agent.server:app",
        "port": os.environ["CREDIT_RISK_AGENT_PORT"],
    },
    {
        "name": "Routing Agent",
        "module": "routing_agent.server:app",
        "port": os.environ["ROUTING_AGENT_PORT"],
    },
]

server_procs: list[subprocess.Popen] = []


async def wait_for_server_ready(server, timeout=30):
    async with httpx.AsyncClient() as client:
        start = time.time()
        while True:
            try:
                health_url = f"http://{server_url}:{server['port']}/health"
                response = await client.get(health_url, timeout=2)
                if response.status_code == 200:
                    return True
            except Exception:
                pass

            if time.time() - start > timeout:
                return False
            await asyncio.sleep(1)


async def run_client_main():
    from client import main as client_main
    await client_main()


async def main():
    print("Credit Risk Assessment Agent")
    print("----------------------------")
    print("Starting services...")

    for server in servers:
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            server["module"],
            "--host",
            server_url,
            "--port",
            str(server["port"]),
            "--log-level",
            "warning",
        ]

        process = subprocess.Popen(
            cmd,
            env=os.environ.copy(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            universal_newlines=True,
        )
        server_procs.append(process)

        ready = await wait_for_server_ready(server)
        if not ready:
            print(f"Unable to start {server['name']}.")
            for running_process in server_procs:
                if running_process.poll() is None:
                    if sys.platform == "win32":
                        running_process.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        running_process.terminate()
            sys.exit(1)

        print(f"{server['name']}: Ready")

    print()
    print("All services are ready.")
    print()
    print("Credit Risk Assessment Agent")
    print("Enter your question or type 'help' for examples.")
    print("Type 'quit' to exit.")

    try:
        await run_client_main()
    except Exception as exc:
        print(f"The credit risk assessment session ended unexpectedly: {exc}")
    finally:
        for process in server_procs:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()


if __name__ == "__main__":
    asyncio.run(main())
