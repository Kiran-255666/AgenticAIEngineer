---
lab:
  title: 'Evaluate an Azure AI agent using the Python SDK'
  description: 'Learn how to evaluate an existing Azure AI agent using the Python SDK and review evaluation results in Microsoft Foundry.'
  level: 300
  duration: 40
  islab: true
  status: 'released'
---

# Evaluate an Azure AI agent using the Python SDK

In this exercise, you'll use the Azure AI Projects SDK to evaluate an existing Credit Risk Assessment agent. You'll prepare a JSONL test dataset, configure built-in evaluators, run the evaluation, and review the results in Microsoft Foundry.

This exercise takes approximately **40 minutes** to complete.

## Learning objectives

By the end of this exercise, you'll be able to:

* Prepare a JSONL dataset for agent evaluation.
* Connect to a Microsoft Foundry project using the Python SDK.
* Configure built-in evaluators.
* Run an evaluation against an Azure AI agent.
* Review evaluation results in Microsoft Foundry.
* Identify weak test cases and suggest improvements.

## Prerequisites

Before starting this exercise, ensure you have:

* [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
* [Python 3.12.10](https://www.python.org/downloads/) installed.
* [Git](https://git-scm.com/downloads) installed on your local machine.
* [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed.
* Access to the Microsoft Foundry project used for this lab.
* An existing Credit Risk Assessment agent.
* A model deployment available in the same Microsoft Foundry project.

> This lab was tested with Python 3.12.10.

## Use the deployed model

Use the model deployment already available in your Microsoft Foundry project at [ai.azure.com](https://ai.azure.com/).

The model deployment is used by the evaluation script for model-based evaluation.

> **Important:** Use the **model deployment name**, not only the underlying model name.

## Create the agent

Create a new agent in the same Microsoft Foundry project.

Use the following name:

```text
<your_unique_prefix>-credit-risk-assessment-agent
```

Configure the agent for the **Credit Risk Assessment** use case and make sure it uses the model deployment selected above.

If you want to provide custom instructions, you can replace the default instructions with the following:

```text
You are a Credit Risk Assessment Agent. Help users understand factors that may affect credit risk and provide clear, concise responses based on the information provided.
```

After creating the agent, use the same agent name in the `.env` file:

```env
AGENT_NAME="<your_unique_prefix>-credit-risk-assessment-agent"
```

> **Important:** Replace `<your_unique_prefix>` with a unique prefix assigned to you before creating the agent.

## Get the application files from GitHub

1. Open a web browser and go to the [AgenticAIEngineer repository](https://github.com/Kiran-255666/AgenticAIEngineer).

   > **Important:** Before downloading, make sure you don't already have an older ZIP file or extracted `AgenticAIEngineer-main` folder from a previous download. Delete or move the old files if needed.

2. Select **<> Code**, and then select **Download ZIP**.

3. Extract the downloaded ZIP file.

4. Open **PowerShell** and run the following command to copy the `lab02-agent-evaluation-foundry-results` folder to your Desktop:

   ```powershell
   Copy-Item "C:\Users\agenticuser\Downloads\AgenticAIEngineer-main\AgenticAIEngineer-main\labfiles\Day08\lab02-agent-evaluation-foundry-results" "$env:USERPROFILE\Desktop\lab02-agent-evaluation-foundry-results" -Recurse
   ```

5. Run the following command to open the copied lab folder from your Desktop in Visual Studio Code:

   ```powershell
   code "$env:USERPROFILE\Desktop\lab02-agent-evaluation-foundry-results"
   ```

   > Update the source path in step 4 if the extracted ZIP is in a different location or has a different folder name.

6. In Visual Studio Code, select **Terminal > New Terminal**.

7. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

8. Install the required Python packages:

   ```powershell
   pip install -r requirements.txt
   ```

## Configure the environment

The lab includes a `.env` file with the configuration required by the evaluation script.

Open the `.env` file and replace these placeholders value with your actual values:

```env
AZURE_AI_PROJECT_ENDPOINT="https://<your-foundry-resource>.services.ai.azure.com/api/projects/<your-project-name>"

AZURE_AI_MODEL_DEPLOYMENT_NAME="<your-model-deployment>"

AGENT_NAME="<your-agent-name>"
```

Make sure the values match your Microsoft Foundry project.

The `AGENT_NAME` value must match the existing Credit Risk Assessment agent that you want to evaluate.

> **Important:** Use the **model deployment name** for `AZURE_AI_MODEL_DEPLOYMENT_NAME`, not only the underlying model name.

## Sign in to Azure

1. In the integrated terminal, sign in to Azure:

   ```powershell
   az login
   ```

2. Verify the active Azure account:

   ```powershell
   az account show
   ```

If multiple Azure subscriptions are available, make sure the correct subscription is selected before continuing.

## Review the lab files

The lab contains the following files:

```text
lab04-agent-evaluation-foundry-results/

├── .env
├── requirements.txt
├── evaluate_agent_advanced.py
├── data/
│   └── credit_risk_test_queries.jsonl
└── results/
```

The files have the following purpose:

* **`.env`** contains the Microsoft Foundry project and agent configuration.
* **`requirements.txt`** contains the required Python packages.
* **`credit_risk_test_queries.jsonl`** contains the test queries.
* **`evaluate_agent_advanced.py`** contains the evaluation workflow.
* **`results/`** stores the local evaluation summary created by the script.

## Review the test dataset

Open:

```text
data/credit_risk_test_queries.jsonl
```

The file contains one JSON object per line.

For example:

```json
{"query": "What factors are usually considered when assessing a customer's credit risk?"}
```

The evaluation script uses the `query` field to send each test case to the Credit Risk Assessment agent.

The dataset contains questions covering different aspects of credit risk assessment.

> **Note:** You can add or replace test queries with questions relevant to your Credit Risk Assessment agent. Keep the `query` field in each JSON object.

## Review the evaluation script

Open:

```text
evaluate_agent_advanced.py
```

The script performs the complete evaluation workflow.

### Connect to Microsoft Foundry

The script loads the project configuration from `.env` and creates an authenticated Microsoft Foundry client.

The Azure identity is provided through `DefaultAzureCredential`.

This allows the script to use the Azure account authenticated through Azure CLI.

### Upload the test dataset

The script uploads:

```text
data/credit_risk_test_queries.jsonl
```

to the Microsoft Foundry project as an evaluation dataset.

Each `query` is used as an input to the agent.

### Configure built-in evaluators

The evaluation uses built-in Azure AI evaluators:

* **Coherence**: Evaluates whether the response is clear and logically consistent.
* **Violence**: Evaluates the response against the configured safety criteria.
* **Task Adherence**: Evaluates whether the response follows the expected task.

The evaluators are configured directly in the evaluation script.

The configured model deployment is used by the model-based evaluators that require a judge model.

### Create and run the evaluation

The script creates an evaluation using the uploaded dataset and configured evaluators.

The evaluation target is the existing Credit Risk Assessment agent.

The script then monitors the evaluation run until it reaches a terminal state.

## Run the evaluation

1. Make sure the virtual environment is active.

2. Verify your Azure account:

   ```powershell
   az account show
   ```

3. From the lab root folder, run:

   ```powershell
   python evaluate_agent_advanced.py
   ```

4. The script performs the following operations:

   1. Uploads the credit risk test dataset.
   2. Configures the built-in evaluators.
   3. Creates the evaluation.
   4. Runs the evaluation against the agent.
   5. Monitors the evaluation until it completes.
   6. Displays the Microsoft Foundry report URL.
   7. Saves a local evaluation summary.

5. When the evaluation completes, the terminal displays the evaluation status, evaluation ID, run ID, report URL, and result counts.

The local summary is saved to:

```text
results/evaluation_run_summary.json
```

A successful run displays a result similar to:

```text
Status: completed
Result counts: ResultCounts(errored=0, failed=0, passed=7, total=7, skipped=0)
```

> **Note:** The number of test cases and evaluation results depends on the dataset and evaluation run.

> **Note:** Evaluation output can vary slightly between runs because model-generated responses and evaluator results can differ.

## Review the evaluation results in Microsoft Foundry

1. Open the report URL displayed in the terminal.

2. If the URL is not available, open [Microsoft Foundry](https://ai.azure.com/).

3. Select the Microsoft Foundry project used by the lab.

4. Open **Evaluations**.

5. Select the evaluation run created by the script.

6. Review the evaluation results.

Review the following information:

* Overall evaluation status.
* Individual test case results.
* Coherence results.
* Violence safety results.
* Task Adherence results.
* Evaluator reasoning.
* Failed or weak test cases.

### Review individual test cases

Open individual test cases to compare:

* The original query.
* The agent response.
* The evaluator result.
* The evaluator reasoning.

Pay particular attention to test cases where the agent receives a low score or where an evaluator identifies a quality issue.

## Improve the agent and re-evaluate

Choose one weak or failed test case.

Review the result and determine whether the issue is related to:

* Agent instructions.
* Agent knowledge.
* Agent tools.
* Test query.
* Response quality.

Make one improvement to the agent and run the evaluation again.

Compare the new evaluation run with the previous run.

Consider whether the change improved the result without introducing problems in other test cases.

## Troubleshoot the evaluation

### Missing environment variable

If the script reports a missing environment variable, open the `.env` file and verify that these values are present:

```text
AZURE_AI_PROJECT_ENDPOINT
AZURE_AI_MODEL_DEPLOYMENT_NAME
AGENT_NAME
```

Make sure there are no spelling errors in the variable names.

### Authentication error

Run:

```powershell
az login
az account show
```

Make sure you are signed in with an account that has access to the Microsoft Foundry project.

### Agent not found

Check the agent name in Microsoft Foundry.

Make sure the value of:

```text
AGENT_NAME
```

matches the existing agent name.

### Model deployment error

Verify that:

```text
AZURE_AI_MODEL_DEPLOYMENT_NAME
```

contains the **deployment name** configured in the Microsoft Foundry project.

Do not use only the underlying model name.

### Dataset or evaluation error

Verify that:

* `data/credit_risk_test_queries.jsonl` exists.
* Each line contains valid JSON.
* Each JSON object contains a `query` field.
* The Microsoft Foundry project is available.
* The configured agent is available in the project.

Run the script again after correcting the issue.

## Clean up

The evaluation creates evaluation-related resources in the Microsoft Foundry project and a local summary file.

After completing the exercise, you can remove test resources that are no longer required according to your project's resource-management practices.

The local evaluation summary is stored at:

```text
results/evaluation_run_summary.json
```

## Summary

In this exercise, you used the Azure AI Projects SDK to evaluate an existing Credit Risk Assessment agent.

You prepared a JSONL test dataset, configured built-in evaluators, ran the evaluation, and reviewed the results in Microsoft Foundry.

You also identified weak test cases and re-evaluated the agent after making improvements.

## The key takeaway is that **agent evaluation provides a repeatable way to test response quality and identify areas for improvement using defined test cases and evaluators**.

### What I fixed

The important production corrections are:

* Removed **all rubric generation** references.
* Removed **Agent Quality generated rubric evaluator** references.
* Removed the incorrect **6-step** execution flow.
* Updated the flow to match the **actual successful Python script**.
* Added **Task Adherence** because your working script actually uses it.
* Updated the results section to match the three real evaluators.
* Added the actual successful `7/7` output as an example, while making clear that results depend on the dataset.
* Kept the Credit Risk Assessment scenario throughout.
* Kept the existing folder structure and commands unchanged.
* Removed the old misleading troubleshooting section about rubric generation.

One small thing I would **not** put in the published lab: your actual `eval_*` IDs, agent name `it-support-agent`, dataset version, or report URL. Those are run-specific and should stay out of the static documentation.
