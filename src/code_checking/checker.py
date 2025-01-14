import os
import subprocess
from typing import Callable, Any

from server.client import Client

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

		self.check_queue: list[tuple[str, Client, int, Callable[[dict, Client, int], None]]] = []

	def push_check(self, filename: str, client: Client, ex_id: int, on_checked_func: Callable[[dict, Client, int], None]) -> None:
		"""
		Push a file to the checking queue.
		:param filename: Name of the file with source code that will be checked.
		:param client: Socket, IP and PORT of the source code sender.
		:param ex_id: ID of the exercise (problem header) for which the file will be checked.
		:param on_checked_func: Function to execute when file checking is done.
		"""
		self.check_queue.append((filename, client, ex_id, on_checked_func))

	def listen(self) -> None:
		"""
		Listens for new files in the checking queue. Should be called in a different thread.
		"""
		while True:
			if len(self.check_queue) > 0:
				filename, client, ex_id, on_checked = self.check_queue[0]
				result = self.check(filename, ex_id)
				on_checked(result, client, ex_id)
				del self.check_queue[0]
				if result["invalid_problem_id"] or result["compilation_error"]:
					os.remove(os.path.join(self.compiler.input_dir, filename))

	def check(self, code_file: str, ex_id: int) -> dict[str, Any]:
		"""
		Compiles and checks the code file. The file after checking.
		:param code_file: File with source code that needs to be checked.
		:param ex_id: ID of the exercise (problem header) for which the file will be checked.
		:return: Result dict containing "%" key with percentage of tests passed and
		(if applies) "first_failed" with the first failed test.
		"""
		
		score = 0
		result = {"%": None, "first_failed": None, "time_limit_exceeded": False,
				  "compilation_error": False, "invalid_problem_id": False}

		if ex_id >= self.pack_loader.get_pack_count():
			result["invalid_problem_id"] = True
			return result

		program = self.compiler.compile(code_file)
		
		if not os.path.exists(os.path.join(self.compiled_dir, program)):
			result["compilation_error"] = True
			return result
		
		test_pack = self.pack_loader.load_bytes(ex_id)
		pack_config = self.pack_loader.load_config(ex_id)

		for test_in, test_out in test_pack:
			try:
				output = subprocess.check_output(os.path.join(self.compiled_dir, program),
												 input=test_in, timeout=pack_config['time_limit'])
			except subprocess.CalledProcessError:
				result["first_failed"] = test_in
				break

			except subprocess.TimeoutExpired:
				result["time_limit_exceeded"] = True
				result["first_failed"] = test_in
				break

			if output.decode()[:-1] == test_out.decode():
				score += 1
			else:
				result["first_failed"] = test_in
				break

		os.remove(os.path.join(self.compiled_dir, program))
		os.remove(os.path.join(self.compiler.input_dir, code_file))
		result["%"] = (score / len(test_pack)) * 100
		return result