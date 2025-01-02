import os
import subprocess
from typing import Callable, Any

from .commands import Compiler
from .pack_loader import PackLoader


class Checker:
    def __init__(self, compiler: Compiler, pack_loader: PackLoader):
        self.compiler = compiler
        self.pack_loader = pack_loader

        self.compiled_dir = self.compiler.output_dir

        self.check_queue = []

    def push_check(self, filename: str, ex_id: int, on_checked_func: Callable[[dict], None]) -> None:
        self.check_queue.append((filename, ex_id, on_checked_func))

    def listen(self) -> None:
        while True:
            if len(self.check_queue) > 0:
                filename, ex_id, on_checked = self.check_queue[0]
                result = self.check(filename, ex_id)
                on_checked(result)
                del self.check_queue[0]

    def check(self, code_file: str, ex_id: int) -> dict[str, Any]:
        result = {"%": None, "first_failed": None}
        score = 0
        program = self.compiler.compile(code_file)
        test_pack = self.pack_loader.load_bytes(ex_id)
        for test_in, test_out in test_pack:
            data, write = os.pipe()
            os.write(write, test_in)
            print(os.path.join(self.compiled_dir, program))
            o = subprocess.check_output(os.path.join(self.compiled_dir, program), stdin=data, shell=True)
            if o == test_out:
                score += 1
            else:
                result["first_failed"] = test_in
                break

        result["%"] = score / len(test_pack)
        return result
