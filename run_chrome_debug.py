import subprocess

def run_chrome_debugging():
    """
    Run Google Chrome with remote debugging enabled.

    This function performs the following steps:
    1. Uses the subprocess module to execute the command to run Chrome with the specified debugging port.
    2. Prints a message indicating that Chrome has been started in debugging mode.
    """
    chrome_path = r"C:\Users\lenovo\AppData\Local\ms-playwright\chromium-1129\chrome-win\chrome.exe"
    debugging_port = 9222
    try:
        subprocess.Popen([chrome_path, f"--remote-debugging-port={debugging_port}"])
        print(f"Google Chrome has been started with remote debugging on port {debugging_port}.")
    except Exception as e:
        print(f"Failed to start Chrome with remote debugging: {e}")

# Call the function to run Chrome with debugging
run_chrome_debugging()