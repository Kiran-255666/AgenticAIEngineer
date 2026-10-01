---
lab:
    title: 'Develop an Azure AI agent with the Microsoft Agent Framework SDK'
    description: 'Learn how to use the Microsoft Agent Framework SDK to create and use an Azure AI chat agent.'
    level: 300
    duration: 40
    islab: true
    status: 'released'
---

# Develop an Azure AI chat agent with the Microsoft Agent Framework SDK

In this exercise, you'll use Azure AI Agent Service and Microsoft Agent Framework to create an AI agent that processes expense claims.

This exercise should take approximately **40** minutes to complete.

## Prerequisites

Before starting this exercise, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- An active [Azure subscription](https://azure.microsoft.com/free/)
- [Python 3.12.10](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Foundry Toolkit VS Code extension

> This lab was tested with Python 3.12.10.

## Use the Deployed Model

**Use the deployed model already available in your Microsoft Foundry project at [ai.azure.com](https://ai.azure.com/).**

# Get the application files from GitHub

1. If you downloaded and extracted the repository during the previous day’s lab, delete the ZIP file and extracted folder from **Downloads**. If you copied the repository to the **Desktop**, your saved progress will remain there. This helps avoid potential long path issues when running the PowerShell commands below.

2. Open a web browser and go to the [lab files on GitHub](https://github.com/Kiran-255666/AgenticAIEngineer).

3. On the repository page, select the green **`<> Code`** button, and then select **Download ZIP**.

4. Once the download finishes, extract the ZIP file.

5. Open ****PowerShell**** and run the following two commands to avoid long path issues:

```powershell
Copy-Item "C:\Users\agenticuser\Downloads\AgenticAIEngineer-main\AgenticAIEngineer-main\labfiles\Day06\lab01-agent-framework" "$env:USERPROFILE\Desktop\lab01-agent-framework" -Recurse

code "$env:USERPROFILE\Desktop\lab01-agent-framework"
```

The first command copies the lab folder to your ****Desktop****, and the second command opens the copied folder directly in ****Visual Studio Code****.

This folder already contains the application files and the required code for this exercise.

6. You are now working from the ****Desktop**** folder, so there is no need to worry about the long path issue. Press ****Ctrl+Shift+`**** to open the integrated terminal.

7. In the terminal, enter the following commands to create and activate a virtual environment and install the required Python packages:

   ```
   python -m venv labenv
   .\labenv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

8. The ****.env**** file is already configured for you. You do not need to change any of the existing values.

## Review the Credit Risk Assessment Agent

The `agent-framework.py` file already contains the code required to create and run the Credit Risk Assessment agent.

> **Note:** The code has already been updated for the current Credit Risk Assessment use case. Before running the application, review the code in `agent-framework.py` and make sure the file paths, environment variables, and configuration are correct.

1. Open the **`agent-framework.py`** file in the code editor.

2. Review the project structure:

```text
lab01-agent-framework/
├── .env
├── agent-framework.py
├── requirements.txt
└── data/
    ├── data.txt
    └── instructions.txt
```

3. Review the **`data`** folder.

The folder contains two `.txt` files:

* **`data.txt`** → contains the sample company information used for the credit-risk assessment.
* **`instructions.txt`** → contains the credit-risk assessment rules and instructions followed by the agent.

Keeping the company data and assessment instructions in separate files allows you to modify the information and rules without changing the Python application.

4. Open the **`agent-framework.py`** file and review the references at the top:

```python
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
```

These libraries are used to load environment variables, read the `.txt` files, authenticate with Azure, connect to the Microsoft Foundry project, and create the agent.

5. Review the **`load_file()`** function:

```python
def load_file(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()
```

This function reads the contents of the files stored in the `data` folder.

6. Review the **`main()`** function.

The application locates the `data` folder and loads both the company information and assessment instructions:

```python
script_dir = Path(__file__).parent
data_dir = script_dir / "data"

company_data = load_file(data_dir / "data.txt")
instructions = load_file(data_dir / "instructions.txt")
```

The application then asks for an assessment request:

```python
user_prompt = input(
    "What would you like me to assess?\n\n"
)
```

7. Review the **Create the Foundry project client** section:

```python
project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

`DefaultAzureCredential` authenticates the application using an available Azure identity. The `AIProjectClient` connects the application to the Microsoft Foundry project using the project endpoint configured in the `.env` file.

8. Review the **Create the Credit Risk Assessment Agent** section:

```python
agent = project.agents.create_version(
    agent_name="credit-risk-assessment-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=instructions,
    ),
)
```

The agent uses the model deployment configured in the `.env` file. The instructions from `instructions.txt` are provided to the agent so that it can follow the defined credit-risk assessment process.

9. Review the **Send the assessment request** section:

```python
response = openai.responses.create(
    conversation=conversation.id,
    input=f"""
Company data:

{company_data}

Assessment request:

{user_prompt}
""",
)
```

The company information from `data.txt` and the assessment request entered by the user are sent to the Credit Risk Assessment agent.

10. Review the **Display the response** section:

```python
print("\nCredit Risk Assessment")
print("----------------------")
print(response.output_text)
```

This displays the response generated by the agent in the terminal.

## Test the application

The application is now ready to run.

1. In the integrated terminal, verify that you are signed in to Azure:

```powershell
az account show
```

If your Azure account details are displayed, continue to the next step.

If you are not signed in, run:

```powershell
az login
```

2. Run the application:

```powershell
python agent-framework.py
```

3. When prompted, enter:

```text
Assess ABC Utilities Pvt Ltd for credit approval.
```

### Test Case 1: Low Risk

The agent should produce an assessment similar to:

```text
Credit Risk Assessment
----------------------

Company: ABC Utilities Pvt Ltd

Document Verification:
Company Registration Certificate: Present
GST Certificate: Present
Result: Pass

Company Name Verification:
Registration Certificate Name: ABC Utilities Pvt Ltd
GST Certificate Name: ABC Utilities Pvt Ltd
Result: Pass

MCA Status:
Active

Sanctions Check:
No Match Found

Financial Statements:
Available

Financial Analysis:
Current Ratio:
1.56

Debt-to-Equity:
1.86

Net Profit Margin:
5.56%

D&B Score:
720

Industry Risk:
Utilities - Low

Total Score:
90/100

Risk Rating:
Low

Recommended Credit Limit:
$5,000,000

Recommended Payment Terms:
60 days
```

6. At the next prompt, enter:

```text
Assess Nova Manufacturing Pvt Ltd for credit approval.
```

### Test Case 2: Medium Risk

The agent should identify values similar to:

```text
Current Ratio: 1.27
Debt-to-Equity: 1.83
Net Profit Margin: 4.38%
D&B Score: 670
Industry Risk: Medium
Total Score: 73/100
Risk Rating: Medium
Recommended Credit Limit: $2,000,000
Recommended Payment Terms: 30 days
```

7. At the next prompt, enter:

```text
Assess Skyline Construction Ltd for credit approval.
```

### Test Case 3: High Risk

The agent should identify values similar to:

```text
Current Ratio: 0.67
Debt-to-Equity: 4.50
Net Profit Margin: 0.71%
D&B Score: 610
Industry Risk: High
Total Score: 28/100
Risk Rating: High
Recommended Credit Limit: No credit
Recommended Payment Terms: Advance payment
```

8. You can continue entering additional assessment requests using the other companies in `data.txt`.

9. To stop the application, enter:

```text
quit
```

or:

```text
exit
```

You can also press **Ctrl+C** to stop the application.

> **Note:** The exact wording and formatting may differ because the response is generated by the AI agent. Focus on whether the agent correctly applies the rules from `instructions.txt` to the company information in `data.txt`.


## Experiment with the `.txt` Files (Optional)

After completing the test cases, experiment with the information in the `data` folder.

Open **`data.txt`** and try changing values such as:

* Current Assets
* Current Liabilities
* Total Debt
* Total Equity
* Revenue
* Net Profit
* D&B Score
* Industry
* MCA status
* Certificate availability
* Company names
* Sanctions status

For example, change the financial values and run the application again to see how the calculated ratios and risk score change.

You can also create different scenarios by:

* Removing one of the required certificates.
* Changing the company name on one certificate.
* Changing the MCA status to Inactive.
* Adding a sanctions match.
* Changing the industry from Low Risk to High Risk.
* Adding a new company record with your own values.

You can also review and modify **`instructions.txt`** to understand how the assessment rules control the agent's response.

> **Note:** Save your changes before running the application again. For these experiments, modify the `.txt` files rather than changing the Python code.

## Clean Up the Agent

The codebase includes cleanup logic to remove the temporary agent version when the application exits.

The `delete_version()` function removes the specific agent version created during the current run:

```python
project.agents.delete_version(
    agent_name=agent.name,
    agent_version=agent.version,
)
```

The cleanup runs when you enter `quit`, enter `exit`, or press **Ctrl+C**.

## Summary

In this exercise, you used **Agent Framework** with Microsoft Foundry to create and test a Credit Risk Assessment agent.

You reviewed the Python code, company data, and assessment instructions, tested different risk scenarios, and experimented with the `.txt` files to see how changes in the input affect the assessment.

The key takeaway is that the **Python application, company data, and assessment rules are kept separate**, allowing you to test different credit-risk scenarios without changing the main application code.
