import subprocess
from os.path import join

from logger import Logger

class Compiler:
	"""
	Class for code compilation
	"""
	def __init__(self, logger: Logger, compiler: str, input_dir: str, output_dir: str):
		"""
		:param compiler: A string that represents the compiler used in commands. Usually g++ or clang++
		:param input_dir: Directory that contains the source code files
		:param output_dir: Directory that will contain the compiled files
		:param logger: Logger instance
		"""
		self.logger = logger
		self.compiler = compiler
		self.input_dir = input_dir
		self.output_dir = output_dir

	def compile(self, filename: str) -> str:
		"""
		Compile a file
		:param filename: Name of the file to compile (must sit in the input directory)
		:return: Name of the compiled file that sits inside the output directory
		"""
		target_filename = filename[:-3] + 'out'	 # file.cpp -> file.out

		command = [self.compiler, join(self.input_dir, filename), "-O2", "--std=c++23", "-o", join(self.output_dir, target_filename)]

		try:
			subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		except FileNotFoundError:
			self.logger.alert(f"{self.compiler} compiler is not installed!", self.compile)

		return target_filename
