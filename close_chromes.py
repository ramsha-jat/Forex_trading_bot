import subprocess

def close_chrome():
    """
    Close all instances of Google Chrome.

    This function performs the following steps:
    1. Uses the subprocess module to execute the command to close Chrome.
    2. Prints a message indicating that Chrome has been closed.
    """
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=True)
        print("All instances of Google Chrome have been closed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to close Chrome: {e}")

# Call the function to close Chrome
close_chrome()