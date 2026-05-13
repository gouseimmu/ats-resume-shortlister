import os
import sys
import time
import socket
import subprocess
import webbrowser

PORT = 8501
LOCK_FILE = "browser_opened.lock"

def is_running():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", PORT)) == 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(BASE_DIR, "app.py")

# Start Streamlit only once
if not is_running():

    streamlit_exe = os.path.join(
        sys.prefix,
        "Scripts",
        "streamlit.exe"
    )

    subprocess.Popen(
        [
            streamlit_exe,
            "run",
            APP_PATH,
            "--server.headless=true",
            "--server.port=8501"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for startup
    for _ in range(30):
        if is_running():
            break
        time.sleep(1)

# Open browser only ONCE
lock_path = os.path.join(BASE_DIR, LOCK_FILE)

if not os.path.exists(lock_path):

    webbrowser.open("http://localhost:8501")

    with open(lock_path, "w") as f:
        f.write("opened")

# Keep alive
while True:
    time.sleep(1)