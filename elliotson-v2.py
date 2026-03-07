import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

SOURCE_CODE_LOCATION = "H:\\godot-b-a-v0"

CUSTOM_OPTION_ENABLED = False
CUSTOM_OPTION_VALUE = ""  # Will store user input from the text field


# -----------------------------
# Path resolution utilities
# -----------------------------

def get_exe_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def unix_like_path(path):
    path = path.strip('"')
    return path.replace("\\", "/")


def unix_like_path_single(path):
    path = path.strip('"')
    return path.replace("\\", "/")


# -----------------------------
# Command execution
# -----------------------------

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


def run_command_stream(command, log_callback):
    """
    Runs a command in a subprocess and streams stdout/stderr line by line to log_callback.
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        for line in iter(process.stdout.readline, ''):
            if line:
                log_callback(line.rstrip())

        process.stdout.close()
        process.wait()
        log_callback(f"Process finished with exit code {process.returncode}")
    except Exception as e:
        log_callback(f"Error: {e}")


# -----------------------------
# Application
# -----------------------------

class ScriptRunnerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Script Runner Portable")
        self.resizable(True, True)

        self.exe_dir = get_exe_dir()
        self.sources_dir = os.path.join(self.exe_dir, "projects")
        self.scripts_dir = self.exe_dir
        self.gradle_dir = unix_like_path(os.path.join(self.exe_dir, "build-tools\gradle-7.4-all.zip"))

        self.selected_folder = tk.StringVar()

        self.custom_option = tk.BooleanVar(value=False)
        self.custom_value = tk.StringVar(value="")

        self.path_a = unix_like_path(os.path.join(self.exe_dir, "build-tools/android-sdk"))
        self.path_b = unix_like_path(os.path.join(self.exe_dir, "android-sdk\\jdk"))

        self._build_ui()
        self.custom_entry.bind("<KeyRelease>", self.on_custom_value_change)
        self._populate_sources()

        self.update_gradle_properties()
        self.log("Gradle paths set")

    # -------------------------
    # UI
    # -------------------------

    def _build_ui(self):
        padding = {"padx": 10, "pady": 5}

        ttk.Checkbutton(self, text="Enable custom robocopy path", variable=self.custom_option,
                        command=self.on_custom_toggle).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.custom_entry = ttk.Entry(self, textvariable=self.custom_value, width=20)
        self.custom_entry.grid(row=0, column=1, columnspan=2, sticky="w", padx=30, pady=2)
        self.custom_entry.grid_remove()  # Hide initially

        # Robocopy section
        ttk.Label(self, text="0) Copy Source Files").grid(row=1, column=0, sticky="w", **padding)
        ttk.Button(self, text="Run Robocopy", command=self.run_robocopy).grid(row=1, column=1, **padding)
   
        # ADB Restart section
        ttk.Label(self, text="1) Restart ADB Server").grid(row=2, column=0, sticky="w", **padding)
        ttk.Button(self, text="Restart ADB", command=self.restart_adb).grid(row=2, column=1, **padding)

        # Source dropdown
        ttk.Label(self, text="2) Select Source Folder").grid(row=3, column=0, sticky="w", **padding)
        self.source_combo = ttk.Combobox(self, textvariable=self.selected_folder, state="readonly")
        self.source_combo.grid(row=3, column=1, **padding)

        # Paths
        ttk.Label(self, text="3) Generated Paths").grid(row=4, column=0, sticky="w", **padding)

        ttk.Label(self, text="Android SDK:").grid(row=5, column=0, sticky="e", **padding)
        self.path_a_entry = ttk.Entry(self, width=50)
        self.path_a_entry.insert(0, self.path_a)
        self.path_a_entry.config(state="readonly")
        self.path_a_entry.grid(row=5, column=1, **padding)
        ttk.Button(self, text="Copy Path SDK", command=lambda: self.copy_to_clipboard(self.path_a)).grid(row=5, column=2, **padding)

        ttk.Label(self, text="Java SDK:").grid(row=6, column=0, sticky="e", **padding)
        self.path_b_entry = ttk.Entry(self, width=50)
        self.path_b_entry.insert(0, self.path_b)
        self.path_b_entry.config(state="readonly")
        self.path_b_entry.grid(row=6, column=1, **padding)
        ttk.Button(self, text="Copy Path JDK", command=lambda: self.copy_to_clipboard(self.path_b)).grid(row=6, column=2, **padding)

        # Run script
        ttk.Label(self, text="4) Execute Script").grid(row=7, column=0, sticky="w", **padding)
        ttk.Button(self, text="RUN", command=self.run_script).grid(row=7, column=1, **padding)

        # Status
        ttk.Label(self, text="Status").grid(row=8, column=0, sticky="w", **padding)
        self.status = tk.Text(self, height=13, width=80, state="disabled")
        self.status.grid(row=9, column=0, columnspan=3, **padding)

    # -------------------------
    # Logic
    # -------------------------
    
    def update_gradle_properties(self):
	
        def write_multiline_to_file(content: str, filepath: str) -> None:
                with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
        gradle_props = f"""
        distributionBase=GRADLE_USER_HOME
        distributionPath=wrapper/dists
        distributionUrl= file\:///{self.gradle_dir}
        zipStoreBase=GRADLE_USER_HOME
        zipStorePath=wrapper/dists
        """
        path = os.path.join(unix_like_path(self.exe_dir), "addons/openxr/gradle/wrapper/gradle-wrapper.properties")
        write_multiline_to_file(gradle_props, path)


    def restart_adb(self):
        """
        Stops adb server, starts it again, and lists devices
        to trigger authorization prompt.
        """
        def adb_sequence():
            commands = [
                r".\android-sdk\platform-tools\adb.exe kill-server",
                r".\android-sdk\platform-tools\adb.exe start-server",
                r".\android-sdk\platform-tools\adb.exe devices"
            ]

            for cmd in commands:
                self.log(f"Running: {cmd}")
                run_command_stream(cmd, self.log)

            self.log("ADB restart sequence complete. Check device for authorization prompt.")

        threading.Thread(target=adb_sequence, daemon=True).start()

    def log(self, text):
        self.status.config(state="normal")
        self.status.insert("end", text + "\n")
        self.status.see("end")
        self.status.config(state="disabled")

    def _populate_sources(self):
        if not os.path.isdir(self.sources_dir):
            self.log("ERROR: sources directory missing")
            self.source_combo["values"] = []
            return

        folders = [
            name for name in os.listdir(self.sources_dir)
            if os.path.isdir(os.path.join(self.sources_dir, name))
        ]

        self.source_combo["values"] = folders
        if folders:
            self.source_combo.current(0)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.log(f"Copied to clipboard: {text}")

    def run_robocopy(self):
        source = SOURCE_CODE_LOCATION

        if CUSTOM_OPTION_ENABLED and CUSTOM_OPTION_VALUE:
            source = CUSTOM_OPTION_VALUE

        destination = os.getcwd()
        command = f'robocopy "{source}" "{destination}" /E'
        self.log(f"Running: {command}")

        # Run in background thread and stream output
        threading.Thread(target=run_command_stream, args=(command, self.log), daemon=True).start()

    def run_script(self):
        folder = self.selected_folder.get()
        if not folder:
            messagebox.showerror("Error", "No source folder selected")
            return

        script_path = os.path.join(self.scripts_dir, "build_and_deploy.bat")
        if not os.path.isfile(script_path):
            messagebox.showerror("Error", "Script not found")
            return

        command = f'"{script_path}" {folder}'
        self.log(f"Running: {command}")

        # Run in background thread and stream output
        threading.Thread(target=run_command_stream, args=(command, self.log), daemon=True).start()

    def on_custom_toggle(self):
        global CUSTOM_OPTION_ENABLED, CUSTOM_OPTION_VALUE
        CUSTOM_OPTION_ENABLED = self.custom_option.get()

        if CUSTOM_OPTION_ENABLED:
            self.custom_entry.grid()  # Show text field
        else:
            self.custom_entry.grid_remove()  # Hide text field

        CUSTOM_OPTION_VALUE = self.custom_value.get()
        self.log(f"Custom option enabled: {CUSTOM_OPTION_ENABLED}")

    def on_custom_value_change(self, event):
        global CUSTOM_OPTION_VALUE
        CUSTOM_OPTION_VALUE = self.custom_value.get()


# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    app = ScriptRunnerApp()
    app.mainloop()