import subprocess
import time
import os
import signal

process = None


def restart():
    global process
    if process:
        process.terminate()
        process.wait()
    process = subprocess.Popen(["streamlit", "run", "main.py"])


try:
    restart()
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class ChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith(".py"):
                print(f"File changed: {event.src_path}")
                restart()

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    if process:
        process.terminate()
    observer.stop()
    observer.join()
