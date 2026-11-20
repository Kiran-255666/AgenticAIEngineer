# Capstone Project 02: AI-Powered Legal Document Review System

## 1. Project Statement

Create a multi-agent AI system that reviews legal documents, extracts important clauses, identifies potential compliance issues, and generates structured review reports.

The system must use RAG to retrieve relevant legal rules and reference documents to support its analysis and recommendations.

## 2. Technical Requirements

- Use the existing Microsoft Foundry project and its deployed models to ensure consistent project tracking, management, and evaluation.
- Create and configure the required agents, tools, and workflows in Microsoft Foundry.
- Test the agents using the Foundry Playground.
- Implement the complete application.
- Connect the Python application to the existing Foundry project using its endpoint and API key.
- Test the application and capture screenshots of the Foundry portal and Python application.

### Agent 1: Document Analysis Agent

- Accept legal documents in PDF or TXT or MD format.
- Extract document text and identify the document type.
- Extract important clauses, such as confidentiality, termination, liability, payment terms, and governing law.
- Identify missing, unclear, or potentially problematic clauses.
- Generate a structured document summary.

### Agent 2: Legal Compliance Agent

- Create high-quality synthetic legal rules, reference documents, and sample data. Use them as the knowledge sources for the assistant.
- Use RAG to retrieve relevant legal information.
- Compare extracted clauses against the retrieved references.
- Identify potential compliance issues and risks.
- Provide supporting explanations and references.
- Highlight issues that require human review.

### Multi-Agent Workflow

Create a workflow that connects **Agent 1 (Document Analysis Agent)** and **Agent 2 (Legal Compliance Agent)**.

1. Accept a legal document as input.
2. Send the document to Agent 1 for analysis and clause extraction.
3. Send the extracted clauses to Agent 2 for compliance checks.
4. Retrieve relevant legal references using RAG.
5. Combine the outputs from both agents.
6. Generate one final legal review report containing the document summary, extracted clauses, missing clauses, legal references, potential compliance issues, risks, and recommendations.

**Note:** Create only two agents. The workflow must make both agents work together. A third agent is not required.

## 3. Deliverables and Submission

Submit one ZIP file containing:

- Complete source code.
- Sample legal documents (`.md` or `.txt`).
- Sample legal rules and reference documents (`.md` or `.txt`).
- RAG implementation and document retrieval functionality.
- README with setup and usage instructions.
- PowerPoint presentation.
- Screenshots of the Foundry configuration, agent testing, workflow execution, document analysis, and final review report.

### Required Folder Structure

<details>
<summary><strong>View required folder structure</strong></summary>

Create a folder using your assigned name, such as `agenticuser99`.

Follow the project template:

```text
agenticuser99/
├── src/
├── data/
├── screenshots/
├── presentation/
├── README.md
└── .env.example
```

You can organize the folders and files according to your implementation.

</details>

### Folder Guidelines

<details>
<summary><strong>View folder guidelines</strong></summary>

- `src/`: Complete codebase. Organize agents, RAG, document processing, workflows, application files, and other source files as required.
- `data/`: Sample legal documents, legal rules, and reference documents (`.pdf`, `.csv`, `.md`, or `.txt`).
- `screenshots/`: Screenshots (`.png`) of the Foundry portal, agent configurations, Playground testing, workflow execution, and application results.
- `presentation/`: PowerPoint presentation (`.pptx`).
- `README.md`: Project overview, architecture, prerequisites, setup instructions, configuration, and execution steps.
- `.env.example`: Environment variable template with placeholder values only.

</details>

### PowerPoint Presentation

<details>
<summary><strong>View presentation requirements</strong></summary>

Your presentation should cover:

1. Project overview and problem statement.
2. System architecture.
3. Responsibilities of both agents.
4. RAG implementation.
5. Multi-agent workflow showing how both agents work together.
6. Technology stack and application demonstration.

</details>

### Environment Configuration

<details>
<summary><strong>View environment configuration instructions and example</strong></summary>

Include an `.env.example` file with the environment variables required by your application.

Example:

```env
AZURE_AI_PROJECT_ENDPOINT=your_project_endpoint
AZURE_AI_API_KEY=your_api_key
AZURE_AI_MODEL=your_deployed_model
AGENT_1_NAME=document_analysis_agent
AGENT_2_NAME=legal_compliance_agent
```

The example shows common configuration values. You can add other environment variables based on your project requirements.

Use the variable names required by your application. Include placeholder values only. **Never include actual API keys, passwords, or other secrets.**

</details>

### ZIP and Submission Instructions

1. Replace all actual values in `.env` with placeholders and save them in `.env.example` if you haven't done.
2. Delete the original `.env` file and virtual environment directories (`venv`, `.venv`).
3. Ensure your entire working project folder contains all required source code, data, screenshots, documentation, and presentation files.
4. Compress your entire working project folder into a ZIP file, keeping your assigned project folder (e.g., `agenticuser99`) as the root folder inside the ZIP.
5. Name the ZIP file after your assigned folder (e.g., `agenticuser99.zip`).
6. Upload the ZIP file to the provided submission link.

### Optional Video Demonstration

<details>
<summary><strong>View video demonstration guidelines</strong></summary>

A video demonstration is optional. A duration of less than 90 seconds is ideal.

</details>
