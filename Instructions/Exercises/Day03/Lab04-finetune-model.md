---
lab:
  title: Fine-tune a language model
  description: Learn how to use your own training data to fine-tune a model and customize its behavior.
  level: 300
  duration: 90
  islab: true
  status: 'released'
---

# Fine-tune a language model

Prompt engineering tells a language model how to behave in one conversation. Fine-tuning uses example conversations to make a particular style or behavior more consistent.

In this exercise, you explore a travel-planning chat application. First, you test the prepared **gpt-5.4-mini** model in the playground. Next, you create a supervised fine-tuning job using **gpt-4.1** and your training data. Finally, you test the fine-tuned model and compare its responses with the prepared base model.

The goal is to create a friendly travel assistant that suggests destinations and activities in a consistent tone, without recommending hotels, flights, rental cars, or restaurants.

This exercise takes approximately **90 minutes**.

> **Note**: Fine-tuning depends on cloud capacity and can take 60 minutes or longer. Some portal features are in preview or active development, so you may see warnings, errors, or unexpected behavior. Continue with the playground-testing tasks while the job runs.

## Prerequisites

Before you start, ensure that you have:

- An active [Azure subscription](https://azure.microsoft.com/free/)
- A web browser
- A Microsoft Foundry project prepared by your trainer or lab environment
- The **gpt-5.4-mini** model available for the initial playground test
- The **gpt-4.1** model available for the supervised fine-tuning job
- Permission to create fine-tuning jobs and upload datasets

> The project and required models are already prepared for this exercise. Do not create a new project or add another base model.

# Verify the existing project

Microsoft Foundry projects organize the models, resources, data, and other assets used to build an AI solution.

1. Open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in with your Azure credentials. Close any tips or quick-start panes that appear.
1. On the home page, select the project prepared by your trainer or lab environment.
1. Open the model playground and confirm that the prepared **gpt-5.4-mini** model is available.

    > **Tip**: If you cannot find the project or gpt-5.4-mini, check with your trainer before continuing.

# Download the training data

1. Open the [training dataset](https://github.com/Kiran-255666/AgenticAIEngineer/blob/main/labfiles/Day03/lab04-fine-tuning/credit_risk_management.jsonl) in a browser.
1. Download the file and save it locally as `credit_risk_management.jsonl`.

    > **Important**: Your browser may save the file with a `.txt` extension. If it does, rename the file so that its name ends in `.jsonl`.

# Start a fine-tuning job

Start the job now. It may take a while, so you can test gpt-5.4-mini in the playground while the fine-tuning job runs.

1. In the Foundry portal, select **Fine-tune** in the left navigation.

    ![Fine-tuning page with an arrow pointing to Start fine-tuning.](../../media/fine-tune-001.png)

1. Select **Start fine-tuning**.
1. In **Basic details**, configure the job as follows:

    - **Customization method**: Supervised
    - **Model**: gpt-4.1
    - **Training type**: Data Zone

    ![Basic details page showing Supervised, gpt-4.1, and Data Zone selected.](../../media/fine-tune-002.png)

1. Select **Next**.
1. In **Datasets**, under **Training data source**, select **Upload or drag and drop**. Upload `travel-finetune-hotel.jsonl`.
1. Confirm that the upload finishes and that the Dataset preview displays the file content and JSONL rows.
1. Leave **Validation data source (optional)** empty.

    ![Datasets page showing travel-finetune-hotel.jsonl uploaded and previewed.](../../media/fine-tune-003.png)

1. Select **Next** to open **Optional settings**.
1. Configure or confirm these settings:

    - **Display name**: Keep the generated name, or enter `ft-travel`
    - **Seed**: Keep the default value, **Random**
    - **Automatically deploy model after job completion**: Turn this on
    - **Hyperparameter tuning**: Keep **Default** selected for batch size, number of epochs, and learning-rate multiplier

    ![Optional settings page showing a generated display name, Random seed, automatic deployment control, and default hyperparameters.](../../media/fine-tune-004.png)

1. Select **Submit** to start the job.

> **Note**: Fine-tuning and automatic deployment can take 60 minutes or longer. To check progress, open the fine-tuning job and select the **Monitor tab**. The steps to reach the Monitor tab are shown in the following screenshots.

![Snippet](../../media/w8.png)

# Test gpt-5.4-mini in the playground

While the fine-tuning job runs, test the prepared **gpt-5.4-mini** model and note how prompt instructions affect its behavior.

1. Open the model playground for **gpt-5.4-mini**.

2. In the chat pane, enter:

   ```text
   What can you do?
   ```

   The response may be generic. The credit risk application needs more specific behavior focused on business credit assessment.

3. In the **Instructions** field, enter:

   ```text
   You are an AI assistant that helps assess the creditworthiness of business clients.
   ```

4. Ask the same question again:

   ```text
   What can you do?
   ```

   The assistant may provide a general response. The credit risk application requires more specific behavior and should focus on document verification, compliance checks, financial analysis, external credit information, and industry risk.

5. Replace the instructions with the following prompt:

   ```text
   You are an AI credit risk management assistant that helps assess the creditworthiness of business clients. Your objective is to evaluate company documents, compliance status, financial ratios, external credit information, and industry risk using the provided credit risk assessment rules.
   Do not invent missing financial or compliance information.
   Clearly identify missing documents or data and explain how they affect the assessment.
   ```

6. Test the model with these questions. Note the answers, tone, and writing style:

   ```text
   What documents are required to start a credit risk assessment?
   ```

   ```text
   The client uploaded only the GST Certificate. Can we pass the document verification step?
   ```

   ```text
   A company has a Current Ratio of 1.56, Debt-to-Equity of 1.86, and Net Profit Margin of 5.56%. How many points does it receive for these three financial metrics?
   ```

   ```text
   How does industry risk affect the credit score?
   ```

   ```text
   What happens if a sanctions or compliance match is confirmed?
   ```

# Review the training data

The training file contains examples of the behavior and writing style that you want the fine-tuned model to learn.

1. Open the downloaded `credit_risk_management.jsonl` file in a text editor.

2. Review the JSONL entries. The first entry should look similar to the following example, formatted for readability:

```json
{"messages": [
  {
    "role": "system",
    "content": "You are an AI credit risk management assistant that helps assess the creditworthiness of business clients. Your objective is to evaluate company documents, compliance status, financial ratios, external credit information, and industry risk using the provided credit risk assessment rules. Do not invent missing financial or compliance information. Clearly identify missing documents or data and explain how they affect the assessment."
  },
  {
    "role": "user",
    "content": "What documents are required to start a credit risk assessment?"
  },
  {
    "role": "assistant",
    "content": "The assessment requires both the Company Registration Certificate and GST Certificate. The company name must match exactly across the client information and both certificates. The assessment should also verify the company's legal status, sanctions or adverse compliance records, financial statements for the last two financial years, and the latest external credit score or rating."
  }
]}
```

Each entry includes system instructions, a credit-risk-related user question, and an assistant response that you want the model to learn. These examples help the fine-tuned model produce more consistent credit risk assessments and follow the defined scoring rules.

# Test the fine-tuned model

1. In the left navigation, select **Fine-tune** and check the status of the job you started earlier.

2. Select the job to view its details. Open the **Logs** tab if you need to review completed tasks or errors.

![Snippet](../../media/logs.png)

1. When fine-tuning finishes, verify that the fine-tuned model is available in **Deployments**.

   > **Tip**: If automatic deployment did not finish successfully, open the completed fine-tuning job and make the fine-tuned model available from its details page.

2. Open the fine-tuned model in the model playground.

3. Set the **Instructions** field to the same credit risk management prompt used earlier:

   ```text
   You are an AI credit risk management assistant that helps assess the creditworthiness of business clients. Your objective is to evaluate company documents, compliance status, financial ratios, external credit information, and industry risk using the provided credit risk assessment rules.
   Do not invent missing financial or compliance information.
   Clearly identify missing documents or data and explain how they affect the assessment.
   ```

4. Ask the same credit risk questions again:

   ```text
   What documents are required to start a credit risk assessment?
   ```

   ```text
   The client uploaded only the GST Certificate. Can we pass the document verification step?
   ```

   ```text
   A company has a Current Ratio of 1.56, Debt-to-Equity of 1.86, and Net Profit Margin of 5.56%. How many points does it receive for these three financial metrics?
   ```

   ```text
   How does industry risk affect the credit score?
   ```

   ```text
   What happens if a sanctions or compliance match is confirmed?
   ```

5. Compare the fine-tuned model's responses with the prepared **gpt-5.4-mini** base model. Note differences in tone, consistency, adherence to the credit risk instructions, and use of the defined assessment rules.

## Summary

You tested the prepared **gpt-5.4-mini** model using prompt instructions, reviewed the supervised fine-tuning dataset in `credit_risk_management.jsonl`, and tested the resulting fine-tuned model. Fine-tuning is useful when a particular behavior, response style, or domain-specific approach needs to remain consistent across many credit risk assessment conversations.
