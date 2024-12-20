import os
import subprocess
from typing import Callable, Any

from commands import CodeCompiler, ExeRunner


class Checker:
    def __init__(self, code_dir: str, code_extension: str, compiler: CodeCompiler, runner: ExeRunner):
        self.code_dir = code_dir
        self.code_extension = code_extension

        self.compiler = compiler
        self.runner = runner

        self.check_queue = []

    def push_check(self, filename: str, on_checked_func: Callable[[dict], None]) -> None:
        self.check_queue.append((filename, on_checked_func))

    def listen(self) -> None:
        while True:
            if len(self.check_queue) > 0:
                filename, on_checked = self.check_queue[0]
                result = self.check(filename)
                on_checked(result)
                del self.check_queue[0]

    def check(self, code_file: str) -> dict[str, Any]:
        pass
