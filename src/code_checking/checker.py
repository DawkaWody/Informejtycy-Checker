import os
import subprocess
from typing import Callable, Any
from os.path import exists

from .commands import Compiler
from .pack_loader import PackLoader


class Checker:
	"""
	Main code checking class. Checks everything in check_queue.
	"""
	def __init__(self, compiler: Compiler, pack_loader: PackLoader):
		"""
		:param compiler: Compiler instance
		:param pack_loader: Pack loader instance
		"""
		self.compiler = compiler
		self.pack_loader = pack_loader

		self.compiled_dir = self.compiler.output_dir

		self.check_queue: list[tuple[str, int, Callable[[dict], None]]] = []

	def push_check(self, filename: str, ex_id: int, on_checked_func: Callable[[dict], None]) -> None:
		"""
		Push a file to the checking queue.
		:param filename: Name of the file with source code that will be checked.
		:param ex_id: ID of the exercise (problem header) for which the file will be checked.
		:param on_checked_func: Function to execute when file checking is done.
		"""
		self.check_queue.append((filename, ex_id, on_checked_func))

	def listen(self) -> None:
		"""
		Listens for new files in the checking queue. Should be called in a different thread.
		"""
		while True:
			if len(self.check_queue) > 0:
				filename, ex_id, on_checked = self.check_queue[0]
				result = self.check(filename, ex_id)
				on_checked(result)
				del self.check_queue[0]

	def check(self, code_file: str, ex_id: int) -> dict[str, Any]:
		"""
		Compiles and checks the code file.
		:param code_file: File with source code that needs to be checked.
		:param ex_id: ID of the exercise (problem header) for which the file will be checked.
		:return: Result dict containing "%" key with percentage of tests passed and
		(if applies) "first_failed" with the first failed test.
		"""
		result = {"%": None, "first_failed": None}
		score = 0
		program = self.compiler.compile(code_file)
		test_pack = self.pack_loader.load_bytes(ex_id)
		
		#if not exist('"'+os.path.join(self.compiled_dir, program)+'"'):
		#	self.logg
		
		for test_in, test_out in test_pack:
			o = subprocess.check_output('"' + os.path.join(self.compiled_dir, program) + '"', input=test_in, shell=True)
			if o.decode()[:-1] == test_out.decode():
				score += 1
			elif result["first_failed"] is None:
				result["first_failed"] = test_in

		os.remove(os.path.join(self.compiled_dir, program))
		os.remove(os.path.join(self.compiler.input_dir, code_file))
		result["%"] = (score / len(test_pack)) * 100
		return result
