---
lab:
  title: Explore Azure AI Foundry and call a deployed model
  description: Learn how to navigate Azure AI Foundry, test a deployed model in the Chat Playground, and call it from a Jupyter notebook using the SDK and REST.
  level: 200
  duration: 30
  islab: true
  status: 'released'
---

# Explore Azure AI Foundry and call a deployed model

**Note: This document has three parts. Part 1 is an optional fundamentals recap that you can open if you want a refresher. Part 2 is a tour of the Azure AI Foundry portal. Part 3 sends you to the lab notebook, where you run the code.**

In this exercise, you will use a project and a model deployment that are already set up for you. You will find them in the Azure AI Foundry portal, test the deployed model in the Chat Playground, and then call the same model from a Jupyter notebook using the OpenAI SDK and REST.

This exercise takes approximately **30** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may see unexpected behavior, warnings, or errors.

## What you will use in this lab

You do not create a project, and you do not deploy a model. Both are ready for you.

- **Project:** The workspace in Azure AI Foundry that holds your model deployment, your endpoint, and your key. Your project is already created.
- **Deployed model:** A model that is running and ready to receive requests. In this lab, the deployed model is **gpt-5.4-mini**.

Because of this, the lab only uses the terms and settings that help you work with an existing project and an existing deployment. Parts of the portal that are used to create or deploy things are described briefly so that you recognize them, but you do not need to use them.

If you cannot see your project or the **gpt-5.4-mini** deployment, tell the instructor before you continue.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- Python 3.12.1 available as a kernel
- The **Python (Microsoft)** and **Jupyter (Microsoft)** extensions installed and enabled in VS Code
- Microsoft Edge (or another web browser)
- Basic familiarity with running notebook cells (you do not need to know Python already; the code is provided)

> A Foundry project with the **gpt-5.4-mini** model already deployed has been set up for you. If more than one AI Foundry resource is available, ask the instructor which resource to use. Use the resource and model from the demonstration unless the instructor tells you otherwise.
>
> **Important:** Copy the endpoint and the key into a local text file (for example, Notepad) and keep them somewhere safe. You will use them in the notebook.
>
> **Tip:** Keep the Azure AI Foundry project page open in Microsoft Edge for easy access during the lab.

---

# Part 1: Fundamentals recap (optional)

Open any section below if you want to refresh a concept. You can skip this part and come back to it later. Every concept here appears in the lab.

<details>
<summary><strong>What generative AI is</strong></summary>

Generative AI refers to models that learn patterns from large datasets and then produce new content. The content can be text, code, images, audio, video, or structured JSON.

A discriminative model decides which class an input belongs to. A generative model creates new content that fits the patterns it learned.

- **Discriminative example:** "Is this email spam?" The model answers with a class, such as spam or not spam.
- **Generative example:** "Draft a reply to this email in a friendly tone." The model writes new text.

Cloud platforms such as Azure AI Foundry let you use these models through a web portal (the playground) and through code (an API).

</details>

<details>
<summary><strong>What a large language model is and how it produces text</strong></summary>

A large language model (LLM) is a neural network that is trained on very large amounts of text and code to predict the next token. A model that predicts the next token well can write sentences, answer questions, follow instructions, write code, and return information in a fixed format.

These ideas explain how an LLM produces a reply:

- **Token:** A small piece of text, often a part of a word. The model reads and writes tokens. Length limits and cost are counted in tokens, not in characters or words. For example, the word "Internationalization" can be split into the tokens "International" and "ization".
- **Embedding:** A list of numbers that represents the meaning of a token. The model works with these numbers.
- **Next-token prediction:** The model reads your prompt, predicts the most suitable next token, adds it to the text, and repeats this step until the reply is complete.
- **Context window:** The largest number of tokens that the prompt and the reply can use together. If a request needs more tokens than the context window allows, the request fails or the text is cut off.
- **Training:** The model first learns general language patterns from a very large set of text and code. Later training steps teach it to follow instructions and to respond in a helpful and safe way. This training is already finished for the model you will use.

