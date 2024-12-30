import subprocess
from os.path import join


class Compiler:
    def __init__(self, compiler: str, input_dir: str, output_dir: str):
        self.compiler = compiler
        self.input_dir = input_dir
        self.output_dir = output_dir

    def compile(self, filename: str) -> None:
        command = self.compiler + ' ' + join(self.input_dir, filename) + ' -o ' + join(self.output_dir, filename)
        subprocess.run(command, shell=True)
