from gui import *
import subprocess

def run_flask_server():
    flask_process = subprocess.Popen(["python3", "wui.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return flask_process

def stop_flask_server(flask_process):
    flask_process.terminate()
    flask_process.wait()

if __name__ == "__main__":
    process = run_flask_server()
    root()
    stop_flask_server(process)
