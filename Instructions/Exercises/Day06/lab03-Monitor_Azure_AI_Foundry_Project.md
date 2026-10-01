---
lab:
    title: 'Monitor Your Azure AI Foundry Project'
    description: 'Use Azure Monitor metrics, alerts, diagnostic settings, and logs to monitor an Azure AI Foundry project.'
    level: 300
    duration: 45
    islab: true
    status: 'released'
---

# Monitor Your Azure AI Foundry Project

In this exercise, you'll monitor your **Microsoft Foundry project `hakunamatata11`** from the Azure portal. You'll explore **Azure Monitor Alerts, Metrics, Diagnostic settings, and Logs**, create a Metrics chart with Azure OpenAI metrics, and review signals such as request count, data usage, latency, and availability.

This exercise should take approximately **45** minutes to complete.

## Prerequisites

- Azure portal access with the provided credentials.
- Access to the **hakunamatata11** Microsoft Foundry project.
- Sufficient permission to view Monitoring and Metrics for the resource.
- Recent activity on the project is helpful so that metrics display meaningful values.

## Step-by-Step Instructions

### Step 1: Sign in to the Azure Portal

1. Open Microsoft Edge.
2. Go to the Azure portal at https://portal.azure.com/.
3. If you haven't signed in, sign in using the credentials provided for the lab.
4. Wait until the Azure portal home page loads.


### Step 2: Open Microsoft Foundry

1. In the Azure portal search bar, type **Foundry**.
2. From the search results, select **Microsoft Foundry**.
3. In the side panel, select **All Resources**.
4. From the resource list, locate the Foundry resource named **`hakunamatata11`**.
5. Select **`hakunamatata11`** to open the resource.
6. Confirm that the **`hakunamatata11`** project overview page is displayed.

### Step 3: Expand the Monitoring Section

1. From the left menu, find **Monitoring** section.
2. Expand Monitoring to view the available monitoring options.
3. Review the available options before opening Metrics.

### Step 4: Understand the Monitoring Options

The Monitoring section contains several options. Explain the purpose of each option to learners before they start configuring metrics.

<div align="center">

<table align="center">
<tr>
<th>Monitoring Option</th>
<th>Purpose</th>
<th>How It Helps</th>
</tr>
<tr>
<td><b>Alerts</b></td>
<td>Used to notify administrators when a configured metric or log condition is met.</td>
<td>Helps make monitoring proactive instead of manually checking charts.</td>
</tr>
<tr>
<td><b>Metrics</b></td>
<td>Used to view numeric time-series data for the resource, such as request count, latency, and availability.</td>
<td>This is the main area used in the lab to build a monitoring chart.</td>
</tr>
<tr>
<td><b>Diagnostic settings</b></td>
<td>Used to route platform logs and metrics to destinations such as Log Analytics, Storage Account, or Event Hub.</td>
<td>Learners understand how monitoring data can be retained or sent for advanced analysis.</td>
</tr>
<tr>
<td><b>Logs</b></td>
<td>Used to query detailed log data, usually with KQL, when diagnostic data is available.</td>
<td>Learners understand where to investigate detailed events and support troubleshooting.</td>
</tr>
</table>

</div>

### **Step 5: Open Metrics**

1. Under **Monitoring**, select **Metrics**.

2. Confirm that the **Scope** is set to **`hakunamatata11`**.

3. Keep the **Time range** as the default **Local Time: Last 24 hours**.

![Screenshot](../../media/abcd21.png)

4. Click **Add metric** to start adding metrics to the chart.

![Screenshot](../../media/abcd2.png)

*Figure 2: Metrics Explorer area where multiple metrics are added to the chart.*

### **Step 6: Add Metrics to the Chart**

> **Important:** Add at least five metrics. Each time you click **Add metric**, keep the following settings unchanged:
>
> * **Scope:** `hakunamatata11`
> * **Metric Namespace:** **Cognitive Services / Azure OpenAI metrics**
>
> Only change the **Metric** and **Aggregation** as specified for each metric below.

#### **Metric 1: Azure OpenAI Requests**

1. Click **Add metric**.
2. Keep the default **Scope** and **Metric Namespace**.
3. In the **Metric** dropdown, select **Azure OpenAI Requests**.
4. Set **Aggregation** to **Sum**.
5. Confirm that the metric appears as a chip above the chart by clicking Finish editing metric

![Screenshot](../../media/abcd11.png)

> **Why this metric is useful:** Shows the total number of Azure OpenAI requests during the selected time range.

#### **Metric 2: Data In**

1. Click **Add metric**.
2. Keep the default **Scope** and **Metric Namespace**.
3. In the **Metric** dropdown, select **Data In**.
4. Set **Aggregation** to **Sum**.
5. Confirm that the metric appears as a chip above the chart.

> **Why this metric is useful:** Shows how much input data is sent to the service.

#### **Metric 3: Time Between Token**

1. Click **Add metric**.
2. Keep the default **Scope** and **Metric Namespace**.
3. In the **Metric** dropdown, select **Time Between Token**.
4. Set **Aggregation** to **Average**.
5. Confirm that the metric appears as a chip above the chart.

> **Why this metric is useful:** Shows the average delay between streamed tokens and helps review response streaming performance.

#### **Metric 4: Time to First Byte**

1. Click **Add metric**.
2. Keep the default **Scope** and **Metric Namespace**.
3. In the **Metric** dropdown, select **Normalized Time to First Byte**.
4. Set **Aggregation** to **Average**.
5. Confirm that the metric appears as a chip above the chart.

> **Why this metric is useful:** Shows how quickly the service starts returning the response after a request is submitted.

#### **Metric 5: Azure OpenAI Availability Rate**

1. Click **Add metric**.
2. Keep the default **Scope** and **Metric Namespace**.
3. In the **Metric** dropdown, select **Azure OpenAI Availability Rate**.
4. Set **Aggregation** to **Average**.
5. Confirm that the metric appears as a chip above the chart.

> **Why this metric is useful:** Shows service availability during the selected time range.

![Screenshot](../../media/abcd3.png)

### Optional Metrics to Explore

- Time to Last Byte
- Time to Response
- Processed Fine-Tuned Training Hours
- Generated Completion Tokens
- Generated Prompt Tokens
- Total Tokens

### Review the Metrics Chart

1. Review the chart after all selected metrics are added.
2. Check whether the lines or values show request activity, data usage, latency, or availability patterns.
3. Use the legend under the chart to identify each metric.
4. Use the time range selector if you want to review another time window.
5. Optionally, use **Save to dashboard** if the chart should be reused later.

## Conclusion

In this lab, we monitored the **`hakunamatata11`** Microsoft Foundry project from the Azure portal. We explored the Monitoring section and understood how Alerts, Metrics, Diagnostic settings, and Logs support operational visibility.

> **Key takeaway:** Monitoring is important because it gives visibility into how an AI resource is performing and being used. Metrics provide a quick operational view, while logs and diagnostic settings support deeper troubleshooting and long-term analysis.
