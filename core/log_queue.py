from datetime import datetime
import time


class TempusOnePsLogQueue:
    def __init__(self):
        today = datetime.now()
        self.id_prefix = today.strftime("%b%y-").upper()
        self.log_queue = []
        self.log_data = None

    def log(self, log_data):
        timestamp = time.time()
        log = {
            "log_data": log_data,
            "status": 0,
            "ID": self.id_prefix + str(timestamp)
        }
        # print(log)
        self.log_queue.append(log)
        # print(len(self.log_queue))
        return log["ID"]

    def mask_done(self, log_id):
        for log in self.log_queue:
            if log["ID"] == log_id:
                log["status"] = 1
                return True
        return False

    def get_all(self):
        return self.log_queue

    def clear_done(self):
        self.log_queue = [log for log in self.log_queue if log["status"] != 1]

    def clear_all(self):
        self.log_queue = []
