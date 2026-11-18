"""
Azure AI Foundry Agent Evaluation Lab

Evaluates an existing Credit Risk Assessment Agent using a JSONL test
dataset and built-in Azure AI evaluators.

Flow:
0. Load config and ask for a unique run name (checked against Foundry).
1. Upload the test dataset (reused if already uploaded).
2. Configure built-in evaluators.
3. Create the evaluation.
4. Start the run against the existing agent.
5. Wait for it to finish, print the report URL, save one summary file.

Built to be run by many people at the same time against one Foundry project.

Run from the lab root folder:

    python evaluate_agent_advanced.py
"""

import hashlib
import json
import os
import random
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from itertools import islice
from pathlib import Path

import openai
from dotenv import load_dotenv
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ServiceRequestError,
    ServiceResponseError,
)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator
from openai.types.eval_create_params import DataSourceConfigCustom


# ---------------------------------------------------------------------------
# Paths and settings
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
DATASET_PATH = ROOT_DIR / "data" / "credit_risk_test_queries.jsonl"
RESULTS_DIR = ROOT_DIR / "results"

MIN_NAME_LENGTH = 7
NAME_PATTERN = re.compile(r"^[a-z0-9_-]+$")

POLL_SECONDS = 10               # base wait between status checks
MAX_WAIT_SECONDS = 30 * 60      # stop waiting after 30 minutes
STARTUP_JITTER_SECONDS = 10     # random delay so 50 people don't start together
MAX_RETRIES = 5                 # attempts per Azure call on busy/transient errors
MAX_EVALS_TO_CHECK = 1000
TERMINAL_STATUSES = {"completed", "failed", "canceled", "cancelled"}


def say(message: str = "") -> None:
    print(message, flush=True)


# ---------------------------------------------------------------------------
# Error classification and retry
# ---------------------------------------------------------------------------

def status_of(exc: Exception):
    """HTTP status code of an error, if it has one."""
    return getattr(exc, "status_code", None)


def is_rate_limit(exc: Exception) -> bool:
    return isinstance(exc, openai.RateLimitError) or status_of(exc) == 429


def is_transient(exc: Exception) -> bool:
    """Errors that usually go away if we wait and try again."""

    if is_rate_limit(exc):
        return True

    if isinstance(
        exc,
        (
            openai.APIConnectionError,   # includes timeouts
            openai.InternalServerError,
            ServiceRequestError,
            ServiceResponseError,
        ),
    ):
        return True

    return isinstance(exc, HttpResponseError) and status_of(exc) in (
        408, 500, 502, 503, 504,
    )


