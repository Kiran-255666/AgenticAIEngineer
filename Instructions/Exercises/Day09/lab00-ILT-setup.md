---
lab:
  title: ILT Setup
  module: Introduction
  description: In this exercise, you will access the Microsoft Copilot Studio portal and create an environment and solution to use throughout the remaining labs.
  duration: 25 minutes
  level: 200
  islab: true
  primarytopics:
    - Microsoft Copilot
    - Microsoft Copilot Studio
---

## Exercise 1 Create a Power Platform environment

### Task 1.1 - Power Platform Admin Center

Before you start the lab exercises, you must create a development environment to work in.

1. Open a web browser and copy the **Power Platform admin center URL** given below:

   ```text
   https://admin.powerplatform.microsoft.com/manage/environments
   ```

2. Paste the URL into the browser's address bar and press **Enter**.

3. Sign in using the **credentials provided for this lab**.

4. If prompted, select the option to **Stay signed in**. Close any pop-up messages that appear.

### Task 1.2 - Create a new environment

1. In the sidebar, select **Manage**.
2. On the **Environments** page, select **+ New**.

   ![Environment page's select new.](../../media/ClickNew-v11.png)

3. In the **New environment** panel, set **Type** to Trial and **Region** to the default region shown (a local region provides quicker data access).

   ![Environment page's Type and Region.](../../media/TypeRegion.png)
4. Enter your preferred name in the **Name** field.
   ![Environment page's set Your Name.](../../media/YourName1.png)
5. Expand **Change default settings**. Under **Add a Dataverse data store?**, select **Yes**.

   ![Environment page's select new.](../../media/ToggleYes.png)

> [!NOTE]
> **Pay-as-you-go with Azure is unavailable for Trial environments. This setting is supported only for Production and Sandbox environments**.

6. Select **Next**. 

7. In the **Add Dataverse** panel, set the following:
   - **Language**: Leave it as **English (United States)** if it is already selected. Otherwise, select **English (United States)** and move to the next field.
   - **Currency**: leave as default
   - **Security group**: Click **+ Select** and in **Edit security group** find **open access** click **None** and Click **Done**
   ![Environment Done Button.](../../media/done.png)
   - **URL**: No changes are required.
   - **Enable Dynamics 365 apps?**: leave as it is (locked to **No**), move to the next field
   - **Deploy sample apps and data?**: No

> [!NOTE]
> **Currency defaults based on your region (for example, INR for India). Enable Dynamics 365 apps is disabled for Trial environments and it's only available for Production or Sandbox environments**.  

   ![Environment Save Button.](../../media/Save.png)

7. Select **Save** and wait for the environment state to change from **Preparing** to **Ready**. After some time, use **Refresh** to update the status.

> [!NOTE]
> Environment provisioning can take several minutes, depending on your tenant configuration. The environment state will change from **Preparing** to **Ready** once provisioning is complete. You can also verify that the Dataverse status changes from **No** to **Yes**.

   ![Environment created in the Power Platform Admin center.](../../media/environment-created1.png)

### Task 1.3 - Access Copilot Studio

1. Open a new browser tab. Copy the **Copilot Studio URL**:

   ```text
   https://copilotstudio.microsoft.com/
   ```

2. Paste the URL into the browser's address bar and press **Enter**. If prompted, sign in using the **credentials provided for this lab**.

3. You will be redirected to the **new Copilot Studio UI**, which currently has fewer features than the **Classic Experience UI**. For consistency across all labs, we will use the **Classic Experience UI** throughout.

   ![Copilot Studio interface.](../../media/newuserxp1-v1.png)

4. Select **...** (More options) at the bottom of the page. Under **Explore**, select **Open Classic Experience**, then select **Skip feedback** and if any setup prompts appear, select Get started and follow the prompts until they are completed. .

   ![Copilot Studio interface.](../../media/newuserxp2-v1.png)

5. Now you are in the **Open Classic Experience**. In the **upper-right corner** of the page, just to the left of the **Settings** ⚙️ icon, locate the **Environment Selector** showing the current environment.

6. Select the **Environment Selector**.

   ![Environment Selector.](../../media/u111.png)

7. The **Select environment** menu will open.

   ![Environment Selector.](../../media/u22.png)

8. Under **Supported environments**, select your **named environment**.

   ![Environment Selector.](../../media/u33.png)

9. Your **named environment** should now be displayed in the **Environment Selector**.

   ![Environment Selector.](../../media/u44.png)

10. You are now in the correct **environment** and the **Classic Experience** UI is ready for the lab.

> [!TIP]
>
> **Remember these steps, as you will use them throughout the labs when you are redirected to the new UI or a different environment.**

### Task 1.4 - Create a solution

1. In the left navigation pane, select the ellipses (**...**), then select **Solutions**.
2. Verify that **Default Solution** and **Common Data Services Default Solution** are listed.

   ![List of solutions in Maker portal.](../../media/solutions-list.png)

3. Select **+ New solution**.
4. Enter **`Lab Exercises`** in the **Display name** field. The **Name** field should automatically populate as **LabExercises**, with the space removed.
5. Select **+ New publisher** below the **Publisher** drop-down.
6. Enter **`Fabrikam_unique_Suffix`** for Display name, `fabrikam_unique_suffix` for Name, Leave the Description field empty and proceed to the next field, Prefix. Now fill `fab` for Prefix, then select **Save**.

   ![List of solutions in Maker portal.](../../media/fabone.png)
     
7. Confirm **Fabrikam_unique_suffix (fabrikam_unique_suffix)** is selected in the **Publisher** drop-down.
8. Leave **Version** as the default value.
9. Select the **Set as your preferred solution** checkbox.

> [!NOTE]
> Setting this as your preferred solution ensures new assets created during later labs are added to the Lab Exercises solution by default.

10. Select **Create**.

   ![New solution.](../../media/newsolutionone.png)

11. Close the **Solutions** browser tab by selecting the **←** icon in the left pane.

![New solution.](../../media/labex11.png)

12. You now have a Power Platform environment and solution to work in.

![New solution.](../../media/labex1-v1.png)

## Summary

In this exercise, you created a Power Platform trial environment with Dataverse, accessed Microsoft Copilot Studio, selected your environment, and created a **Lab Exercises** solution with a custom publisher. This environment and solution will be used throughout the remaining labs.
