import subprocess
from os.path import join
import os

class Compiler:
    def __init__(self, compiler: str, input_dir: str, output_dir: str):
        self.compiler = compiler
        self.input_dir = input_dir
        self.output_dir = output_dir

    def compile(self, filename: str) -> str:
        target_filename = filename[:-3] + 'out'  # file.cpp -> file.out
        command = self.compiler + ' "' + join(self.input_dir, filename) + '" -o "' + join(self.output_dir, target_filename) + '"'
        subprocess.run(command, shell=True)
        return target_filename
