import subprocess
import time
import sys
import os

def main():
    print("------------------------------------------------")
    print("   Starting AI Fake News Platform Prototype")
    print("------------------------------------------------")
    print(f"Working Directory: {os.getcwd()}")

    # 1. Start Backend (FastAPI)
    print(">> Launching Backend (Uvicorn)...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.getcwd(),
        env=os.environ.copy()
    )

    # Wait briefly for backend to warm up
    time.sleep(3)

    # 2. Start Frontend (Streamlit)
    print(">> Launching Frontend (Streamlit)...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/Home.py", "--server.port", "8501"],
        cwd=os.getcwd(),
        env=os.environ.copy()
    )

    print("\n[INFO] App is running!")
    print(" -> Backend: http://localhost:8000/docs")
    print(" -> Frontend: http://localhost:8501")
    print("\nPress Ctrl+C to stop servers.\n")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping services...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("[INFO] Services stopped.")

if __name__ == "__main__":
    main()
