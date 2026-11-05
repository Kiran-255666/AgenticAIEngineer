"""
Advanced Azure AI Foundry Agent Evaluation Lab

This script evaluates an existing Credit Risk Assessment Agent
using a JSONL test dataset and built-in Azure AI evaluators.

Main flow:
1. Connect to the Foundry project.
2. Upload the credit-risk test dataset.
3. Create an evaluation with built-in evaluators.
4. Run the evaluation against the existing agent.
5. Monitor the evaluation run.
6. Print the Foundry portal report URL.
7. Save a local evaluation summary under results/.

Run from the lab root folder:

    python evaluate_agent_advanced.py
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator
from openai.types.eval_create_params import DataSourceConfigCustom


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    ROOT_DIR
    / "data"
    / "credit_risk_test_queries.jsonl"
)

RESULTS_DIR = ROOT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------

def require_env(name: str) -> str:
    """Return a required environment variable."""

    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            f"Check your .env file in the lab root folder."
        )

    return value


# ---------------------------------------------------------------------------
# Create clients
# ---------------------------------------------------------------------------

def build_clients():
    """Load configuration and create Foundry clients."""

    load_dotenv(ROOT_DIR / ".env")

    endpoint = require_env(
        "AZURE_AI_PROJECT_ENDPOINT"
    )

    model_deployment = require_env(
        "AZURE_AI_MODEL_DEPLOYMENT_NAME"
    )

    agent_name = require_env(
        "AGENT_NAME"
    )

    credential = DefaultAzureCredential()

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    )

    openai_client = project_client.get_openai_client()

    return (
        project_client,
        openai_client,
        model_deployment,
        agent_name,
    )


# ---------------------------------------------------------------------------
# Upload test dataset
# ---------------------------------------------------------------------------

def upload_dataset(project_client):
    """Upload the credit-risk JSONL dataset to Foundry."""

    print(
        "\n[1/5] Uploading credit-risk test dataset..."
    )

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {DATASET_PATH}"
        )

    dataset_name = os.getenv(
        "DATASET_NAME",
        "credit-risk-test-queries",
    )

    dataset_version = os.getenv(
        "DATASET_VERSION",
        datetime.now(timezone.utc).strftime(
            "%Y%m%d%H%M%S"
        ),
    )

    dataset = project_client.datasets.upload_file(
        name=dataset_name,
        version=dataset_version,
        file_path=str(DATASET_PATH),
    )

    print(
        f"  Dataset uploaded: "
        f"{dataset.name} v{dataset.version}"
    )

    print(
        f"  Dataset ID: {dataset.id}"
    )

    return dataset


# ---------------------------------------------------------------------------
# Create evaluation criteria
# ---------------------------------------------------------------------------

def create_testing_criteria(model_deployment):
    """Create built-in Azure AI evaluation criteria."""

    print(
        "\n[2/5] Configuring evaluation criteria..."
    )

    testing_criteria = [
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="Coherence",
            evaluator_name="builtin.coherence",
            initialization_parameters={
                "deployment_name": model_deployment
            },
            data_mapping={
                "query": "{{item.query}}",
                "response": "{{sample.output_text}}",
            },
        ),
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="Violence",
            evaluator_name="builtin.violence",
            data_mapping={
                "query": "{{item.query}}",
                "response": "{{sample.output_text}}",
            },
        ),
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="Task Adherence",
            evaluator_name="builtin.task_adherence",
            initialization_parameters={
                "deployment_name": model_deployment
            },
            data_mapping={
                "query": "{{item.query}}",
                "response": "{{sample.output_text}}",
            },
        ),
    ]

    print(
        "  Added built-in evaluator: builtin.coherence"
    )

    print(
        "  Added built-in evaluator: builtin.violence"
    )

    print(
        "  Added built-in evaluator: builtin.task_adherence"
    )

    return testing_criteria


# ---------------------------------------------------------------------------
# Create evaluation
# ---------------------------------------------------------------------------

def create_evaluation(
    openai_client,
    testing_criteria,
):
    """Create the Foundry evaluation."""

    print(
        "\n[3/5] Creating evaluation..."
    )

    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": [
                "query"
            ],
        },
        include_sample_schema=True,
    )

    evaluation = openai_client.evals.create(
        name=os.getenv(
            "EVALUATION_NAME",
            "Credit Risk Agent Evaluation",
        ),
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )

    print(
        f"  Evaluation created: "
        f"{evaluation.id}"
    )

    return evaluation


# ---------------------------------------------------------------------------
# Start evaluation run
# ---------------------------------------------------------------------------

def start_evaluation_run(
    openai_client,
    evaluation,
    dataset,
    agent_name,
):
    """Start an evaluation run against the existing agent."""

    print(
        "\n[4/5] Starting evaluation run..."
    )

    eval_run = openai_client.evals.runs.create(
        eval_id=evaluation.id,
        name=os.getenv(
            "EVALUATION_RUN_NAME",
            "Credit Risk Agent Evaluation Run",
        ),
        data_source={
            "type": "azure_ai_target_completions",
            "source": {
                "type": "file_id",
                "id": dataset.id,
            },
            "input_messages": {
                "type": "template",
                "template": [
                    {
                        "type": "message",
                        "role": "user",
                        "content": {
                            "type": "input_text",
                            "text": "{{item.query}}",
                        },
                    }
                ],
            },
            "target": {
                "type": "azure_ai_agent",
                "name": agent_name,
            },
        },
    )

    print(
        f"  Evaluation run created: "
        f"{eval_run.id}"
    )

    return eval_run


# ---------------------------------------------------------------------------
# Monitor evaluation
# ---------------------------------------------------------------------------

def monitor_evaluation(
    openai_client,
    evaluation,
    eval_run,
    agent_name,
    dataset,
):
    """Monitor the evaluation until it reaches a terminal state."""

    print(
        "\n[5/5] Monitoring evaluation run..."
    )

    terminal_statuses = {
        "completed",
        "failed",
        "canceled",
        "cancelled",
    }

    while True:

        run = openai_client.evals.runs.retrieve(
            run_id=eval_run.id,
            eval_id=evaluation.id,
        )

        print(
            f"  Current status: {run.status}"
        )

        if run.status in terminal_statuses:
            break

        time.sleep(5)

    report_url = getattr(
        run,
        "report_url",
        None,
    )

    result_counts = getattr(
        run,
        "result_counts",
        None,
    )

    print(
        "\n=========================================="
    )

    print(
        "Evaluation completed"
    )

    print(
        "=========================================="
    )

    print(
        f"Status: {run.status}"
    )

    print(
        f"Evaluation ID: {evaluation.id}"
    )

    print(
        f"Run ID: {eval_run.id}"
    )

    print(
        f"Report URL: {report_url}"
    )

    print(
        f"Result counts: {result_counts}"
    )

    summary = {
        "completed_at_utc": (
            datetime.now(timezone.utc)
            .isoformat()
        ),
        "evaluation_id": evaluation.id,
        "run_id": eval_run.id,
        "status": run.status,
        "report_url": report_url,
        "result_counts": str(result_counts),
        "agent_name": agent_name,
        "dataset": dataset.name,
        "dataset_version": dataset.version,
        "use_case": "Credit Risk Assessment",
        "evaluators": [
            "builtin.coherence",
            "builtin.violence",
            "builtin.task_adherence",
        ],
    }

    summary_file = (
        RESULTS_DIR
        / "evaluation_run_summary.json"
    )

    summary_file.write_text(
        json.dumps(
            summary,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Local summary saved to: "
        f"{summary_file}"
    )

    return run


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():

    (
        project_client,
        openai_client,
        model_deployment,
        agent_name,
    ) = build_clients()

    dataset = upload_dataset(
        project_client
    )

    testing_criteria = create_testing_criteria(
        model_deployment
    )

    evaluation = create_evaluation(
        openai_client,
        testing_criteria,
    )

    eval_run = start_evaluation_run(
        openai_client,
        evaluation,
        dataset,
        agent_name,
    )

    monitor_evaluation(
        openai_client,
        evaluation,
        eval_run,
        agent_name,
        dataset,
    )


if __name__ == "__main__":
    main()