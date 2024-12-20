import os
import subprocess
from queue import Queue
from typing import Callable

from commands import CodeCompiler, ExeRunner


class Checker:
    def __init__(self, code_dir: str, code_extension: str, compiler: CodeCompiler, runner: ExeRunner):
        self.code_dir = code_dir
        self.code_extension = code_extension

        self.compiler = compiler
        self.runner = runner

        self.check_queue = Queue()

    def push_check(self, filename: str, on_checked_func: Callable[[dict], None]):
        self.check_queue.put((filename, on_checked_func))

    def listen(self):
        while True:
            if not self.check_queue.empty():
                filename, on_checked = self.check_queue.get()

    def check(self, code_file: str):
        pass
