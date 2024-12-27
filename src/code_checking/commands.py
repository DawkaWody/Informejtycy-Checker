import subprocess
from os.path import join


class CodeCompiler:
    def __init__(self, compiler: str):
        self.compiler = compiler

    def compile(self, file_path: str, program_id: int) -> None:
        command = self.compiler + ' ' + file_path + ' -o ' + str(program_id)
        subprocess.run(command, shell=True)


class ExeRunner:
    def __init__(self, exe_dir_path: str):
        self.exe_dir_path = exe_dir_path

    def run(self, file: str, readable_input) -> bytes:
        output = subprocess.check_output(join(self.exe_dir_path, file), stdin=readable_input, shell=True)
        return output
