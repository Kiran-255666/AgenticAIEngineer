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

Before you start the lab exercises, you must create a development environment for you to work in.

1. Open a web browser and navigate to the **Power Platform admin center** https://admin.powerplatform.microsoft.com/manage/environments. If you are already signed in with your **@hackable.in** account, ensure you sign out first, then sign in with the new **@justlabs.online** account provided for this lab.
   
   ![Environment page's select new.](../../media/ami.png)
   
1. If prompted, choose the option to stay signed in.
1. Close any pop-up messages that are displayed.

### Task 1.2 - Create a new environment

1. In the sidebar, select **Manage**.
1. In the **Environments** page, select **+ New**.
   ![Environment page's select new.](../../media/ClickNew.png)
1. In the **New environment** panel, set **Type** to Trial and **Region** to the default region shown (a local region provides quicker data access).
   ![Environment page's Type and Region.](../../media/TypeRegion.png)
1. Enter your name in the **Name** field.
   ![Environment page's set Your Name.](../../media/YourName.png)
1. Expand **Change default settings**. Under **Add a Dataverse data store?**, select **Yes**.
   ![Environment page's select new.](../../media/ToggleYes.png)
   > [!NOTE]
   > Pay-as-you-go with Azure is unavailable for Trial environments — only Production and Sandbox environments support this setting.

1. Select **Next**. In the **Add Dataverse** panel, set the following:
   - **Language**: leave as it is if already English (United States), otherwise select English (United States) and move to the next field
   - **Currency**: leave as default
   - **Security group**: Click **+ Select** and in **Edit security group** find **open access** click **None** and Click **Done**
   ![Environment Done Button.](../../media/done.png)
   - **URL**: No changes are required.
   - **Enable Dynamics 365 apps?**: leave as it is (locked to No), move to the next field
   - **Deploy sample apps and data?**: No

   > [!NOTE]
   > Currency defaults based on your region (for example, INR for India). Enable Dynamics 365 apps is disabled for Trial environments — it's only available for Production or Sandbox environments.
   
   ![Environment Save Button.](../../media/Save.png)

1. Select **Save** and wait until the environment state is **Ready** (use **Refresh** to update the display).

   > [!NOTE]
   > Environment provisioning can take several minutes depending on tenant configuration.

   ![Environment created in the Power Platform Admin center.](../../media/environment-created.png)

### Task 1.3 - Access Copilot Studio

1. In a new browser tab, open **Copilot Studio** https://copilotstudio.microsoft.com/ and sign in if prompted.

   ![Copilot Studio interface.](../../media/olduserxp.png)

   <details>
   <summary>Does your interface look different? Click here</summary>
   
   ![Copilot Studio interface.](../../media/newuserxp.png)

   Select **...** (More options) at the bottom of the page. Under **Explore**, select **Open Classic Experience**. These labs use the **Classic Experience**.
   
   </details>

2. Look at the **upper-right corner** of the page. Just to the left of the **Settings** ⚙️ icon, you will see the **Environment Selector** showing your current environment.

   ![Environment.](../../media/u1.png)

3. Check the **Environment Selector**. If your *named environment* is already displayed, use it.

   <details>
   <summary>Can't see your named environment? Click here</summary>

   a. Select the **Environment Selector**.

   ![Environment Selector.](../../media/u1.png)

   b. The **Switch environment** menu will open.

   ![Environment Selector.](../../media/u2.png)

   c. Under **Supported environments**, select your **named environment**.

   ![Environment Selector.](../../media/u3.png)

   d. Your **named environment** should now be shown in the **Environment Selector**.

   ![Environment Selector.](../../media/u4.png)

   </details>

### Task 1.4 - Create a solution

1. In the left navigation pane, select the ellipses (**...**), then select **Solutions**.
1. Verify that **Default Solution** and **Common Data Services Default Solution** are listed.

   ![List of solutions in Maker portal.](../../media/solutions-list.png)

1. Select **+ New solution**.
1. Enter `Lab Exercises` in the **Display name** field. The **Name** field should automatically populate as **LabExercises**, with the space removed.
1. Select **+ New publisher** below the **Publisher** drop-down.
1. Enter `Fabrikam_unique_Suffix` for Display name, `fabrikam_unique_suffix` for Name, Leave the Description field empty and proceed to the next field, Prefix. Now fill `fab` for Prefix, then select **Save**.

   ![List of solutions in Maker portal.](../../media/fabone.png)
     
1. Confirm **Fabrikam_unique_suffix (fabrikam_unique_suffix)** is selected in the **Publisher** drop-down.
1. Leave **Version** as the default value.
1. Select the **Set as your preferred solution** checkbox.

   > [!NOTE]
   > Setting this as your preferred solution ensures new assets created during later labs are added to the Lab Exercises solution by default.

1. Select **Create**.

   ![New solution.](../../media/newsolutionone.png)

1. Close the **Solutions** browser tab, then refresh the **Copilot Studio** page.
![New solution.](../../media/labex1.png)

You now have a Power Platform environment and solution to work in.

## Summary

In this exercise, you created a Power Platform trial environment with Dataverse, accessed Microsoft Copilot Studio, selected your environment, and created a **Lab Exercises** solution with a custom publisher. This environment and solution will be used throughout the remaining labs.
