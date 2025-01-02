import subprocess
from os.path import join
from os import getcwd,chdir
from server.logger import Logger # not .server.logger


class Compiler:
	def __init__(self, compiler: str, input_dir: str, output_dir: str, logger: Logger):
		self.compiler = compiler
		self.input_dir = input_dir
		self.output_dir = output_dir
		
		self.logger = logger

	def compile(self, filename: str) -> str:
		self.logger.info(f"Compiling... (file {filename})")
		target_filename = filename[:-3] + 'out'	 # file.cpp -> file.out
		command = self.compiler + ' "' + join(self.input_dir, filename) + '" -o "' + join(self.output_dir, target_filename) + '"'
		subprocess.run(command, shell=True)
		return target_filename
