import subprocess
from os.path import join

from logger import Logger

class Compiler:
	"""
	Class for code compilation
	"""
	def __init__(self, logger: Logger, compiler: str, input_dir: str, output_dir: str, debug_output_dir: str):
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
		self.debug_output_dir = debug_output_dir

	def compile(self, filename: str, debug: bool = False) -> str:
		"""
		Compile a file
		:param filename: Name of the file to compile (must sit in the input directory)
		:param debug: Is file compiled for debugging (with -g flag)
		:return: Name of the compiled file that sits inside the output directory
		"""
		target_filename = filename[:-3] + 'out'	 # file.cpp -> file.out

		command = []
		if not debug:
			command = [self.compiler, join(self.input_dir, filename), "-o", join(self.output_dir, target_filename)]
		else:
			command = [self.compiler, join(self.input_dir, filename), "-g", "-o", join(self.debug_output_dir, target_filename)]

		try:
			subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		except FileNotFoundError:
			self.logger.alert(f"{self.compiler} compiler is not installed!", self.compile)

		return target_filename
