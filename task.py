import threading
import time


class Task(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, daemon=True, **kwargs)

    def is_running(self) -> bool:
        return self._running

    def run(self):
        self._running = True

    def stop(self):
        self._running = False

    def sleep(self, seconds: float):
        time.sleep(seconds)