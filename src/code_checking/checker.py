from queue import Queue

class Checker:
    def __init__(self, code_dir: str, code_extension: str):
        self.code_dir = code_dir
        self.code_extension = code_extension

        self.check_queue = Queue()