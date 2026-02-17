# Meta XR Deployer: User Guide

This guide provides step-by-step instructions on how to use the Meta XR Deployer tool to build and deploy your XR projects.

## 1. Overview

The Meta XR Deployer is a graphical user interface (GUI) tool designed to streamline the process of building and deploying Meta XR projects. It automates several common tasks, including copying source files, managing ADB (Android Debug Bridge) connections, setting up environment paths, and executing build and deployment scripts.

## 2. Prerequisites

Before using the Meta XR Deployer, ensure you have the following:

*   **Godot Engine 4.x**: The `godot-4.5.exe` executable should be present in the same directory as the deployer tool.
*   **Android SDK**: The Android SDK build tools and platform tools should be located in the `android-sdk` directory relative to the deployer tool.
*   **Java Development Kit (JDK)**: A JDK installation should be present in the `android-sdk/jdk` directory relative to the deployer tool.
*   **Source Projects**: Your XR projects should be located in the `projects` directory relative to the deployer tool.
*   **Templates**: Export templates should be available in the `templates` directory relative to the deployer tool.

## 3. Using the Meta XR Deployer GUI

Follow these steps to use the Meta XR Deployer:

### Step 0: Copy Source Files

This step uses `robocopy` to copy necessary source files to the current working directory. By default, it copies from `H:\godot-b-a-v0`. You can specify a custom source path if needed.

1.  **Enable custom robocopy path (Optional)**:
    *   Check the box next to "Enable custom robocopy path" if you want to specify a different source directory for `robocopy`.
    *   ![Placeholder for 'Enable custom robocopy path' checkbox](images/enable_custom_robocopy.png)

2.  **Enter Custom Robocopy Path (Optional)**:
    *   If the custom path is enabled, an input field will appear. Enter the desired source path here.
    *   ![Placeholder for 'Custom Robocopy Path' input field](images/custom_robocopy_path_input.png)

3.  **Run Robocopy**:
    *   Click the "Run Robocopy" button to initiate the file copying process.
    *   The status log at the bottom will display the progress.
    *   ![Placeholder for 'Run Robocopy' button](images/run_robocopy_button.png)

### Step 1: Restart ADB Server

This step stops and restarts the ADB server and lists devices to ensure a fresh connection and prompt for device authorization.

1.  **Restart ADB**:
    *   Click the "Restart ADB" button.
    *   Monitor the status log for ADB server messages and check your device for any authorization prompts.
    *   ![Placeholder for 'Restart ADB' button](images/restart_adb_button.png)

### Step 2: Select Source Folder

Choose the XR project you wish to build and deploy from the dropdown list.

1.  **Select Project**:
    *   Click on the dropdown menu labeled "Select Source Folder" and choose your project.
    *   ![Placeholder for 'Select Source Folder' dropdown](images/select_source_folder_dropdown.png)

### Step 3: Generated Paths

This section displays the automatically generated paths for the Android SDK and Java SDK, which are crucial for the build process. You can copy these paths to your clipboard if needed.

1.  **Copy Paths (Optional)**:
    *   Click "Copy Path SDK" to copy the Android SDK path.
    *   Click "Copy Path JDK" to copy the Java SDK path.
    *   ![Placeholder for 'Generated Paths' section](images/generated_paths.png)

### Step 4: Execute Script

This is the final step to build and deploy your selected XR project.

1.  **Run Deployment**:
    *   Click the "RUN" button to execute the `build_and_deploy.bat` script for the selected project.
    *   The status log will show the build and deployment progress.
    *   ![Placeholder for 'RUN' button](images/run_button.png)

## 4. Status Log

The text area at the bottom of the GUI displays real-time status updates and output from the executed commands. Monitor this area for progress, errors, and important messages.

![Placeholder for 'Status Log' area](images/status_log.png)