</details>

<details>
<summary><strong>The settings you will use in the lab</strong></summary>

You control the model's reply with the settings below. The notebook uses the first five. The last two are in the playground and in the notebook as optional controls.

- **System message:** An instruction that sets the role, the tone, and the format rules for the model. For example, "You are a concise Azure assistant." or "Return ONLY valid JSON."
- **User message:** Your question or task. The model answers it.
- **Maximum output tokens (`max_output_tokens`):** The largest number of tokens the reply can contain. A smaller limit gives shorter replies and lower cost. If the limit is too small, the reply is cut off.
- **Streaming (`stream=True`):** The reply arrives in small parts while the model writes it, instead of arriving as one block after it finishes. The total number of tokens does not change.
- **JSON output:** You ask for a reply in JSON, with fixed keys, so that code can read the reply reliably. Your code should still check that the reply is valid JSON before it uses it.
- **Reasoning effort (`reasoning`):** For models that support it, this setting controls how much the model reasons before it writes the answer. The reasoning uses tokens, and those tokens count toward `max_output_tokens`. When the limit is very small, reasoning can use all the tokens and leave no room for the answer. The notebook explains what to do in that case.
- **Temperature and top-p:** These settings control how varied the reply is. A lower temperature gives more consistent replies, and a temperature near 0 gives the most predictable ones. A higher temperature gives more varied replies. Top-p limits the choice to the smallest group of likely tokens whose probabilities add up to the value p. Some models do not allow you to change these two settings.

</details>

<details>
<summary><strong>Terms you will see in the lab</strong></summary>

- **Project:** The workspace in Azure AI Foundry that contains your deployment, endpoint, and key.
- **Deployment:** A model that is running in your project and can receive requests. Your deployment is **gpt-5.4-mini**.
- **Deployment name:** The name that your code sends in the `model` field. In this lab, it is `gpt-5.4-mini`.
- **Endpoint:** The web address that your code sends requests to.
- **API key:** A secret value that proves your code is allowed to use the deployment. Treat it like a password. Do not share it, and do not paste it in public places.
- **Responses API:** The API that the notebook calls. You send messages to it and it returns the model's reply.
- **SDK:** A code library that makes the API easier to call. The notebook uses the OpenAI Python SDK.
- **REST:** Calling the API directly with an HTTP request. The notebook shows one REST call with the `requests` library.
- **Playground:** A page in the portal where you try prompts without writing code.
- **Hallucination:** A reply that sounds confident but is wrong or has no basis. Check important answers against a reliable source.
- **Grounding:** Giving the model trusted information to base its answer on, so that the answer relies on that information.

</details>

<details>
<summary><strong>Safe use of a model</strong></summary>

- Do not send secrets, passwords, or personal data in a prompt.
- Keep your API key private. Remove the key from the notebook before you save or share it.
- Check important answers, because a model can produce wrong content.
- Keep the system message clear, so that the model knows the role and the format that you expect.

</details>

<details>
<summary><strong>Self-check with answers</strong></summary>

1. **What is the difference between a generative model and a discriminative model?**
   A generative model creates new content. A discriminative model decides which class an input belongs to.

2. **Which setting do you lower to make replies more consistent?**
   The temperature.

3. **What is the context window, and why does it matter for cost and latency?**
   The context window is the largest number of tokens that the prompt and the reply can use together. A request with more tokens costs more and takes longer to process.

4. **Name one risk of using a model and one way to reduce it.**
   One risk is hallucination. You reduce it by checking important answers against a reliable source.

5. **Where do you find the endpoint and the key of your deployment?**
   On the **Details** tab of the deployed model page in the Azure AI Foundry portal.

</details>

---

# Part 2: Explore Azure AI Foundry

In this part, you will explore the Azure AI Foundry portal. No coding is required. You will use the project and the **gpt-5.4-mini** deployment that you created earlier.

## Open Your Project

1. Navigate to the Azure AI Foundry portal: <https://ai.azure.com/>.
2. Sign in with your Azure account.
3. Open the project that you created in Part 1.

