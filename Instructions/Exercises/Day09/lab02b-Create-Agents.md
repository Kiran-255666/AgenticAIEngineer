---
lab:
  title: Create agents with Copilot Studio
  module: Create agents in Microsoft Copilot Studio
  description: In this exercise, you will access the Microsoft Copilot Studio portal, select the appropriate environment, and create a new agent.
  duration: 55 minutes
  level: 200
  islab: true
  primarytopics:
    - Microsoft Copilot
    - Microsoft Copilot Studio
---

# Create agents with Copilot Studio

## Scenario

In this exercise, you will:

- Create an agent from a template
- Create and name an agent
- Define how the agent should behave using instructions
- Add a public website as a knowledge source
- Publish the agent and test with the Demo website

This exercise will take approximately **45** minutes to complete.

## What you will learn

- How to create an agent from a template
- How to create an agent using natural language
- How agent instructions influence generative behavior
- How Generative AI answers use configured knowledge sources
- How to publish an agent to the Demo website

## High-level lab steps

- Create an agent from a template
- Create an agent using Copilot
- Define agent behavior using instructions
- Add Generative AI knowledge sources
- Publish the agent

## Prerequisites

- Have a Microsoft Entra ID account
- Have a Copilot Studio license or have signed up for a free trial.
- Have access to a Power Platform environment and a solution where you can create agents and related assets.
- You can use:
  - the environment and **Lab Exercises** solution created in the **ILT Setup** lab, or
  - your own existing environment and solution.
- If you do not already have an environment and solution prepared, complete the steps in the **ILT Setup** lab before continuing.

## Key concept: Agent components and behavior

When generative orchestration is enabled, the agent can use instructions, knowledge, topics, and tools to generate responses dynamically.

## Exercise 1 - Create an agent from a template

In this exercise, you will create an agent by using a template, and then test the agent.

### Task 1.1 – Create an agent from the Safe Travels template

Open the **Copilot Studio** home page: `https://copilotstudio.microsoft.com/`

> [!IMPORTANT]
> You might notice a new Copilot Studio experience. Some features used in these labs are not available in the new experience, so for these labs use the **Classic Experience**.
>
> The image below shows the **Classic Experience** UI. If your interface looks like this, you're good to go. Continue to the next section. If it looks different, expand the section below and switch back to the **Classic Experience**.
>
> ![Copilot Studio Classic Experience interface.](../../media/olduserxp.png)
>
> <details>
> <summary>Does your interface look different? Click here</summary>
>
> ![Copilot Studio new experience interface.](../../media/newuserxp.png)
>
> Select **...** (More options) at the bottom of the page. Under **Explore**, select **Open Classic Experience** to switch back to the **Classic Experience**.
>
> </details>

