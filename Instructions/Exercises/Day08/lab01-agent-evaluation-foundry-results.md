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

## Prerequisites

Before starting this exercise, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.12.10](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed on your local machine.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed.
- Access to the Microsoft Foundry project and a model deployment within the same project.

## Create the agent

1. Return to [Microsoft Foundry](https://ai.azure.com/?utm_source=chatgpt.com) and select your project if you haven't been automatically redirected to the home page.

2. Click on **Create an agent**.

3. A dialog box will appear. Enter your agent name in the following format: `<your_unique_prefix>-cra`.

4. Leave the other settings unchanged. Click **Create**.

5. Replace the default instructions with the following:

   ```text
   You are a Credit Risk Assessment Agent. Help users understand factors that may affect credit risk and provide clear, concise responses based on the information provided.
   ```

6. After creating the agent, note its name in Notepad, as you will need to use the same name in the `.env` file shortly:

   ```env
   AGENT_NAME="<your_unique_prefix>-cra"
   ```

## Get the application files from GitHub

### 1. Clean Up Previous Downloads

Before downloading the latest repository version, remove the previous downloaded files and extracted folders to avoid using an outdated copy.

1. Open your **Downloads** folder.
2. Delete the previously downloaded `AgenticAIEngineer-main.zip` file.
3. Delete the previously extracted `AgenticAIEngineer-main` folder and any duplicate extracted folders, such as `AgenticAIEngineer-main (1)`.
4. Make sure the old copies have been removed before proceeding.

> [!TIP]
> Make sure to download the latest repository ZIP file, as it contains the current lab files and instructions required to complete the steps in this exercise.

### 2. Download and Extract the Latest Repository

The application files for the Credit Risk RAG application are provided in the [training repository](https://github.com/Kiran-255666/AgenticAIEngineer).

1. Open the [training repository](https://github.com/Kiran-255666/AgenticAIEngineer) in a browser.

2. Select **Code** and then select **Download ZIP**.

3. Once the ZIP file has downloaded, open the **Downloads** folder.

4. Right-click the ZIP file and select **Extract All**.

> **Important:** Do not run the application directly from the deeply nested extracted folder in `Downloads`. The long Windows path can cause path-related problems in the VM.

5. After extracting the repository, open **PowerShell** and run these commands.

   ```powershell
   Copy-Item "C:\Users\agenticuser\Downloads\AgenticAIEngineer-main\AgenticAIEngineer-main\labfiles\Day08\lab01-agent-evaluation-foundry-results" "$env:USERPROFILE\Desktop\lab01-agent-evaluation-foundry-results" -Recurse
   ```

6. Run the following command to open the copied lab folder from your Desktop in Visual Studio Code:

   ```powershell
   code "$env:USERPROFILE\Desktop\lab01-agent-evaluation-foundry-results"
   ```

7. In Visual Studio Code, select **Terminal > New Terminal**.

8. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

9. Install the required Python packages:

   ```powershell
   pip install -r requirements.txt
   ```

### Configure the environment

> [!TIP]
> `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME` are already prefilled. You only need to replace the `AGENT_NAME` value with the agent name you saved earlier in Notepad.

1. Use the agent name you saved in Notepad in the previous step to replace `<your_unique_prefix>-cra`.

## Sign in to Azure

1. In the terminal, run:

   ```powershell
   az account show
   ```

2. If your account details are displayed, continue to the next step, [Review the lab files](#review-the-lab-files). Otherwise, run `az login` followed by `az account show` to sign in and verify your Azure account.

> [!TIP]
> Want to complete the lab first and understand the code later? You can do that too. Skip to [Run the evaluation](#run-the-evaluation) and complete the steps. Once you're done, come back to [Review the lab files](#review-the-lab-files) to understand the code.

# Agent Evaluation with Microsoft Foundry

## Review the Lab Files

The lab contains the following files:

```text
labfiles/Day08/lab01-agent-evaluation-foundry-results/
├── .env
├── requirements.txt
├── evaluate_agent_advanced.py
├── data/
│   └── credit_risk_test_queries.jsonl
└── results/
```

The files have the following purpose:

- **`.env`**: Contains the Microsoft Foundry project endpoint, model deployment name, and agent name.
- **`requirements.txt`**: Contains the required Python packages (`azure-ai-projects>=2.8.0`, `azure-identity`, `azure-core`, `openai`, and `python-dotenv`).
- **`data/credit_risk_test_queries.jsonl`**: Contains the test queries used during evaluation.
- **`evaluate_agent_advanced.py`**: Contains the complete evaluation workflow.
- **`results/`**: Stores local evaluation summaries, with one JSON file per run.

## Review the .env Configuration

Open the `.env` file in the lab root folder.

It contains the following configuration variables:

- **`AZURE_AI_PROJECT_ENDPOINT`**: Your Microsoft Foundry project endpoint. It must follow this format: `https://<account>.services.ai.azure.com/api/projects/<project>`. Copy it from **Microsoft Foundry > Your project > Overview**.
- **`AZURE_AI_MODEL_DEPLOYMENT_NAME`**: The model deployment name (not the model name) from **Microsoft Foundry > Models + endpoints**. This deployment is used as the judge model by evaluators that require one.
- **`AGENT_NAME`**: The name of the existing Credit Risk Assessment agent (for example, `<your_unique_prefix>-cra`).

Optional settings:

- **`DATASET_NAME`**: Overrides the default dataset name (`credit-risk-test-queries`).
- **`EVAL_DEBUG`**: Set this variable to any value to print full Python tracebacks when an error occurs.

Ensure that the endpoint, deployment name, and agent name match the resources available in your Foundry project.

## Review the Test Dataset

Open the following file:

```text
data/credit_risk_test_queries.jsonl
```

The file contains one JSON object per line. Each object represents a test case with the following fields:

- **`query`**: The question sent to the Credit Risk Assessment agent. This is the only field used as input to the agent.
- **`context`**: Relevant policy, scorecard rules, or client-specific information. Retained for reference.
- **`response`**: The expected response for the test case. Retained for reference.
- **`ground_truth`**: The reference answer used for documentation and reference purposes.

For example:

```json
{"query":"What documents are required to start a credit risk assessment?","context":"Credit risk assessment policy. Required documents: Company Registration Certificate and GST Certificate.","response":"The two required documents are the Company Registration Certificate and the GST Certificate.","ground_truth":"The two required documents are the Company Registration Certificate and the GST Certificate."}
```

The dataset contains questions covering different aspects of credit risk assessment, including:

- Document verification
- Financial ratios
- Industry risk
- Compliance checks
- External credit scores
- Scorecard calculations
- Credit-limit decisions

> [!NOTE]
> The evaluation sends only the `query` field to the agent and scores the agent's actual output using the configured evaluators. The `context`, `response`, and `ground_truth` fields are not sent to the agent. Keep all four fields in each JSON object to maintain the expected dataset structure. You can add or replace test cases with questions relevant to your Credit Risk Assessment agent.

## Review the Evaluation Script

Open the following file:

```text
evaluate_agent_advanced.py
```

The script implements the complete evaluation workflow and supports multiple participants running evaluations simultaneously against one shared Microsoft Foundry project.

### Connect to Microsoft Foundry

The script loads the project configuration from `.env` and creates an authenticated Microsoft Foundry client.

Authentication is handled through `DefaultAzureCredential`, allowing the script to use the Azure account authenticated through Azure CLI.

### Choose a Unique Run Name

The script suggests a randomly generated unique run name (for example, `ab12cd34-credit-ef56gh78`).

Before accepting a name, the script checks it against:

- Existing local summaries in the `results/` folder.
- Existing evaluations in the Microsoft Foundry project.

Press **Enter** to use the suggested name, or enter your own unique name.

Custom run names must:

- Contain at least 7 characters.
- Use only lowercase letters, numbers, hyphens, and underscores.
- Be unique across the local summaries and existing Foundry evaluations.

### Upload the Test Dataset

The script uploads the following file to the Microsoft Foundry project as a versioned dataset:

```text
data/credit_risk_test_queries.jsonl
```

The dataset version is derived from the file's SHA-256 hash.

This allows the script to:

- Reuse an existing dataset version if the same file has already been uploaded.
- Avoid duplicate uploads when multiple participants use identical datasets.
- Detect simultaneous upload conflicts, wait for the other upload to finish, and reuse the existing version.

A short random startup delay also helps distribute simultaneous requests across participants.

### Configure Built-in Evaluators

The evaluation uses the following built-in Azure AI evaluators:

| Evaluator | Purpose | Judge Model Required |
|---|---|---|
| **Coherence** | Evaluates whether the response is clear and logically consistent. | Yes |
| **Violence** | Evaluates the response against configured safety criteria. | No |
| **Task Adherence** | Evaluates whether the response follows the expected task. | Yes |

The evaluators are configured directly in the evaluation script.

The model deployment specified through `AZURE_AI_MODEL_DEPLOYMENT_NAME` is used as the judge model for evaluators that require one.

### Create and Run the Evaluation

The script creates an evaluation using the uploaded dataset and configured evaluators.

The evaluation target is the existing Credit Risk Assessment agent specified through `AGENT_NAME`.

For each test case:

1. The `query` field is sent to the agent.
2. The agent generates its response.
3. The configured evaluators assess the agent's actual output.
4. The evaluation results are recorded in Microsoft Foundry.

The script polls the evaluation run approximately every 10 seconds until it reaches a terminal state:

- `completed`
- `failed`
- `canceled`

The maximum waiting period is 30 minutes.

Transient errors, including rate limits, connection issues, and HTTP 5xx responses, are retried automatically using exponential backoff.

## Run the Evaluation

1. Install the required Python packages:

   ```powershell
   pip install -r requirements.txt
   ```

2. Open a terminal in the lab root folder and execute:

   ```powershell
   python evaluate_agent_advanced.py
   ```

3. When prompted, press **Enter** to use the suggested run name, or enter your own unique name.

4. The script performs the following operations:

   1. Uploads the credit risk test dataset or reuses an existing version.
   2. Configures the built-in evaluators.
   3. Creates the evaluation.
   4. Starts the evaluation run against the existing Credit Risk Assessment agent.
   5. Monitors the run until it completes.
   6. Displays the Microsoft Foundry report URL.
   7. Saves a local evaluation summary.

5. Once the evaluation finishes, the terminal displays:

   - Run name
   - Evaluation ID
   - Run ID
   - Total test cases
   - Passed test cases
   - Failed test cases
   - Errored test cases
   - Microsoft Foundry report URL

The evaluation typically takes approximately 2–3 minutes, although it may take longer when multiple participants run evaluations simultaneously.

### Review the Local Evaluation Summary

Each completed run saves its summary as a separate JSON file:

```text
results/<run_name>_summary.json
```

For example:

```text
results/
├── ab12cd34-credit-ef56gh78_summary.json
├── cd34ef56-credit-gh78ij90_summary.json
└── ...
```

You can use these files to review and retain the results of individual evaluation runs.

> [!NOTE]
> If you stop the script using `Ctrl+C` while it is waiting, the evaluation run continues running in Microsoft Foundry. You can search for your run name under **Evaluations** in the Foundry portal to check its status and results.
>
> If the run does not finish within 30 minutes, the script exits and directs you to the Foundry portal to check the evaluation.
>
> Common issues, such as expired Azure CLI authentication, incorrect project endpoints, using a model name instead of a deployment name, or rate limits during simultaneous runs, are reported with troubleshooting hints.

## Run the Evaluation

1. Open a terminal in the lab root folder and execute:

   ```powershell
   python evaluate_agent_advanced.py
   ```

2. When prompted, press **Enter** to use the suggested run name, or enter your own unique name.

3. The script performs the following operations:

   1. Uploads the credit risk test dataset or reuses an existing version.
   2. Configures the built-in evaluators.
   3. Creates the evaluation.
   4. Starts the evaluation run against the existing Credit Risk Assessment agent.
   5. Monitors the evaluation until it reaches a terminal state.
   6. Displays the Microsoft Foundry report URL.
   7. Saves a local evaluation summary.

4. When the evaluation completes, the terminal displays the run name, evaluation ID, run ID, result counts (`total`, `passed`, `failed`, and `errored`), and report URL.

The local summary is saved using the run name:

```text
results/<run_name>_summary.json
```

Each evaluation run generates a separate summary file in the `results/` folder.

## Review the Evaluation Results in Microsoft Foundry

1. Open the report URL displayed in the terminal.

   If the URL is unavailable:

   1. Open [Microsoft Foundry](https://ai.azure.com/).
   2. On Left click **Evaluations**.
   3. Search the evaluation run using the run name displayed in the terminal.

2. Review the evaluation results:

   - **Evaluation Run Status:** Check whether the run completed successfully.
   - **Overall Evaluation Results:** Review the summary of the evaluation.
   - **Coherence:** Check whether the agent's responses are clear and logically structured.
   - **Violence:** Check whether any responses contain violent or unsafe content.
   - **Task Adherence:** Check whether the agent follows the instructions given in each query.
   - **Individual Test Cases:** Open each test case and inspect the input query and generated response.
   - **Evaluator Reasoning:** Review why each evaluator marked a response as passing or failing.
   - **Response Accuracy:** Compare the generated responses with the expected answers and reference context.
   - **Performance Metrics:** Check response latency and token usage.

### Review Individual Test Cases

Open individual test cases to examine:

- The original test query.
- The agent's generated response.
- The evaluator results.
- The evaluator reasoning, where available.

Pay particular attention to test cases where the agent receives a low score or an evaluator identifies a quality or safety issue.

Remember that the evaluation sends only the `query` field to the agent. The other dataset fields are retained for reference and are not supplied as agent input. Use these reference fields to manually check whether the agent's response is accurate and follows the expected credit risk assessment requirements.

> [!Tip] 
> When testing your agent with your own dataset for the first time, you may receive low evaluation scores. This is normal. Use the evaluation results to identify issues, improve your agent, and run multiple iterations until you achieve satisfactory results. The `credit_risk_test_queries.jsonl` dataset used in this lab has already gone through multiple iterations of testing and refinement.

## Summary

In this exercise, you used the Azure AI Projects SDK to evaluate an existing Credit Risk Assessment agent.

You prepared a JSONL test dataset, connected to your Microsoft Foundry project, configured built-in evaluators, and ran an evaluation against the existing agent.

You then reviewed the evaluation results in Microsoft Foundry, examined individual test cases, identified areas for improvement, and updated the agent.

Finally, you ran another evaluation and compared the results to assess whether your changes improved the agent's performance.