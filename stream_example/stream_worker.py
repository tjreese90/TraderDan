from queue import Queue
import threading
import time
from instrumentCollection.log_wrapper import LogWrapper
from models.live_api_price import LiveApiPrice

class WorkProcessor(threading.Thread):
    
    def __init__(self, work_queue: Queue):
        super().__init__()
        self.work_queue = work_queue
        self.log = LogWrapper("workProcessor")
    
    
    def run(self):
        while True:
            work: LiveApiPrice = self.work_queue.get()
            self.log.logger.debug(f"New Work: {work}")
            time.sleep(7)
            # Where we place trade, of update data base etc, based on live prices