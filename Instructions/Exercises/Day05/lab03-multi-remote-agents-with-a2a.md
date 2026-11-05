---
lab:
    title: 'Connect to remote agents with A2A protocol'
    description: 'Use the A2A protocol to collaborate with remote agents.'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# Connect to remote agents with A2A protocol

**Note: We have already updated the mentioned files with the code mentioned in the instructions, but we would highly suggest going through it before executing it**

In this exercise, you'll use Azure AI Agent Service with the A2A protocol to create simple remote agents that interact with one another. These agents will assist technical writers with preparing their developer blog posts. A title agent will generate a headline, and an outline agent will use the title to develop a concise outline for the article. Let's get started.

This exercise should take approximately **30** minutes to complete.

## Prerequisites

Before starting this exercise, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- An active [Azure subscription](https://azure.microsoft.com/free/)
- [Python 3.13](https://www.python.org/downloads/) or later installed
- Foundry Toolkit for VS Code extension 


> \* Python 3.13 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.12.10

# Get the application files from GitHub

1. If you have already downloaded and extracted the repository in a previous lab, delete the existing ZIP file and the extracted folder. This will allow us to use the PowerShell commands in the following steps and help avoid long path issues.

2. Open a web browser and go to the [lab files on GitHub](https://github.com/Kiran-255666/AgenticAIEngineer).

3. On the repository page, select the green **`<> Code`** button, and then select **Download ZIP**.

4. Once the download finishes, extract the ZIP file.

5. Open ****PowerShell**** and run the following two commands to avoid long path issues:

```powershell
Copy-Item "C:\Users\agenticuser\Downloads\AgenticAIEngineer-main\AgenticAIEngineer-main\labfiles\Day05\lab03-multi-remote-agents-with-a2a" "$env:USERPROFILE\Desktop\lab03-multi-remote-agents-with-a2a" -Recurse

code "$env:USERPROFILE\Desktop\lab03-multi-remote-agents-with-a2a"
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

# Review Before You Run

This project is already filled in. You do not need to add the example code from older lab instructions. First read the files below and follow how one question travels through the application. Then run it and try a few questions.

## What the application does

You type a question. The Routing Agent sends it to the right specialist, and the specialist looks up information in `data/` and sends back an answer.

```text
You -> CLI -> Routing Agent -> Specialist Agent -> Answer
```

The specialists are:

- **Document Verification Agent**: checks which company documents are listed and whether names match.
- **Financial Analysis Agent**: reports financial values and works out financial ratios.
- **Credit Risk Assessment Agent**: summarizes the available risk information and explains what is missing.

The agents talk to each other using A2A. Think of A2A as the agreed format they use to send a request and receive a reply.

## Review the source documents first

Open the `data/` folder. These files contain the facts and rules the application should use:

- `company_documents.txt`: company identity and document availability.
- `financial_data.txt`: the company's reported financial numbers.
- `credit_bureau_report.txt`: external credit score and industry details.
- `document_verification_instructions.txt`: what to check in the company documents.
- `financial_analysis_instructions.txt`: which financial ratios to calculate and how.
- `credit_risk_instructions.txt`: what the final risk summary should cover.

The Python code should read these files. The company name, financial numbers, score, and rules should not be typed directly into Python code. If a document does not contain an answer, the agent should say it is unavailable.

## A few important functions

The code is already written. Before running it, follow these four functions to understand the main path:

- `load_all_data()` in `credit_risk_data.py` opens the files in `data/`.
- `compute_financial_ratios()` in `credit_risk_data.py` calculates ratios from the documented numbers.
- `send_message(...)` in `routing_agent/agent.py` passes your question from the router to a specialist using A2A.
- `run_conversation(...)` in a specialist's `agent.py` prepares that specialist's answer using the documents.

The names on each agent's card tell the router what specialists are available. You do not need to edit these functions for the review exercise.

## Try the application

The environment and packages are already set up. From the project folder, run:

```text
python run_all.py
```

At the prompt, try these questions one at a time. The wording may vary, but each answer should include the expected information below.

### Test 1: Company documents

Ask:

```text
What company documents are available?
```

The agent should return information similar to:

* Company: Apex Manufacturing Pvt Ltd.
* Company Registration Certificate: Available.
* GST Certificate: Available.
* Registration status: Active.
* The company name shown on both certificates matches.

> **Tip:** Generally, you should see output similar to the above. However, in some cases, you may see output in the following format:
>
> * Available company documents: Company Registration Certificate and GST Certificate.
> * Name consistency: Both documents show Apex Manufacturing Pvt Ltd, and the names match the stated company name.
> * Missing/unavailable expected documents: None; the required documents are available.

### Test 2: Financial ratios

Ask:

```text
What are the financial ratios?
```

The agent should return information similar to:

* Current Assets: 7,800,000.
* Current Liabilities: 5,000,000.
* Total Debt: 9,300,000.
* Shareholders' Equity: 5,000,000.
* Revenue: 9,000,000.
* Net Profit: 500,000.
* Current Ratio: 1.56.
* Debt-to-Equity Ratio: 1.86.
* Net Profit Margin: 5.56%.

The source file does not specify a currency, so the agent should not assume or add one.

### Test 3: Credit bureau and industry

Ask:

```text
What is the external credit bureau score and industry?
```

The agent should return information similar to:

* External Credit Bureau Score: 720.
* Industry: Manufacturing.
* Credit Bureau Status: No adverse records reported.
* A separate industry risk rating is not provided in the available information.

### Test 4: Overall assessment

Ask:

```text
Assess the available credit-risk information.
```

The agent should provide a summary similar to:

* Company documents and their verification status.
* Available financial values.
* Calculated financial ratios.
* External Credit Bureau Score: 720.
* Credit Bureau Status: No adverse records reported.
* Industry: Manufacturing.
* Any relevant information that is not available in the provided data.

The response should distinguish between **document facts** and **calculated financial ratios**. It should also make clear that the available information does not provide an industry risk rating or enough criteria to confirm a final credit decision.

The agent should not approve or reject the company based on the available information.

> **Note:** The exact wording and structure of the responses may vary because the responses are generated dynamically by the agents. Focus on verifying that the expected information is retrieved and passed through the multi-agent workflow.

### Additional test

You can also enter:

```text
help
```

The application should display example questions similar to:

```text
Example questions:
1. What company documents are available?
2. What financial information is available?
3. What are the financial ratios?
4. What is the external credit bureau score?
5. Assess the available credit-risk information.
```

When you are finished, enter:

```text
quit
```

to exit the application.


Type `quit` to exit. The agent may organize its answer differently, but it should not invent facts or a final credit decision.

### Summary

In this exercise, you use **Azure AI Agent Service with the A2A protocol** to build a Credit Risk Assessment application with multiple specialist agents.

The application follows this flow:

```text
User → CLI → Routing Agent → Specialist Agent → Answer
```

The Routing Agent sends each question to the appropriate specialist:

* **Document Verification Agent** — checks company documents, availability, status, and name matching.
* **Financial Analysis Agent** — provides financial information and calculates financial ratios.
* **Credit Risk Assessment Agent** — summarizes the available credit-risk information and identifies missing information.

The application reads the required information from the files in the `data/` folder rather than hardcoding company details or financial values in Python.

The main functions to review are:

* `load_all_data()` — loads the source documents.
* `compute_financial_ratios()` — calculates the required financial ratios.
* `send_message(...)` — sends requests between agents using A2A.
* `run_conversation(...)` — prepares the specialist agent's response.

You then run the application with:

```text
python run_all.py
```

and test company documents, financial ratios, credit bureau information, and the overall credit-risk assessment.

The application should **only use information available in the source documents**, clearly distinguish calculated values from document facts, and state when information is unavailable rather than inventing it.
