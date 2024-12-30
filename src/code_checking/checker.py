import os
import subprocess
from typing import Callable, Any

from commands import Compiler
from pack_loader import PackLoader


class Checker:
    def __init__(self, compiler: Compiler, pack_loader: PackLoader):
        self.compiler = compiler
        self.pack_loader = pack_loader

        self.compiled_dir = self.compiler.output_dir

        self.check_queue = []

    def push_check(self, filename: str, ex_id:int, on_checked_func: Callable[[dict], None]) -> None:
        self.check_queue.append((filename, ex_id, on_checked_func))

    def listen(self) -> None:
        while True:
            if len(self.check_queue) > 0:
                filename, ex_id, on_checked = self.check_queue[0]
                result = self.check(filename, ex_id)
                on_checked(result)
                del self.check_queue[0]

    def check(self, code_file: str, ex_id: int) -> dict[str, Any]:
        result = {}
        self.compiler.compile(code_file)
        for i, test_in, test_out in enumerate(self.pack_loader.load_bytes(ex_id)):
            data, write = os.pipe()
            os.write(write, test_in)
            o = subprocess.check_output(os.path.join(self.compiled_dir, code_file), stdin=data, shell=True)
            result[i] = o == test_out
