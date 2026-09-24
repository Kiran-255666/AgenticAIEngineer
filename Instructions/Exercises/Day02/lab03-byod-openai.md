---
lab:
  title: Utilize prompt engineering in your app
  description: Learn how different prompt structures shape a generative AI model's response, then build a Python app to test them.
  level: 200
  duration: 30
  islab: true
  status: 'released'
---

# Utilize prompt engineering in your app
**Note: We have already updated the mentioned files with the code mentioned in the instructions, but we would highly suggest going through it before executing it**

How you write a prompt has a direct effect on how an Azure OpenAI model responds. The model can tailor and format its output if you ask clearly, but the same request phrased two different ways can produce very different results.

In this exercise, you'll play the role of a developer on a wildlife marketing team. You're testing how generative AI can improve advertising emails and sort articles for your team. The prompt techniques you'll practice apply just as well to other use cases beyond this one.

This exercise takes approximately **30** minutes.

## Prerequisites

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account)
- [Python 3.13](https://www.python.org/downloads/) or later installed
- **Azure CLI** installed. [Install Azure CLI](https://aka.ms/installazurecliwindows)
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- A web browser
- Basic familiarity with running commands in a terminal (you don't need to know Python already; the code is provided)

> A Foundry project with a language model already deployed has been set up for you. If you completed the previous exercise, you may already have the **endpoint** and **deployment name** saved.
>
> **Important:** Copy both values into a local text file (for example, Notepad) and keep them somewhere safe, as you'll use them repeatedly throughout these labs.
>
> **Security note:** Treat your endpoint and deployment details as sensitive information. Never share them publicly, or paste them into online websites, AI assistants, forums, or chats. If you ever need to share screenshots or logs, mask or redact your endpoint, URLs, API keys, and any other sensitive information first.

# Find your project endpoint and deployment name

1. If you already saved your **endpoint** and **deployment name** from a previous exercise, skip ahead to **Explore prompt engineering techniques**. Otherwise, follow the steps below.
1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in with your Azure credentials. Close any tips or quick-start panes that appear the first time you sign in.
1. On the home page, select your project. (If you have more than one, pick the one your trainer or lab environment set up for this exercise.)

    ![Screenshot of the Foundary Portal showing your project details.](../../media/home-page.png)

    Selecting your project takes you straight to its home page.

    ![Screenshot of the Foundry project home page, showing the API key, Project endpoint, and Azure OpenAI endpoint fields.](../../media/project-home-page-1.png)

1. To confirm the name of your deployed model, use any of these:
    - Under **Use a model**, select **View deployments**

        ![Screenshot of the View deployments page, listing the deployed model name.](../../media/view-deployments.png)

    - On the same home page scroll down, check the **Recent work** or **All** section

        ![Screenshot of the Recent work / All section on the home page, showing the deployed model.](../../media/recent-work-all.png)

    - In the top menu, select **Build**, then **Models**

        ![Screenshot of the Build menu with Models selected, showing the deployed model name.](../../media/build-models.png)

    Note this exact name too.
1. On the project home page, find the **Project endpoint** field and copy the value shown there directly. This is the web address your app will use to reach your project and model. (The **Azure OpenAI endpoint** field, shown next to it, works too if you prefer to use that instead.)

    ![Screenshot of the API key, Project endpoint, and Azure OpenAI endpoint fields, with the copy icon next to Project endpoint highlighted.](../../media/project-endpoint-copy.png)

1. Copy both the endpoint and the deployment name into a local text file and save it somewhere safe. You'll paste these values into a configuration file later in this exercise, and you'll need them again in later exercises.

    > **Tip**: If you don't see a project or a deployment here, check with your trainer before continuing.

# Explore prompt engineering techniques

In this section, you'll use the deployed model playground in Microsoft Foundry to see how instructions and examples change the model's response.

1. If you are not already on the project home page, open the [Microsoft Foundry portal](https://ai.azure.com), select your training project, and open **Home**.

1. In the **Use a model** card, select **View deployments**.

    ![Screenshot of the Foundry project home page with View deployments selected.](../../media/1.png)

1. In **Models** > **Deployments**, select the deployed chat model provided for the lab.

1. In the model details pane, select **Open in playground**.

    ![Screenshot of the Models deployments page with a deployed model selected and the Open in playground button available.](../../media/22.png)

1. The model playground opens. Verify that the selected deployment is shown at the top of the left pane.

    The playground has two main areas:

    - **Instructions**: Where you define the model's behavior and response format.
    - **Chat**: Where you send prompts and review responses.

    ![Screenshot of the new Foundry model playground with Instructions and Chat panes.](../../media/3.png)

1. In **Instructions**, verify that the following default instruction is present:

    ```text
    You are an AI assistant that helps people find information.
    ```

1. If the instruction is not present, enter it manually.

1. In the **Chat** message box, submit the following prompt:

    ```text
    What kind of article is this?
    ---
    Severe drought likely in California

    Millions of California residents are bracing for less water and dry lawns as drought threatens to leave a large swath of the region with a growing water shortage.

    In a remarkable indication of drought severity, officials in Southern California have declared a first-of-its-kind action limiting outdoor water use to one day a week for nearly 8 million residents.

    Much remains to be determined about how daily life will change as people adjust to a drier normal. But officials are warning the situation is dire and could lead to even more severe limits later in the year.
    ```

1. Review the response. With the default instruction, the model will usually describe or summarize the article instead of returning one category label.

1. In **Instructions**, replace the default instruction with the following:

    ```text
    You are a news classification assistant.

    Categorize each news article using a single category label.

    Respond with only one of these categories:
    News, Sports, Entertainment, Technology, Business, Health, Science, or Other.
    ```

1. In the **Chat** pane, submit the following prompt. This prompt includes examples directly in the message because the new playground does not provide separate User and Assistant example fields.

    ```text
    Classify each article using exactly one category:
    News, Sports, Entertainment, Technology, Business, Health, Science, or Other.

    Example 1:
    Article:
    New York Baseballers Wins Big Against Chicago

    New York Baseballers mounted a big 5-0 shutout against the Chicago Cyclones last night.

    Category:
    Sports

    Example 2:
    Article:
    Joyous moments at the Oscars

    This year's Academy Awards were full of emotional performances, laughs, and memorable moments.

    Category:
    Entertainment

    Now classify this article:
    ---
    Severe drought likely in California

    Millions of California residents are bracing for less water and dry lawns as drought threatens to leave a large swath of the region with a growing water shortage.

    In a remarkable indication of drought severity, officials in Southern California have declared a first-of-its-kind action limiting outdoor water use to one day a week for nearly 8 million residents.

    Much remains to be determined about how daily life will change as people adjust to a drier normal. But officials are warning the situation is dire and could lead to even more severe limits later in the year.

    Return only the category.
    ```

1. Verify that the model returns a single category label similar to:

    ```text
    News
    ```

    This demonstrates that clear instructions, a defined output format, and examples help produce more consistent responses.

1. In **Instructions**, replace the classification instruction with the following default instruction:

    ```text
    You are an AI assistant that helps people find information.
    ```

1. In the **Chat** pane, submit the following prompt:

    ```text
    # 1. Create a list of animals
    # 2. Create a list of whimsical names for those animals
    # 3. Combine them randomly into a list of 25 animal and name pairs
    ```

1. Review the response. The model may treat the prompt as a plain-language request instead of a request for executable code.

1. In **Instructions**, replace the instruction with:

    ```text
    You are a coding assistant helping write Python code.
    ```

1. Send the same animal-and-name prompt again.

1. Review the response. The model should now produce Python code that creates lists of animals and names, then combines them into pairs.

1. When you finish testing, you can leave the playground open or return to the project home page to continue with the application section.

# Get the application files from GitHub

1. If you already downloaded and extracted this repository's ZIP file in a previous exercise, skip ahead to the next step, and navigate directly to the folder path below. Otherwise, follow the steps below to download it first.
1. Open a web browser and go to the [lab files on GitHub](https://github.com/Kiran-255666/agentic-ai-azure-ai-foundry-labs).
1. On the repository page, select the green **`<> Code`** button, and then select **Download ZIP**.

    ![Screenshot of the Code button.](../../media/code.png)

1. Once the download finishes, locate the ZIP file and extract it to a folder on your computer.
1. In the extracted folder, navigate to:

    ```
    labfiles\Day-01-summary\lab-02-bring-your-own-data-to-open-ai\python\
    ```

    This folder already contains everything you need for this exercise: `.env`, `grounding.txt`, `prompt_engineering.py`, `requirements.txt`, and `system.txt`.

    > **Tip**: If you're not sure which folder contains the exercise files, check with your trainer.

1. In **File Explorer**, select the address bar at the top of the window, type the following command, and press **Enter**:

    ```
    code .
    ```

    This opens the folder directly in Visual Studio Code.

    > **Tip**: If `code .` doesn't work, open the folder manually in Visual Studio Code.

## Configure your application

1. In Visual Studio Code, open the `.env` file. It already contains placeholder values:

    ```env
    AZURE_OPENAI_ENDPOINT=https://your_azure_openai_endpoint/openai/v1/
    AZURE_OPENAI_API_KEY=your_azure_openai_api_key
    AZURE_OPENAI_DEPLOYMENT=your_azure_openai_deployment
    ```

1. Replace each placeholder with the actual Azure OpenAI value you copied or saved earlier.

    > **Important**: Keep your Azure OpenAI API key private. Never share it or commit the `.env` file to a public repository.

1. Open `prompt_engineering.py` and review the code.

    The application is already configured to read the Azure OpenAI settings from the `.env` file, so you don't need to enter the endpoint, API key, or deployment directly in the Python code.

1. Review `system.txt` and `grounding.txt`. These files are already provided and contain the system instructions and grounding information used by the application.
1. Check `prompt_engineering.py` for any indentation issues before running it. Python uses indentation to define blocks of code, so an incorrectly indented line can cause an error when you execute the script.
1. Save your changes.

## Create a Python virtual environment

1. In the Visual Studio Code terminal, make sure you're in the exercise's `python` folder.

2. Create a virtual environment named `.venv`:

   ```powershell
   python -m venv .venv
   ```

   > **Note:** If `python -m venv .venv` returns an error in the Virtual Machine, use the Windows Python Launcher instead:
   >
   > ```powershell
   > py -m venv .venv
   > ```

3. Activate the virtual environment:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   After activation, you should see `(.venv)` at the beginning of the terminal prompt.

   > **Tip:** If PowerShell prevents the activation script from running, open a Command Prompt terminal and use:
   >
   > ```cmd
   > .venv\Scripts\activate.bat
   > ```

4. Install the required packages:

   ```powershell
   pip install -r requirements.txt
   ```


## Run your application

The `system.txt` file contains the system message that the application sends to the model. You'll edit and save this file between iterations. The application pauses each time so you can update the system message before sending the next request.

1. Make sure the virtual environment is activated and that you're in the exercise's `python` folder.
1. Run the application:

    ```powershell
    python prompt_engineering.py
    ```

1. When the application pauses and asks you to continue, open `system.txt` in Visual Studio Code.
1. Replace the contents of `system.txt` with the following system message, and save the file:

    ```text
    You're an AI assistant who helps people find information. You'll provide answers from the text provided in the prompt, and respond concisely.
    ```

1. Return to the terminal and press **Enter** when prompted to continue.
1. When prompted for the user message, enter:

    ```text
    What animal is the favorite of children at Contoso?
    ```

1. Review the model's response.

    ![Screenshot of the terminal in Visual Studio Code, showing the .env file with placeholder values and the app's output after asking about Contoso's favorite animal.](../../media/result-01-02.png)

1. Continue with the remaining iterations in the exercise by editing and saving `system.txt`, then entering the specified user message when prompted.

## Summary

You explored how system instructions and examples can influence a model's responses in the Chat playground. You then created a Python virtual environment and ran an application that reads configuration from a `.env` file and sends different system messages and user prompts to your deployed Azure OpenAI model.
