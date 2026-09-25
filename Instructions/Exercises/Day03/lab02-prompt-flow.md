# Use a prompt flow to manage conversation in a chat app

## Prerequisites

For this lab, the following have already been configured:

- Microsoft Foundry hub and project
- Resource authorization and storage access
- Required Azure resources
- **GPT-5.4-mini** model deployment

Use the existing resources and proceed directly to **Create a prompt flow**.

## Create a prompt flow

A prompt flow provides a way to orchestrate prompts and other activities to define an
interaction with a generative AI model.

In this exercise, you'll use a template to create a basic chat flow for an AI assistant
in a travel agency.

1. In the Foundry portal navigation bar, in the **Build and customize** section,
   select **Prompt flow**.

2. Create a new flow based on the **Chat flow** template, specifying `Travel-Chat`
   as the folder name.

   A simple chat flow is created for you.

   > **Tip:** If a permissions error occurs, wait a few minutes and try again,
   > specifying a different flow name if necessary.

3. To be able to test your flow, you need compute, and it can take a while to start.

   Select **Start compute session** to get it started while you explore and modify
   the default flow.

4. View the prompt flow, which consists of a series of inputs, outputs, and tools.

   You can expand and edit the properties of these objects in the editing panes on
   the left, and view the overall flow as a graph on the right.

   ![Screenshot](../../media/a5.png)

5. View the **Inputs** pane, and note that there are two inputs:

   - Chat history
   - The user's question

6. View the **Outputs** pane and note that there's an output to reflect the model's
   answer.

7. View the **Chat LLM** tool pane, which contains the information needed to submit
   a prompt to the model.

8. In the **Chat LLM** tool pane, for **Connection**, select the connection for the
   Azure OpenAI service resource in your AI hub.

   Then configure the following connection properties:

   - **Api:** `chat`
   - **deployment_name:** The `gpt-4o` model you deployed
   - **response_format:** `{"type":"text"}`

9. Modify the **Prompt** field as follows, removing the `\` escape in the YAML loop:

   ```text
   # system:
   **Objective**: Assist users with travel-related inquiries, offering tips, advice, and
   recommendations as a knowledgeable travel agent.

   **Capabilities**:
   - Provide up-to-date travel information, including destinations, accommodations,
     transportation, and local attractions.
   - Offer personalized travel suggestions based on user preferences, budget, and travel
     dates.
   - Share tips on packing, safety, and navigating travel disruptions.
   - Help with itinerary planning, including optimal routes and must-see landmarks.
   - Answer common travel questions and provide solutions to potential travel issues.

   **Instructions**:
   1. Engage with the user in a friendly and professional manner, as a travel agent
      would.
   2. Use available resources to provide accurate and relevant travel information.
   3. Tailor responses to the user's specific travel needs and interests.
   4. Ensure recommendations are practical and consider the user's safety and comfort.
   5. Encourage the user to ask follow-up questions for further assistance.

   {% for item in chat_history %}
   # user:
   {{item.inputs.question}}
   # assistant:
   {{item.outputs.answer}}
   {% endfor %}

   # user:
   {{question}}

Read the prompt you added so you are familiar with it.

It consists of:

* A **system message**, which includes an objective, a definition of its capabilities,
  and some instructions.
* The **chat history**, ordered to show each user question input and each previous
  assistant answer output.

10. In the **Inputs** section for the Chat LLM tool, under the prompt, ensure the
    following variables are set:

    * **question (string):** `${inputs.question}`
    * **chat_history (string):** `${inputs.chat_history}`

11. Save the changes to the flow.

    > **Note:** In this exercise, we'll stick to a simple chat flow, but note that the
    > prompt flow editor includes many other tools that you could add to the flow,
    > enabling you to create complex logic to orchestrate conversations.

## Test the flow

Now that you've developed the flow, you can use the chat window to test it.

1. Ensure the compute session is running.

   If not, wait for it to start.

2. On the toolbar, select **Chat** to open the Chat pane, and wait for the chat to
   initialize.

3. Enter the query:

   ```text
   I have one day in London, what should I do?
   ```

   Review the output.

   The Chat pane should look similar to this:

   ![Screenshot](../../media/a6.png)

## Deploy the flow

When you're satisfied with the behavior of the flow you created, you can deploy the flow.

> **Note:** Deployment can take a long time, and can be impacted by capacity constraints
> in your subscription or tenant.

1. On the toolbar, select **Deploy** and deploy the flow with the following settings:

   **Basic settings:**

   * **Endpoint:** New
   * **Endpoint name:** Enter a unique name
   * **Deployment name:** Enter a unique name
   * **Virtual machine:** Standard_DS3_v2
   * **Instance count:** 1
   * **Inferencing data collection:** Disabled

   **Advanced settings:**

   * Use the default settings.

2. In Foundry portal, in the navigation pane, in the **My assets** section, select
   the **Models + endpoints** page.

   If the page opens for your `gpt-4o` model, use its back button to view all models
   and endpoints.

3. Initially, the page may show only your model deployments.

   It may take some time before the deployment is listed, and even longer before it's
   successfully created.

4. When the deployment has succeeded, select it.

   Then, view its **Test** page.

   > **Tip:** If the test page describes the endpoint as unhealthy, return to the
   > **Models + endpoints** page and wait a minute or so before refreshing the view
   > and selecting the endpoint again.

   ![Screenshot](../../media/a7.png)

5. Enter the prompt:

   ```text
   What is there to do in San Francisco?
   ```

   Review the response.

6. Enter the prompt:

   ```text
   Tell me something about the history of the city.
   ```

   Review the response.

   The test pane should look similar to this.

7. View the **Consume** page for the endpoint, and note that it contains connection
   information and sample code that you can use to build a client application for your
   endpoint.

   This enables you to integrate the prompt flow solution into an application as a
   generative AI application.

## Conclusion

In this exercise, you created and tested a prompt flow in Microsoft Foundry that uses a GPT model to manage a conversational chat experience. You configured the required resource authorization, deployed the model, created a chat flow with chat history and user input, tested the flow, and deployed it as an endpoint.

You also verified the deployed endpoint using sample travel-related prompts and reviewed the available connection information for integrating the flow into an application.