def retry(call, what: str = "request", only_rate_limit: bool = False):
    """Run call(), retrying with backoff when Azure is busy.

    only_rate_limit=True is used for create calls: a 429 means the request
    was not processed, so retrying is safe. Other errors might have created
    the object already, so they are not retried (avoids duplicates).
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return call()
        except Exception as exc:
            retryable = is_rate_limit(exc) if only_rate_limit else is_transient(exc)
            if not retryable or attempt == MAX_RETRIES:
                raise

            wait = min(60, 3 * 2 ** (attempt - 1)) + random.uniform(0, 3)
            say(
                f"  Azure is busy ({what}). "
                f"Retrying in {wait:.0f}s ({attempt}/{MAX_RETRIES - 1})..."
            )
            time.sleep(wait)


def explain_error(exc: Exception) -> str:
    """Turn a known error into a plain-language hint. Empty if unknown."""

    text = str(exc).lower()
    status = status_of(exc)

    if isinstance(exc, (ClientAuthenticationError, openai.AuthenticationError)) or status == 401:
        return (
            "Azure login failed or expired. Run 'az login' with the lab "
            "account, then try again."
        )

    if isinstance(exc, openai.PermissionDeniedError) or status == 403:
        return (
            "Your account lacks permission on this project. Ask for the "
            "'Azure AI User' role on the Foundry project."
        )

    if is_rate_limit(exc):
        return (
            "Azure is busy (rate limit), probably because many people are "
            "running at the same time. Wait 1-2 minutes and run again."
        )

    if "model resources are not found" in text:
        return (
            "Foundry cannot find your model deployment. Set "
            "AZURE_AI_MODEL_DEPLOYMENT_NAME in .env to the exact "
            "Deployment name from Foundry > Models + endpoints "
            "(the deployment name, not the model name)."
        )

    if isinstance(exc, (ResourceNotFoundError, openai.NotFoundError)) or status == 404:
        return (
            "Resource not found. Check AZURE_AI_PROJECT_ENDPOINT in .env. "
            "It must look like "
            "https://<account>.services.ai.azure.com/api/projects/<project>. "
            "Also make sure AGENT_NAME is an agent that exists."
        )

    if isinstance(exc, FileNotFoundError):
        return "A required file is missing. Check the path in the message."

    if isinstance(exc, ValueError) and "environment variable" in text:
        return "Open the .env file in the lab root folder and fill in the value."

    if isinstance(exc, (openai.APIConnectionError, ServiceRequestError)):
        return "Could not reach Azure. Check your internet connection or VPN, then run again."

    return ""


def show_error(exc: Exception, name_used: bool = False) -> None:
    say("\n" + "=" * 60)
    say(" Something went wrong")
    say("=" * 60)
    say(f" Error : {type(exc).__name__}")

    for line in (str(exc).strip() or "(no message)").splitlines():
        say(f"         {line}")

    hint = explain_error(exc)
    if hint:
        say(f"\n How to fix:\n   {hint}")

    if name_used:
        say(
            "\n Your run name is now taken in Foundry. "
            "When you run again, use the next number."
        )

    if os.getenv("EVAL_DEBUG"):
        say("\n" + traceback.format_exc())


# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------

def require_env(name: str) -> str:
    value = (os.getenv(name) or "").strip().strip('"').strip("'")

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            "Add it to the .env file in the lab root folder."
        )

    return value


def validate_endpoint(endpoint: str) -> None:
    if "/api/projects/" not in endpoint or "/openai/" in endpoint:
        raise ValueError(
            "AZURE_AI_PROJECT_ENDPOINT looks wrong: "
            f"{endpoint}\n"
            "  Expected: https://<account>.services.ai.azure.com"
            "/api/projects/<project>\n"
            "  Copy it from Foundry > your project > Overview."
        )


def build_clients():
    load_dotenv(ROOT_DIR / ".env")

    endpoint = require_env("AZURE_AI_PROJECT_ENDPOINT")
    validate_endpoint(endpoint)
    model_deployment = require_env("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    agent_name = require_env("AGENT_NAME")

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
        allow_preview=True,
    )

    return (
        project_client,
        project_client.get_openai_client(),
        model_deployment,
        agent_name,
    )


# ---------------------------------------------------------------------------
# Summary file (one per run, local to this machine)
# ---------------------------------------------------------------------------

def summary_path(name: str) -> Path:
    return RESULTS_DIR / f"{name}_summary.json"


def save_summary(path: Path, summary: dict) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Unique name (checked locally and against Foundry)
# ---------------------------------------------------------------------------

def list_evals(openai_client):
    """List evaluations, newest first when the service supports it."""

    try:
        return openai_client.evals.list(limit=100, order="desc")
    except Exception:
        return openai_client.evals.list(limit=100)


def count_foundry_matches(openai_client, name: str):
    """How many evaluations are named '<name> - ...'. None if check failed."""

    prefix = f"{name} - ".lower()
    count = 0

    try:
        items = retry(lambda: list_evals(openai_client), "duplicate-name check")
        for item in islice(items, MAX_EVALS_TO_CHECK):
            if item.name and item.name.lower().startswith(prefix):
                count += 1
    except Exception:
        return None

    return count



def ask_for_name(openai_client) -> str:
    """Suggest a random unique name, allowing the user to choose their own."""

    say("\n" + "=" * 60)
    say(" Credit Risk Agent Evaluation")
    say("=" * 60)

    # Generate a random suggested name and check for duplicates.
    while True:
        prefix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=4))
        suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=4))
        suggested_name = f"{prefix}-credit-{suffix}"

        if summary_path(suggested_name).exists():
            continue

        matches = count_foundry_matches(openai_client, suggested_name)
        if matches is not None and matches > 0:
            continue

        break

    say("\nA unique run name has been suggested for you.")
    say("You can use the suggested name or enter your own unique name.")
    say(f"\nSuggested name: {suggested_name}")
    say(
        f"\nAt least {MIN_NAME_LENGTH} characters. "
        "Letters, numbers, hyphens and underscores only.\n"
    )

    while True:
        try:
            name = input(
                "Run name (press Enter to use the suggested name, "
                "or enter your own unique name): "
            ).strip().lower()

        except (EOFError, KeyboardInterrupt):
            say("\nCancelled. No evaluation was started.")
            sys.exit(1)

        name = name or suggested_name

        if len(name) < MIN_NAME_LENGTH:
            say(f"  Too short. Use at least {MIN_NAME_LENGTH} characters.\n")
            continue

        if not NAME_PATTERN.match(name):
            say("  Use only letters, numbers, hyphens and underscores. No spaces.\n")
            continue

        if summary_path(name).exists():
            say(f"  '{name}' is already used locally. Try another name.\n")
            continue

        matches = count_foundry_matches(openai_client, name)

        if matches is None:
            say("  Note: Could not check Foundry for duplicate names.")

        elif matches > 0:
            say(f"  '{name}' is already used in Foundry. Try another name.\n")
            continue

        say(f"\n  Using name: {name}")
        return name

# ---------------------------------------------------------------------------
# Dataset (shared by everyone, so uploads can race)
# ---------------------------------------------------------------------------

def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def looks_like_already_exists(exc: Exception) -> bool:
    return (
        isinstance(exc, ResourceExistsError)
        or status_of(exc) == 409
        or "already exists" in str(exc).lower()
    )


def ensure_dataset(project_client):
    """Reuse the dataset if it is already uploaded, otherwise upload it.

    If someone else uploads the same file at the same moment, wait for
    their upload and reuse it instead of failing.
    """

    say("\n[1/5] Preparing test dataset...")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found: {DATASET_PATH}")

    # Spread people out so they don't all upload in the same second.
    time.sleep(random.uniform(0, STARTUP_JITTER_SECONDS))

    name = os.getenv("DATASET_NAME", "credit-risk-test-queries")
    version = file_hash(DATASET_PATH)

    def fetch():
        return project_client.datasets.get(name=name, version=version)

    def upload():
        return project_client.datasets.upload_file(
            name=name,
            version=version,
            file_path=str(DATASET_PATH),
        )

    try:
        dataset = retry(fetch, "dataset check")
        say(f"  Dataset already uploaded, reusing: {name} v{version}")
        return dataset
    except ResourceNotFoundError:
        pass

    try:
        dataset = retry(upload, "dataset upload")
        say(f"  Dataset uploaded: {dataset.name} v{dataset.version}")
        return dataset
    except Exception as exc:
        if not looks_like_already_exists(exc):
            raise

        say("  Someone just uploaded the same dataset. Waiting for it...")
        for _ in range(6):
            time.sleep(5)
            try:
                dataset = retry(fetch, "dataset check")
                say(f"  Dataset ready, reusing: {name} v{version}")
                return dataset
            except ResourceNotFoundError:
                continue
        raise


# ---------------------------------------------------------------------------
# Evaluation criteria
# ---------------------------------------------------------------------------

def create_testing_criteria(model_deployment):
    say("\n[2/5] Configuring evaluators...")

    data_mapping = {
        "query": "{{item.query}}",
        "response": "{{sample.output_text}}",
    }
    judge_params = {"deployment_name": model_deployment}

    evaluators = [
        ("Coherence", "builtin.coherence", True),
        ("Violence", "builtin.violence", False),
        ("Task Adherence", "builtin.task_adherence", True),
    ]

    criteria = []
    for display_name, evaluator_name, needs_judge in evaluators:
        kwargs = {
            "type": "azure_ai_evaluator",
            "name": display_name,
            "evaluator_name": evaluator_name,
            "data_mapping": data_mapping,
        }
        if needs_judge:
            kwargs["initialization_parameters"] = judge_params

        criteria.append(TestingCriterionAzureAIEvaluator(**kwargs))
        say(f"  Added evaluator: {evaluator_name}")

    return criteria


# ---------------------------------------------------------------------------
# Create evaluation and run
# ---------------------------------------------------------------------------

def create_evaluation(openai_client, testing_criteria, name):
    say("\n[3/5] Creating evaluation...")

    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        include_sample_schema=True,
    )

    evaluation = retry(
        lambda: openai_client.evals.create(
            name=f"{name} - Credit Risk Agent Evaluation",
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
        ),
        "create evaluation",
        only_rate_limit=True,
    )

    say(f"  Evaluation created: {evaluation.id}")
    return evaluation


def warn_if_duplicate_name(openai_client, name: str) -> None:
    """Two people may pick the same name at the same moment. Tell them."""

    matches = count_foundry_matches(openai_client, name)
    if matches and matches > 1:
        say(
            "  Note: another run in this project has the same name. "
            "Use the Evaluation ID or Report URL below to find yours."
        )


def start_evaluation_run(openai_client, evaluation, dataset, agent_name, name):
    say("\n[4/5] Starting evaluation run...")

    eval_run = retry(
        lambda: openai_client.evals.runs.create(
            eval_id=evaluation.id,
            name=f"{name} - Credit Risk Agent Evaluation Run",
            data_source={
                "type": "azure_ai_target_completions",
                "source": {"type": "file_id", "id": dataset.id},
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
                "target": {"type": "azure_ai_agent", "name": agent_name},
            },
        ),
        "start run",
        only_rate_limit=True,
    )

    say(f"  Evaluation run created: {eval_run.id}")
    return eval_run


def wait_for_run(openai_client, evaluation, eval_run):
    """Wait quietly until the run finishes. Returns None on timeout."""

    say(
        "\n[5/5] Running evaluation. This takes roughly 2-3 minutes "
        "(a bit longer when many people run at once). Please wait..."
    )

    deadline = time.monotonic() + MAX_WAIT_SECONDS
    failures = 0

    while True:
        try:
            run = openai_client.evals.runs.retrieve(
                run_id=eval_run.id,
                eval_id=evaluation.id,
            )
            failures = 0
        except Exception as exc:
            # Tolerate a few temporary failures while polling.
            failures += 1
            if not is_transient(exc) or failures > MAX_RETRIES:
                raise
            time.sleep(POLL_SECONDS + random.uniform(0, 5))
            continue

        if run.status in TERMINAL_STATUSES:
            return run

        if time.monotonic() > deadline:
            return None

        time.sleep(POLL_SECONDS + random.uniform(0, 3))


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

def get_count(counts, key):
    if counts is None:
        return None
    if isinstance(counts, dict):
        return counts.get(key)
    return getattr(counts, key, None)


def counts_dict(counts) -> dict:
    result = {}
    for key in ("total", "passed", "failed", "errored"):
        value = get_count(counts, key)
        if value is not None:
            result[key] = value
    return result


def print_final_report(run, evaluation, eval_run, name, path, counts):
    say("\n" + "=" * 60)
    if run.status == "completed":
        say(" Evaluation completed")
    else:
        say(f" Evaluation ended with status: {run.status}")
    say("=" * 60)
    say(f" Name          : {name}")
    say(f" Evaluation ID : {evaluation.id}")
    say(f" Run ID        : {eval_run.id}")
    say(
        " Result counts : "
        + (", ".join(f"{k}={v}" for k, v in counts.items()) or "not available")
    )
    say(f" Report URL    : {getattr(run, 'report_url', None)}")

    error = getattr(run, "error", None)
    if run.status != "completed" and error:
        say(f" Error         : {error}")

    errored = counts.get("errored") or 0
    if errored > 0:
        say(
            f"\n Note: {errored} row(s) errored. When many people run at the "
            "same time, this is usually a rate limit on the agent. "
            "Open the report to see which rows, or run again later."
        )

    say(f"\nSummary saved : results/{path.name}")
    say(f"Full details  : Microsoft Foundry > Evaluations > search '{name}'")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_lab() -> int:
    project_client, openai_client, model_deployment, agent_name = build_clients()

    name = ask_for_name(openai_client)
    path = summary_path(name)

    summary = {
        "name": name,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "agent_name": agent_name,
        "use_case": "Credit Risk Assessment",
        "evaluators": [
            "builtin.coherence",
            "builtin.violence",
            "builtin.task_adherence",
        ],
    }

    try:
        dataset = ensure_dataset(project_client)
        summary.update(dataset=dataset.name, dataset_version=dataset.version)

        criteria = create_testing_criteria(model_deployment)

        evaluation = create_evaluation(openai_client, criteria, name)
        summary.update(evaluation_id=evaluation.id, status="created")
        save_summary(path, summary)  # name is now reserved on this machine
        warn_if_duplicate_name(openai_client, name)

        eval_run = start_evaluation_run(
            openai_client, evaluation, dataset, agent_name, name
        )
        summary.update(run_id=eval_run.id, status="running")
        save_summary(path, summary)

        run = wait_for_run(openai_client, evaluation, eval_run)

    except KeyboardInterrupt:
        if "run_id" in summary:
            summary["status"] = "stopped_waiting"
            save_summary(path, summary)
            say(
                "\nStopped waiting. The run keeps going in Foundry. "
                f"Search for '{name}' under Evaluations to check it."
            )
        else:
            say("\nCancelled.")
        return 1

    except Exception as exc:
        name_used = "evaluation_id" in summary
        if name_used:
            summary.update(status="error", error=str(exc))
            save_summary(path, summary)
        show_error(exc, name_used=name_used)
        return 1

    if run is None:
        summary["status"] = "still_running"
        save_summary(path, summary)
        say(
            "\nStill running after 30 minutes. It is probably queued behind "
            f"other runs. Check Foundry > Evaluations > search '{name}'."
        )
        return 1

    counts = counts_dict(getattr(run, "result_counts", None))
    summary.update(
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        status=run.status,
        report_url=getattr(run, "report_url", None),
        result_counts=counts,
    )
    save_summary(path, summary)

    print_final_report(run, evaluation, eval_run, name, path, counts)
    return 0 if run.status == "completed" else 1


def main() -> None:
    try:
        sys.exit(run_lab())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        say("\nCancelled.")
        sys.exit(1)
    except Exception as exc:
        show_error(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()