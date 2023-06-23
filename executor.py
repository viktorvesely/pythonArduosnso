import threading
import time

from task import Task
from presses import KeyChecker
from puncher import Puncher


class Executor:

    def __init__(self) -> None:
        self.workers : list[Task] = []

    def run_thread(self, worker):

        worker.start()
        self.workers.append(worker)

    def join(self):

        for worker in self.workers:
            worker.join()

    def stop(self):
        print("Stopping all the workers")

        for worker in self.workers:
            worker.stop()

    

if __name__ == "__main__":
    exec = Executor()

    exec.run_thread(KeyChecker({
        "q": exec.stop
    }))

    puncher = Puncher(visual=True)
    
    exec.run_thread(puncher)

    exec.join()