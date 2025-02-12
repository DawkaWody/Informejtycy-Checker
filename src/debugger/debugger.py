import os
import time
from pygdbmi.gdbcontroller import GdbController
from uuid import uuid4
from pprint import pprint
from typing import Optional

from code_checking.commands import Compiler


class GDBDebugger:
	'''
	Class for managing debug process (gdb).
	'''

	def __init__(self, compiler: Compiler, debug_dir: str, file_name: str) -> None:
		self.compiler = compiler
		self.received_dir = self.compiler.input_dir
		self.debug_dir = debug_dir
		self.file_name = file_name

		self.last_ping_time: int = time.time() # time in seconds from the last time client pinged this class

		self.gdb_init_input = [
			"set debuginfod enabled off",
			"python",
			"import sys",
			"sys.path.insert(0, '/usr/share/gcc/python/')",
			"from libstcxx.v6.printers import register_libstdcxx_printers",
			"register_libstdcxx_printers(None)",
			"end",
			"break main",
			"run"
		]

		self.compiled_file_name = ""
		self.process: Optional[pexpect.spawnu] = None
		self.container_name: str = ""

		self.docker_manager = DockerManager(self.compiler.output_dir, debug_dir)
		self.memory_limit_MB = 128

	def ping(self) -> None:
		'''
		Updates last time, the class was pinged.
		'''
		self.last_ping_time = time.time()

	def pprint_response(self, response: dict) -> None:
		pprint(response)

	def run(self) -> int:
		'''
		Runs debug process (gdb).
		:param file_name: Path to the source code file that will be debugged
		'''
		output_file_name = self.compiler.compile(self.file_name, debug=True)

		if not os.path.exists(os.path.join(self.debug_dir, output_file_name)):
			return -1

		self.compiled_file_name = output_file_name
		self.docker_manager.build_for_debugger(self.compiled_file_name)

		self.process, self.container_name, stdin_input_file = self.docker_manager.run_for_debugger("here_is_stdin", self.memory_limit_MB)

		self.stop()
		return 0

	def stop(self) -> None:
		'''
		Stops debug process (gdb) and deinitalizes the class.
		'''
		if self.compiled_file_name:
			os.remove(os.path.join(self.debug_dir, self.compiled_file_name))
			self.compiled_file_name = ""
		os.remove(os.path.join(self.received_dir, self.file_name))

		self.process.close(force=True)
		self.process = None
