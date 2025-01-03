import subprocess
from os.path import join
from server.logger import Logger # not .server.logger (wiadomo xD)


class Compiler:
	"""
	Class for code compilation
	"""
	def __init__(self, compiler: str, input_dir: str, output_dir: str, logger: Logger):
		"""
		:param compiler: A string that represents the compiler used in commands. Usually g++ or clang++
		:param input_dir: Directory that contains the source code files
		:param output_dir: Directory that will contain the compiled files
		:param logger: Logger instance
		"""
		self.compiler = compiler
		self.input_dir = input_dir
		self.output_dir = output_dir
		
		self.logger = logger

	def compile(self, filename: str) -> str:
		"""
		Compile a file
		:param filename: Name of the file to compile (must sit in the input directory)
		:return: Name of the compiled file that sits inside the output directory
		"""
		self.logger.info(f"Compiling... (file {filename})")
		target_filename = filename[:-3] + 'out'	 # file.cpp -> file.out
		command = self.compiler + ' "' + join(self.input_dir, filename) + '" -o "' + join(self.output_dir, target_filename) + '"'
		subprocess.run(command, shell=True)
		return target_filename