> **Note:** After you sign in to Microsoft Foundry (`ai.azure.com`), you may be redirected to the **All Resources** page. This page displays the AI Foundry resources and projects available in your Azure subscription.

![Screenshot of the Foundry portal showing your project.](../../media/AllResources_Page.png)

## Overview of the All Resources Page

### Top Section

| Location | Description | Use |
|----------|-------------|-----|
| Recent Projects | Displays projects that were recently accessed. | Quickly reopen an existing project and continue your work. |
| Create Project | Creates a new AI Foundry project. | Create a new project for building AI applications, agents, and solutions. |

### Resource List Section

| Location | Description | Use |
|----------|-------------|-----|
| Search | Search box for resources and projects. | Find a specific project or resource. |
| Type Filter | Filters resources by resource type. | Display only selected resource types. |
| Subscription Filter | Filters resources by Azure subscription. | Display resources from a specific subscription. |
| Region Filter | Filters resources by Azure region. | Display resources deployed in a selected region. |
| Name | Displays the project name. | Select a project to open and manage it. |
| Type | Displays the resource type. | Identify the type of resource. |
| Parent Resource | Displays the AI Foundry resource associated with the project. | Identify the resource that hosts the project. |
| Subscription | Displays the Azure subscription associated with the resource. | Verify resource ownership and billing context. |
| Region | Displays the Azure region where the resource is | Displays the account that created the resource. | Identify the creator of the resource. |

4. Select your project from the resource list to open it.
5. Wait for the project dashboard to load before proceeding to the next section.

## 1) The page header and navigation

![Screenshot of the project page header and navigation.](image.png)

- **Header (top-left):** Shows Microsoft Foundry and the name of your project. This tells you which project you are working in.
- **Search with AI (top-center):** Searches resources, settings, models, and tools across Foundry. You can open it by pressing the Ctrl and K keys together.
- **Home (top-right):** Shows the main dashboard of the project, with resources, endpoints, and quick-start options.
- **Discover (top-right):** Lets you explore available models, examples, and capabilities.
- **Build (top-right):** Is used to create, configure, and deploy AI applications and agents. You do not use it in this lab.
- **Operate (top-right):** Is used to monitor deployments, review usage, and troubleshoot running solutions.
- **Manage (top-right):** Is used to manage project settings, permissions, connections, and resources.
- **Docs (top-right):** Opens Microsoft documentation, tutorials, and learning materials.
- **Main heading (Welcome):** Shows the name of the account that is signed in.

## 2) The main project cards

![Screenshot of the main project cards.](image.png)

**Use a model**

- Located on the left.
- Lets you manage existing endpoints or deploy a new model.
- The **View deployments** button opens the list of model deployments. You will use this button to find **gpt-5.4-mini**.

**Build an agent**

- Located on the top-right.
- Lets you create an AI agent by configuring instructions, tools, and knowledge, without writing code.
- You do not use it in this lab.

**Code an agent**

- Located below Build an agent.
- Lets you define and deploy an agent in code with the Microsoft Agent Framework.
- You do not use it in this lab.

## 3) Endpoints and API key

Below the main cards, you can see three fields:

![Screenshot of the API key, Project endpoint, and Azure OpenAI endpoint fields.](image.png)

**API key**

- The key is masked.
- A copy icon is on the right.
- Keep the key private.

**Project endpoint**

- Shows the endpoint of your Azure AI Foundry project.
- A copy icon is available.
- Code uses this endpoint to connect to the project.

**Azure OpenAI endpoint**

- Shows the Azure OpenAI endpoint.
- A copy icon is available.
- Code uses this endpoint to work directly with the Azure OpenAI APIs.

In this lab, you take the endpoint and the key from the **Details** tab of the deployed model, as shown later in "Find your endpoint and key".

## 4) Model selection

Below the endpoint section, a Model selection area has three cards:

![Screenshot of the Model selection cards.](image.png)

**Test in playground**

- Lets you run prompts and see responses without writing code.
- You will use it in this lab.

