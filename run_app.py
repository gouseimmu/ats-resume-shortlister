import os
import sys
import time
import socket
import subprocess
import webbrowser

PORT = 8501


# ==========================================
# CHECK IF STREAMLIT IS RUNNING
# ==========================================

def is_running():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        return sock.connect_ex(("127.0.0.1", PORT)) == 0


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_PATH = os.path.join(BASE_DIR, "app.py")


# ==========================================
# START STREAMLIT
# ==========================================

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
            "--server.port=8501",
            "--browser.gatherUsageStats=false"
        ],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for server startup
    for _ in range(30):

        if is_running():
            break

        time.sleep(1)


# ==========================================
# OPEN BROWSER
# ==========================================

webbrowser.open("http://localhost:8501")


# ==========================================
# KEEP APP ACTIVE
# ==========================================

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    pass