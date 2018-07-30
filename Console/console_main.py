import time
import threading


class ConsoleMain:
    def __init__(self, model, main_ctrl):
        self.model = model
        self.main_ctrl = main_ctrl

        self.running = False
        self.frequency = 1
        self.thread = None
        self.lock = threading.Lock()
        self.main_ctrl.paper_login()
        self.start()
        print("Console View")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

    def stop(self):
        self.running = False

        try:
            self.thread.join()
            print("Thread destroyed")

        except Exception as e:
            return None

    def update(self):
        self.main_ctrl.import_transactions()

        while self.running:
            self.lock.acquire()
          #  print(self.model.target_price)
            self.lock.release()
            time.sleep(self.frequency)