**Explore models**

- Lets you browse the models that are available.
- You will look at it next.

**Compare models**

- Lets you review benchmarks and capabilities of models side by side.
- You will look at it next.

## 5) Available models

At the bottom of the page, the portal lists available models, for example:

- claude-fable-5-1 (Anthropic)
- gpt-6-astra (OpenAI)
- MAI-Image-2.6 (Microsoft)
- DeepSeek-V4-Flash (DeepSeek)

Arrows on the left and right show more models. You do not need to choose one of these. Your lab uses **gpt-5.4-mini**.

## 6) Recent work

The Recent work section has three filters: **All**, **Agents**, and **Models**.

It shows the models and projects that you opened recently in a table with these columns: Name, Version, Type, Last viewed, and Endpoint. **gpt-5.4-mini** appears here after you open it. The **View endpoint** link in each row opens the endpoint information of that model. Prev and Next buttons at the bottom move between pages of the table.

## 7) Learning and resources

Further down, the Learning and resources section has three options:

- **Docs:** Explore the detailed Microsoft Foundry documentation.
- **GitHub:** Get the latest SDK updates and code samples.
- **Discord:** Join the Microsoft Foundry community and ask questions.

# Explore the model catalog

The model catalog helps you find and compare models. In this lab, the model is already chosen for you. This tour shows you where the information is, so that you can find it in your own projects later.

## Open the model catalog

1. On the project home page, under Model selection, click **Explore models**.

    ![Screenshot of the Explore models card.](image.png)

    The Models catalog opens. It lists the models that you can browse.

## The catalog page

![Screenshot of the Models catalog.](image.png)

At the top of the page, you can see:

- **Models:** The number of models that the catalog lists.
- **Search:** Finds a model by name.
- **Sort by:** Changes the order of the list. The default is Featured.
- **Compare models:** Lets you select models and compare their capabilities and performance.
- **View leaderboard:** Shows performance measurements of models in several categories.

The left side of the page has two availability options:

- **All models:** Shows every model in the catalog.
- **Available in my project:** Shows the models that your project can use.

The left side also has filters that narrow the list. These are the filters you are most likely to use:

- **Collections:** Filter by collection.
- **Publisher:** Filter by the company that provides the model.
- **Supported features:** Filter by the features a model supports.
- **Inference tasks:** Filter by the kind of task a model performs, such as chat or image generation.
- **Region:** Filter by the regions where a model is available.

The catalog has more filters for deployment options, fine-tuning, lifecycle, domain, and industry. You do not need them in this lab.

The main area shows one entry for each model. Each entry shows the model name, the publisher, and the task types the model supports, such as Chat completion, Responses, Messages, Text to image, or Speech to text.

## Compare models

1. Click **Compare models** at the top-right of the model catalog.

    ![Screenshot of the Compare models button.](image.png)

    The comparison page shows several models side by side. For each model, it can show:

    - Model name and version
    - Deploy option
    - View details
    - Quality
    - Safety
    - Estimated cost
    - Throughput
    - Input types
    - Output types
    - Context window
    - Maximum output
    - Training date

1. Click the **Add model** button to add another model to the comparison.

    This helps you check the capabilities of models against what your application needs.

## View the leaderboard

1. Go back to the model catalog and click **View leaderboard**.

    ![Screenshot of the Model leaderboard.](image.png)

    The leaderboard compares models by benchmark results in four areas:

    - **Quality:** The quality index of the model.
    - **Safety:** The measured attack success rate. A lower value is better.
    - **Throughput (tokens per second):** The number of output tokens that the model generates each second. A higher value is better.
    - **Benchmark cost:** The cost of running the evaluation datasets. A lower value is better.

1. Below the charts, select individual models to compare their quality index, safety, throughput, and benchmark cost.

    > **Tip:** Leaderboard results are benchmark measurements. To judge a model for your own application, test it with your own prompts in the Playground.

# Test the deployed model in the Chat Playground

You will now try the model that is already deployed in your project.

