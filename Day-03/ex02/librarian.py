import sys
import subprocess
import os

if __name__ == "__main__":
    if os.getenv("VIRTUAL_ENV") is None:
        raise Exception("invalid venv")
    subprocess.call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "PyTest"])
    subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=open("requirements.txt", "w"))
    subprocess.run(["cat", "requirements.txt"])