1. In the **upper-right corner** of the page, verify that the **environment you created for this exercise** is selected. If the correct environment is not selected, follow [Task 1.3 - Access Copilot Studio](https://github.com/Kiran-255666/agentic-ai-azure-ai-foundry-labs/blob/main/Instructions/Exercises/Day-09/Lab-00-ILT-setup.md) in `Lab-00-ILT-setup.md`.

1. Select **Agents** in the left-hand navigation.

1. Under **Start with an agent template** section, select the **Safe Travels** template.

   ![Safe Travels template.](../../media/select-template.png)

1. In the upper-right of the page, select the ellipses (**...**) and select **Edit advanced settings**.

1. Validate that the selected *Solution* is **Lab Exercises** and the *Schema name* prefix is **fab** and select **Cancel**.

1. In the upper-right of the page, select **Create**.

1. In the **Overview** tab, review the name, description, and agent instructions.

1. Select the **Knowledge** tab and review the public website that has been added as a knowledge source.

1. In the upper-right of the page, select the **Settings** button.

   ![Safe Travels template.](../../media/sixset.png)

1. Verify that **Orchestration** is set to **No - Use classic orchestration, limiting responses to the content and behavior defined in your agent's topics**.

1. In the upper-right of the Settings page, select **X** icon to close settings.

1. Select the **Topics** tab and select the **System** filter.

   ![System Filter.](../../media/System.png)

1. Select the **Conversational Start** topic. Review the contents of the **Message** node. The message is displayed in the **Test** pane. The message content may vary slightly. The snippet below is provided for reference.
   
   ![Conversation Start topic from the Safe Travels template.](../../media/aaaaa.png)

1. In the drop-down in the upper-left of the page that is showing Conversation Start, select the custom **What can I ask** topic.
   
   ![Conversation Start topic from the Safe Travels template.](../../media/whatcaniask.png) 

### Task 1.2 – Test the agent

1. If the **Test** pane is not visible, select the **Test** icon in the upper-right of the page.

1. In the **Test** pane, select the ellipses (**...**) next to the **{x}** icon, then turn **Track between topics** **On**.

   ![Track between topics.](../../media/track-between-topics.png)

1. Enter the following prompt:

   ```prompt
   Hello
   ```

   The agent will use the default **Greeting** topic and respond with a greeting, typically asking how it can help you. The exact response may vary.

1. At the top of the **Test** pane, select the **Start new test session** icon **+**.

   ![New Session.](../../media/NewSessionn.png)

1. Enter the following prompt:

   ```prompt
   What can I ask?
   ```

   The **What Can I Ask** topic will be triggered and present several prompt options to continue the conversation.

1. Select the **How do I get a passport?** option.

   The response may vary slightly from the example shown below. It is generated using the configured knowledge source and may reference the **Conversational boosting** system topic.

   ![Screenshot of the test pane.](../../media/safe-travels-test.png)

1. Enter the following prompt:

   ```prompt
   What is Copilot Studio?
   ```

   The **Fallback** topic should be selected, and agent should ask you to try rephrasing.

1. Repeat the same prompt two more times. Depending on your environment and orchestration behavior, the agent may trigger the **Fallback** or **Escalate** system topics. You may see a response similar to: **I'm sorry, I'm not sure how to help with that. Can you try rephrasing?**

1. Select **Agents** in the left-hand navigation. The **Safe Travels** agent should be listed.

## Exercise 2 - Create an agent using Copilot

In this exercise, you will create a new agent using natural language to answer questions about government benefits.

### Task 2.1 – Create an agent to answer questions about government benefits

1. In the **Copilot Studio** home page `https://copilotstudio.microsoft.com/`, Verify that you are working in the environment you created earlier and that you are using the **Classic Experience** UI.

1. Select **Agents** in the left-hand navigation.

1. In the bottom-left of the *Start building by describing what your agent needs to do* text box, select the **Agent Settings** icon, which is displayed as a **⚙️** icon.

   ![Screenshot of the agent settings dialog.](../../media/agent-settings-dialog.png)

1. Leave **English (United States)** set as the primary language for the agent.

1. In the **Solution** drop-down, select **Lab Exercises**.

1. Enter `govbenefitsagent` for the *Schema name*.

   ![Screenshot of the Schema Name](../../media/SchemaName.png)

1. Select **Update**.

1. In the *Start building by describing what your agent needs to do* text box, Enter the following prompt:

   ```prompt
   You are an agent that assists with questions related to claiming US government benefits.
   ```

1. Select the **Send (→)** icon.

   Your agent will be created.

   ![Screenshot of the created agent.](../../media/new-agent-overview.png)

   Once your agent has been provisioned, you may proceed with configuring your agent.

### Task 2.2 – Configure the Overview tab

1. Select the **Overview** tab for the agent.

1. In the **Details** section, select **Edit**.

1. In the **Name** text box, enter **`US Benefits Assistant`**. If this name is already displayed, leave it unchanged and continue to the next step.

1. In the **Description** text box, enter **`Helps users with questions related to US government benefit programs`**.

1. Select **Save**.

1. In the **Select your agent's model** section, select **GPT-5 Auto (Preview)**, if available. Otherwise, select the default recommended GPT model.

1. In the **Instructions** section, select **Edit**.

1. Under *# General Guidelines* in the agent instructions, add the following:

   ```prompt
   - Do not provide legal advice.
   ```

1. Select **Save**.

   > [!NOTE]
   > Agent instructions guide how the agent should behave, but they do not strictly enforce behavior. In later labs, you will learn how to change behavior by using topics, knowledge, and generative answers with restricted knowledge sources.

1. Scroll down to the **Suggested prompts** section, then select **Add suggested prompts**.

1. For **Title**, enter `Health`.

1. For **Prompt**, enter `What health assistance programs are available for me?`.

1. Select **Save**.

### Task 2.3 – Add a public website as a knowledge source

1. Select the **Knowledge** tab.

   ![Knowledge tab in Copilot Studio portal.](../../media/knowledge-tab.png)

1. Select **+ Add knowledge**.

1. Select **Public websites**.

1. In the **Public website link** text box, enter **`https://www.usa.gov/benefits`**. This official government public website has details on benefits programs that could be useful for your agent.

1. Select **Add**.

1. For **Name**, enter `Government benefits`.

1. For **Description**, enter `This knowledge source contains information on government programs that may help you pay for food, housing, health care, and other basic living expenses`.

1. Select **Add to agent**.

   > [!NOTE]
   > Public website indexing may take several minutes. If responses are incomplete, wait a few minutes and test the agent again.

### Task 2.4 – Agent settings

1. In the upper-right of the page, select the **Settings** button.

1. Note that **Orchestration** is set to **Yes - Responses will be dynamic, using available tools and knowledge as appropriate**.

1. In the **Responses** section, enter the following:

   ```prompt
   - For process related answer respond with a single sentence.
   - For data-related answers respond with bullet points.
   ```

1. Scroll down you will find **Knowledge** section, set **Allow ungrounded responses** to **Off**.

1. In the **Knowledge** section, set **Use information from the Web** to **On**.

1. Select **Save**

1. In the left-hand side of the **Settings** page, select **Security**.

1. Select **Authentication**.

1. Select **No authentication** for this lab scenario to simplify testing in the Demo website channel.

1. Select **Save** and select **Save** again.

1. In the upper-right of the **Settings** page, select **X** to close settings.

### Task 2.5 – Test the agent

1. If the **Test** pane is not visible, select the **Test** icon in the upper-right of the page.

1. In the **Test** pane, select the ellipses (**...**) next to the variables **{x}** icon, and toggle **Show activity map when testing** to **On** and **Track between topics** to **Off**.

   ![Show activity map.](../../media/show-activity-map.png)

1. At the top of the **Test** pane, select the **Start new test session** icon **+**.

1. Enter the following prompt:

   ```prompt
   What health insurance information is available?
   ```

   The **Activity map** should be displayed, showing that knowledge sources were used to generate the response.

   ![Activity map.](../../media/activity-map.png)

1. Close the **Test** pane.

### Task 2.6 – Publish the agent to the Demo website

1. In the action bar of the agent, select the **Publish** button and select **Publish** again.

1. Select the **Channels** tab.

   ![Screenshot of Channels in Copilot Studio.](../../media/channels-tab.png)

1. Select the **Demo website** channel. This channel is useful for quickly testing and previewing your agent experience.

1. In the **Demo Website** pane, enter the following settings:

   - **Welcome message**: `Ask me about government benefit programs`
   - **Conversation starters**:

      ```prompt
      "Hello"
      "What programs am I entitled to?"
      "What is social security?"
      ```

1. Select **Save**.

1. Select **Open demo website**.

1. Enter the following prompt:

   ```prompt
   What welfare and assistance can I claim for?
   ```

   The response should reference information from the configured knowledge source and may include citations or source references.
   
   ![Screenshot of Channels in Copilot Studio.](../../media/finaloo.png)

1. Try a few more questions and view the responses from your agent. It will have limited functionality, but should be able to provide relevant answers to questions about benefits.

## Summary

In this lab, you created an agent and defined its expected behavior using instructions. You also added a public website as a knowledge source and tested your agent with questions that the knowledge source could help answer. Later labs will show how to use topics, knowledge, and tools to further control agent behavior.