> **Note:** Use the existing **gpt-5.4-mini** deployment. Do not create another deployment. Extra deployments use resources that the lab does not need.

## Open the Chat Playground

1. Go back to the project home page.

1. Under Model selection, click **View deployments**.

    ![Screenshot of the View deployments button.](image.png)

1. Select the deployed **gpt-5.4-mini** model.

1. On the **gpt-5.4-mini** deployment page, click **Playground**.

    ![Screenshot of the Playground button on the deployment page.](image.png)

    The Playground opens with these main areas:

    ![Screenshot of the Playground layout.](image.png)

### The Playground areas

1. **Model and deployment:** Shows the model (gpt-5.4-mini) and the deployment type (Global Standard). The **Save as agent** button saves the current configuration as an agent. The **Compare models** button compares this model with others.
1. **Navigation tabs:** At the top of the deployment page, these tabs are available:
    - **Playground:** Test prompts and interact with the model.
    - **Details:** View information about the deployment and the model. You will use this tab to find your endpoint and key.
    - **Monitor:** View usage, requests, token counts, cost, and performance metrics.
    - **Evaluation:** Evaluate model behavior and configure evaluators.
1. **Instructions:** Holds the system-level instructions that guide how the model responds. This is where you set the system message.
1. **Tools:** Connects additional tools to the model. For example, Web search can add web-based information when it is turned on.
1. **Knowledge:** Lets you upload files or connect knowledge sources that give the model more context. Use the **Add** button for this.
1. **Memory:** Holds memory settings for the model or agent.
1. **Guardrail:** Holds safety controls for managing and testing model behavior.
1. **Chat:** The place where you talk to the model. Type a prompt in the chat input, for example "Explain Azure AI Foundry in simple terms.", and click **Call model**. The response appears in the chat area.

In this lab, you mainly use **Instructions** and **Chat**. The other areas are described so that you recognize them.

## Try the Playground

1. Enter the prompt "Explain Azure AI Foundry in two sentences" and press Enter.

    ![Screenshot of the playground response.](image.png)

    The reply appears in the chat area. Notice that the reply follows your request for two sentences.

# Find your endpoint and key

Your code needs the endpoint and the key of the deployment.

1. On the deployed model page, click the **Details** tab next to Playground.

    ![Screenshot of the Details tab showing the endpoint and key.](image.png)

1. Copy the **Endpoint** and the **Key**.

1. Save both values somewhere safe, such as Notepad. You will paste them into the notebook.

1. In the endpoint, remove everything after `/v1/`.

    For example:

    - Endpoint shown: `https://<your-resource-name>.services.ai.azure.com/openai/v1/responses`
    - Endpoint to use: `https://<your-resource-name>.services.ai.azure.com/openai/v1/`

1. Keep the key exactly as it is, and keep it private.

---

# Part 3: Run the lab

You now know the concepts that the lab uses, and you know where to find your project, your deployed model, the Playground, the endpoint, and the key. Next, run the code in the lab notebook.

### Prepare the application configuration

1. Open a web browser and go to the [GitHub](https://github.com/Kiran-255666/AgenticAIEngineer).
1. On the repo page, select the green **`<> Code`** button, then select **Download ZIP**.

    ![Screenshot of the Code button.](../../media/code.png)
1. Once the download finishes, locate the ZIP file and extract it to a folder on your computer. **Ensure that there are no other ZIP files or extracted folders with the same name in the Downloads folder.**

## Summary

You used a project and a model deployment that were already set up for you. You learned the concepts that the lab uses, you toured the Azure AI Foundry portal, you tested **gpt-5.4-mini** in the Chat Playground, and you found the endpoint and key that your code needs. You now have the knowledge to run the lab.

---

**Next step:** Open [AgenticAIEngineer/labfiles/Day01/lab01-azure-ai-foundry.ipynb at main · Kiran-255666/AgenticAIEngineer](https://github.com/Kiran-255666/AgenticAIEngineer/blob/main/labfiles/Day01/lab01-azure-ai-foundry.ipynb) and run the notebook as it instructs.